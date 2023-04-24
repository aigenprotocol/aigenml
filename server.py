import datetime
import glob
import os

from flask import Flask, request, flash, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from werkzeug.utils import secure_filename

from aigenml import save_model, create_shards
from aigenml.config import MODELS_DIR
from aigenml.utils import slugify

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'h5'}

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    """
    Create app
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your secret key'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MODEL_FOLDER'] = MODELS_DIR
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000 * 1000
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/apple/aigen/aigenml.db"
    db.init_app(app)
    migrate.init_app(app, db)

    CORS(app)

    return app


app = create_app()

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(app.config['MODEL_FOLDER'], exist_ok=True)

"""
Models
"""


class AIProject(db.Model, SerializerMixin):
    __tablename__ = 'ai_project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    model_dir = db.Column(db.String)
    no_of_ainfts = db.Column(db.Integer)
    status = db.Column(db.String)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class SmartContract(db.Model, SerializerMixin):
    __tablename__ = "smart_contract"
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String, nullable=False)
    chain = db.Column(db.String, nullable=False)
    projectId = db.Column(db.Integer, nullable=False)
    compiledContractPath = db.Column(db.String, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class AINFT(db.Model, SerializerMixin):
    __tablename__ = 'ai_nft'
    id = db.Column(db.Integer, primary_key=True)
    projectId = db.Column(db.Integer, nullable=False)
    fileName = db.Column(db.String, unique=True, nullable=False)
    dataCid = db.Column(db.String, nullable=True)
    metadataCid = db.Column(db.String, nullable=True)
    format = db.Column(db.String, nullable=True)
    tokenId = db.Column(db.String, nullable=True)
    status = db.Column(db.String, default="pending")
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


@app.route("/")
def home():
    return {"status": "success", "message": "Hello, World"}


@app.route("/project", methods=["get", "post"])
def project_api():
    if request.method == 'POST':
        print(request.data, request.form)
        name = request.form['name']
        no_of_ainfts = int(request.form['no_of_ainfts'])

        # Create AI NFT Project
        model_name = slugify(name)
        model_dir = os.path.join(app.config['MODEL_FOLDER'], model_name)
        project = db.session.execute(db.select(AIProject).where(AIProject.name == name)).all()
        if len(project) == 0:
            project1 = AIProject(name=name, model_dir=model_dir, no_of_ainfts=no_of_ainfts)
            db.session.add(project1)
            db.session.commit()
        else:
            return jsonify({"status": "failure", "message": "Project already exists!"})

        response = save_file(request)
        if response['status'] == "success":
            # load it and save weights
            save_model(model_name=model_name, model_dir=app.config['MODEL_FOLDER'], model_path=response['file_path'])
            create_shards(model_name=model_name, model_dir=app.config['MODEL_FOLDER'], no_of_ainfts=no_of_ainfts)
            print('Model saved')

            # Create AI NFT in the database
            model_dir = project1.model_dir
            files = glob.glob(os.path.join(model_dir, "final_shards/*"))
            for filename in files:
                ainft = AINFT(fileName=os.path.join("final_shards", os.path.basename(filename)), projectId=project1.id)
                db.session.add(ainft)
                db.session.commit()

            # Config file
            ainft1 = AINFT(fileName=model_name + "_config.json", projectId=project1.id)
            db.session.add(ainft1)
            db.session.commit()

            return jsonify({"status": "success", "message": "Model saved and shards created",
                            "project_id": project1.id})
        else:
            return response
    elif request.method == "GET":
        project_id = request.args.get('id', None)
        if project_id is None:
            return jsonify({"status": "failure", "message": "Project id is missing"})
        ainft_project = AIProject.query.filter_by(id=project_id).first()
        return jsonify({"status": "success", "project": ainft_project.to_dict()})
    else:
        return jsonify({"status": "failure", "message": "Invalid request"})


@app.route("/projects", methods=["get"])
def get_projects():
    if request.method == "GET":
        ainft_projects = [project.to_dict() for project in AIProject.query.order_by(AIProject.created_date.desc())]
        return {"status": "success", "projects": ainft_projects}
    else:
        return jsonify({"status": "failure", "message": "Invalid request"})


@app.route("/project/ainft", methods=["get"])
def get_project_ainft():
    if request.method == "GET":
        project_id = request.args.get('id', None)
        print(request.args)
        if project_id is None:
            return jsonify({"status": "failure", "message": "Project id is missing"})
        ainfts = [ainft.to_dict() for ainft in AINFT.query.filter_by(projectId=project_id).all()]
        return {"status": "success", "ainfts": ainfts}
    else:
        return jsonify({"status": "failure", "message": "Invalid request"})


def save_file(request):
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        print('No file part')
        return {"status": "failure", "message": "No file found"}
    file = request.files['file']
    # If the user does not select a file, the browser submits an empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        print("No selected file")
        return {"status": "failure", "message": "No file found"}

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return {"status": "success", "message": "File uploaded",
                "file_path": os.path.join(app.config['UPLOAD_FOLDER'], filename)}
    else:
        print("Unsupported type")
        return {"status": "failure", "message": "Unsupported file type"}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
