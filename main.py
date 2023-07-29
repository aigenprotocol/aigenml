from dotenv import load_dotenv

load_dotenv()

import shutil
import argparse
import os

from aigenml.utils import slugify
from aigenml import create_shards, save_model, merge_shards, load_model_weights

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='AigenML', description="Aigen's machine learning library to extract models "
                                                                 "weights, create shards, merge shards, and load model "
                                                                 "based on number of ainfts specified",
                                     epilog="Get more help at contact@aigenprotocol.com")
    parser.add_argument('-a', '--action', help='specify action')
    parser.add_argument('-n', '--name', help='specify project name')
    parser.add_argument('-m', '--model_path', help='specify model path')
    parser.add_argument('-no', '--no_of_ainfts', type=int, help='specify number of ainfts to create')
    args = parser.parse_args()

    project_name = slugify(args.name)

    # create project directory
    os.makedirs(os.path.join(os.environ.get("PROJECTS_DIR"), project_name), exist_ok=True)

    if args.action == "create_shards":
        # remove directory
        if os.path.exists(os.path.join(os.environ.get("PROJECTS_DIR"), project_name)):
            shutil.rmtree(os.path.join(os.environ.get("PROJECTS_DIR"), project_name))

        # extracts and save model weights
        save_model(project_name=project_name, project_dir=os.environ.get("PROJECTS_DIR"), model_path=args.model_path)
        print("Model weights extracted successfully!")

        # create shards
        create_shards(project_name=project_name, project_dir=os.environ.get("PROJECTS_DIR"),
                      no_of_ainfts=args.no_of_ainfts)
        print("Model shards created successfully!")

        print("Project name:", project_name)
        print("Project directory:", os.path.join(os.environ.get("PROJECTS_DIR"), project_name))
    elif args.action == "merge_shards":
        merge_shards(args.name)
        print("Shards merged successfully!")
    elif args.action == "load_model":
        model = load_model_weights(project_name=args.name)
        print("Model loaded successfully!:", model)
    else:
        print("Invalid action")
