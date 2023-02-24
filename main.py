import numpy as np

from aigenml import create_shards, save_model, load_model_weights, aggregate_shards, concatenate_arrays, \
    get_keras_model, compare_weights, compare_predictions
import tensorflow as tf

if __name__ == '__main__':
    model_name = "mobilenet"

    # extract and create shards
    # save_model(model_name=model_name)
    # create_shards(model_name=model_name, minimum_split_size=1000000, maximum_split_size=10000000)

    # aggregate_shards(model_name=model_name)
    # concatenate_arrays(model_name=model_name)

    # validate_merged_shards(model_name=model_name)
    model1 = get_keras_model(model_name)
    model = load_model_weights(model_name)
    print(model)

    print(compare_weights(model, model1))
    compare_predictions(model, model1)

