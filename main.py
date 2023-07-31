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
    parser.add_argument('-id', '--project_id', help='specify project id')
    parser.add_argument('-n', '--name', help='specify project name')
    parser.add_argument('-m', '--model_path', help='specify model path')
    parser.add_argument('-no', '--no_of_ainfts', type=int, help='specify number of ainfts to create')
    args = parser.parse_args()

    project_name = slugify(args.name)
    project_id = args.name
    project_dir = os.path.join(os.environ.get("PROJECTS_DIR"), f"${project_name}_${project_id}")

    # create project directory
    os.makedirs(project_dir, exist_ok=True)

    if args.action == "create_shards":
        # remove directory
        if os.path.exists(project_dir):
            shutil.rmtree(project_dir)

        # extracts and save model weights
        save_model(project_name=project_name, project_dir=project_dir, model_path=args.model_path)
        print("Model weights extracted successfully!")

        # create shards
        create_shards(project_name=project_name, project_id=project_id, project_dir=project_dir,
                      no_of_ainfts=args.no_of_ainfts)
        print("Model shards created successfully!")

        print("Project name:", project_name)
        print("Project directory:", project_dir)
    elif args.action == "merge_shards":
        merge_shards(project_name=project_name, project_dir=project_dir)
        print("Shards merged successfully!")
    elif args.action == "load_model":
        model = load_model_weights(project_name=project_name, project_dir=project_dir)
        print("Model loaded successfully!:", model)
    else:
        print("Invalid action")
