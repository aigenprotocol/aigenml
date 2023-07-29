import glob
import json
import numpy as np
import os
import pandas as pd
import tensorflow as tf


def load_model(project_name):
    """
    Load model from config file
    :return: Keras model
    """
    with open(os.path.join(os.path.join(os.environ.get("PROJECTS_DIR"), project_name),
                           "{}_config.json".format(project_name)), "r") as f:
        return tf.keras.Model().from_config(json.load(f))


def load_model_weights(project_name, project_dir):
    model = load_model(project_name)
    final_weights_dir = os.path.join(project_dir, "final_weights")

    filepaths = glob.glob("{}/*".format(final_weights_dir))

    for filepath in filepaths:
        with open(filepath, "r") as f:
            layer_dict = json.load(f)
            layer_name = layer_dict['layer_name']
            weights = layer_dict['weights']

            if len(weights) == 0:
                model.get_layer(layer_name).set_weights(weights)
            else:
                df = pd.DataFrame(weights)
                df1 = df.sort_values(by=['weight_no'], ascending=True)
                values = df1['values'].to_list()
                values = [np.array(a) for a in values]
                model.get_layer(layer_name).set_weights(values)

    return model
