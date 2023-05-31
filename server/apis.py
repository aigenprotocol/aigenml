import glob
import os
import re

from flask import request, jsonify
from sqlalchemy import Update

from aigenml import save_model, create_shards
from server.models import AIProject, AINFT, UserDetails
from server.nftstorage import save_image_to_NFTSTORAGE, delete_file_from_NFT_STORAGE
from server.utils import slugify, save_files
from .globals import globals as g


@g.app.route("/")
def home():
    return {"status": "success", "message": "Hello, World"}


@g.app.route("/project/ainft", methods=["post", "get"])
def create_project_NFT():
    if request.method == 'POST':
        print(request.data, request.form)
        id = request.form['id']
        project = g.db.session.query(AIProject).filter(AIProject.id == id).first()
        print(project)
        project_price = request.form['projectPrice']
        price_per_nft = request.form['pricePerNFT']
        no_of_ainfts = int(request.form['no_of_ainfts'])
        # Create AI NFT Project
        model_name = slugify(project.name)
        model_dir = os.path.join(g.app.config['MODEL_FOLDER'], model_name)

        # Check if the project exists
        if project:
            # Update the project with the new parameters
            project.model_dir = model_dir
            project.no_of_ainfts = no_of_ainfts
            project.project_price = project_price
            project.price_per_nft = price_per_nft

            # Commit the changes to the database
            g.db.session.commit()

        else:
            return jsonify({"status": "failure", "message": "Project Does Not exists!"})

        response = save_files(request)
        if response['status'] == "success":
            #     # load it and save weights
            save_model(model_name=model_name, model_dir=g.app.config['MODEL_FOLDER'],
                       model_path=response['model_file_path'])
            create_shards(model_name=model_name, model_dir=g.app.config['MODEL_FOLDER'], no_of_ainfts=no_of_ainfts)
            print('Model saved')
            #
            # Create AI NFT in the database
            model_dir = project.model_dir
            files = glob.glob(os.path.join(model_dir, "final_shards/*"))
            for filename in files:
                ainft = AINFT(fileName=os.path.join("final_shards", os.path.basename(filename)), projectId=project.id)
                g.db.session.add(ainft)
                g.db.session.commit()
            #
            # Config file
            ainft1 = AINFT(fileName=model_name + "_config.json", projectId=project.id)
            g.db.session.add(ainft1)
            g.db.session.commit()
            #
            project.status = "Model Saved"
            g.db.session.commit()
            return jsonify({"status": "success", "message": "Model saved and shards created",
                            "project_id": project.id})
        else:
            return response
    elif request.method == "GET":
        project_id = request.args.get('id', None)
        print(request.args)
        if project_id is None:
            return jsonify({"status": "failure", "message": "Project id is missing"})
        ainfts = [ainft.to_dict() for ainft in AINFT.query.filter_by(projectId=project_id).all()]
        return {"status": "success", "ainfts": ainfts}
    else:
        return jsonify({"status": "failure", "message": "Invalid request"})


@g.app.route("/project", methods=["get", "post"])
def project_api():
    if request.method == 'POST':
        print(request.data, request.form)
        name = request.form['name']
        description = request.form['description']
        account = request.form['account']
        logo_link = save_image_to_NFTSTORAGE(request, 'logo_file')
        banner_link = save_image_to_NFTSTORAGE(request, 'banner_file')
        project = g.db.session.execute(g.db.select(AIProject).where(AIProject.name == name)).all()

        if len(project) == 0:
            project1 = AIProject(name=name, description=description, logo=logo_link, banner=banner_link,
                                 account=account, status="Created")
            g.db.session.add(project1)
            g.db.session.commit()
            return jsonify({"status": "success", "message": "Project Created Successfully"})
        else:
            return jsonify({"status": "failure", "message": "Project already exists!"})

    elif request.method == "GET":
        project_id = request.args.get('id', None)
        account = request.args.get('account', None)
        print(id, account)
        if project_id is None:
            ainft_projects = [project.to_dict() for project in
                              AIProject.query.filter_by(account=account).order_by(AIProject.created_date.desc())]
            return {"status": "success", "projects": ainft_projects}
        ainft_project = AIProject.query.filter_by(id=project_id).first()
        return jsonify({"status": "success", "project": ainft_project.to_dict()})
    else:
        return jsonify({"status": "failure", "message": "Invalid request"})


@g.app.route("/profile", methods=["get", "post"])
def profile_function():
    if request.method == "GET":
        address = request.args.get('address', None)

        profile = g.db.session.execute(g.db.select(UserDetails).where(UserDetails.address == address)).all()

        if len(profile) == 0:
            profile1 = UserDetails(address=address)
            g.db.session.add(profile1)
            g.db.session.commit()

        profile = [profile.to_dict() for profile in UserDetails.query.filter_by(address=address).all()]
        return {"status": "success", "profile": profile}
    elif request.method == "POST":
        address = request.form.get('address', None)
        file_type = request.form.get('file_type', None)
        username = request.form.get('username', None)
        if file_type == 'banner_file':
            banner_link = save_image_to_NFTSTORAGE(request, file_type)
            profile = [profile.to_dict() for profile in UserDetails.query.filter_by(address=address).all()]
            prev_banner_link = profile[0].get('banner', None)
            if prev_banner_link:
                pattern = r"https://ipfs.io/ipfs/([^/]+)/"
                match = re.search(pattern, prev_banner_link)

                if match:
                    cid = match.group(1)
                    delete_file_from_NFT_STORAGE(cid)
                else:
                    print("CID not found in the link.")

            update_statement = (
                Update(UserDetails)
                .where(UserDetails.address == address)
                .values(banner=banner_link)
            )

            g.db.session.execute(update_statement)
            g.db.session.commit()
            return {"status": "success", "banner": banner_link}
        if file_type == 'profile_picture_file':
            profile_picture_link = save_image_to_NFTSTORAGE(request, file_type)
            profile = [profile.to_dict() for profile in UserDetails.query.filter_by(address=address).all()]
            prev_profile_picture_link = profile[0].get('profilePicture', None)
            if prev_profile_picture_link:
                pattern = r"https://ipfs.io/ipfs/([^/]+)/"
                match = re.search(pattern, prev_profile_picture_link)

                if match:
                    cid = match.group(1)
                    delete_file_from_NFT_STORAGE(cid)
                else:
                    print("CID not found in the link.")
            update_statement = (
                Update(UserDetails)
                .where(UserDetails.address == address)
                .values(profilePicture=profile_picture_link)
            )

            g.db.session.execute(update_statement)
            g.db.session.commit()
            return {"status": "success", "profile_picture": profile_picture_link}
        if username:
            update_statement = (
                Update(UserDetails)
                .where(UserDetails.address == address)
                .values(username=username)
            )

            g.db.session.execute(update_statement)
            g.db.session.commit()
            return {"status": "success", "username": username}

        return jsonify({"status": "failure", "message": "Invalid request"})

    else:
        return jsonify({"status": "failure", "message": "Invalid request"})
