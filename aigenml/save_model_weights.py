import json
import numpy as np
import os
from tensorflow import keras

from aigenml import create_shards


def clean_dict_helper(d):
    if isinstance(d, np.ndarray):
        return d.tolist()

    if isinstance(d, list):  # For those db functions which return list
        return [clean_dict_helper(x) for x in d]

    if isinstance(d, dict):
        for k, v in d.items():
            d.update({k: clean_dict_helper(v)})

    # return anything else, like a string or number
    return d


def save_model_architecture(project_name, project_dir, model):
    print("Saving model architecture")
    with open("{}/{}_config.json".format(project_dir, project_name), "w") as f:
        config = clean_dict_helper(model.get_config())
        json.dump(config, f)


def save_model_weights(project_dir, model):
    print("Saving model weights")
    for layer in model.layers:
        weight_format = {"layer_name": layer.name}

        all_weights = []
        for index, weights in enumerate(layer.get_weights()):
            all_weights.append({"weight_no": index + 1, "shard_no": 1, "values": weights.tolist()})

        weight_format['weights'] = all_weights
        with open("{}/weights/{}.json".format(project_dir, layer.name), "w") as f:
            json.dump([weight_format], f)


def save_model(project_name, project_dir, model_path):
    os.makedirs(project_dir, exist_ok=True)
    os.makedirs(os.path.join(project_dir, "weights"), exist_ok=True)

    model = keras.models.load_model(model_path)

    save_model_weights(project_dir, model)
    save_model_architecture(project_name, project_dir, model)


def save_model_create_shards(project_name, project_id, project_dir,
                             model_path, no_of_ainfts):
    save_model(project_name=project_name, project_dir=project_dir,
               model_path=model_path)
    create_shards(project_name=project_name, project_id=project_id,
                  project_dir=project_dir, no_of_ainfts=no_of_ainfts)
