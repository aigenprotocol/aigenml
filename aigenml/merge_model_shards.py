import glob
import json
import os

import numpy as np
import pandas as pd


def aggregate_shards(model_name):
    aggregated_shards_dir = os.path.join(model_name, "aggregated_shards")
    downloaded_shards_dir = os.path.join(model_name, "downloaded_shards")
    os.makedirs(aggregated_shards_dir, exist_ok=True)

    filepaths = glob.glob(os.path.join(downloaded_shards_dir, "{}_shard_*".format(model_name)))

    for index, filepath in enumerate(filepaths):
        print("File processed {} out of {}".format(index + 1, len(filepaths)))
        print("Filepath:", filepath)
        with open(filepath, "r") as f:
            layer_weights = json.load(f)

            for layer_dict in layer_weights:
                layer_name = layer_dict['layer_name']

                aggregated_shards_file = os.path.join(aggregated_shards_dir, "{}.json".format(layer_name))

                if os.path.exists(aggregated_shards_file):
                    with open(aggregated_shards_file, "r") as fp:
                        existing_weights = json.load(fp)['weights']
                        existing_weights.extend(layer_dict['weights'])
                else:
                    existing_weights = layer_dict['weights']

                with open(os.path.join(aggregated_shards_file), "w") as fq:
                    json.dump({"layer_name": layer_dict['layer_name'], "weights": existing_weights}, fq)


def concatenate_arrays(model_name):
    aggregated_shards_dir = os.path.join(model_name, "aggregated_shards")
    final_weights_dir = os.path.join(model_name, "final_weights")
    os.makedirs(final_weights_dir, exist_ok=True)

    filepaths = glob.glob(os.path.join(aggregated_shards_dir, "*"))

    for index, filepath in enumerate(filepaths):
        print("File processed {} out of {}".format(index + 1, len(filepaths)))
        print("Filepath:", filepath)
        with open(filepath, "r") as f:
            layer_dict = json.load(f)

            layer_name = layer_dict['layer_name']
            weights = layer_dict['weights']

            if len(weights) == 0:
                with open(os.path.join(final_weights_dir, "{}.json".format(layer_name)), "w") as fp:
                    json.dump(layer_dict, fp)
            else:
                df = pd.DataFrame(weights)
                print(df)
                weight_nos = list(set(df['weight_no'].tolist()))
                print(weight_nos)
                all_stacked_weights = []

                for weight_no in weight_nos:
                    weights1 = df.loc[df['weight_no'] == weight_no]
                    weights1 = weights1.sort_values(by=['shard_no'], ascending=True)
                    values = weights1['values'].to_list()
                    if len(values) == 1:
                        stacked_weights = values[0]
                    else:
                        print(type(values))
                        stacked_weights = np.concatenate(values, axis=-1).tolist()

                    all_stacked_weights.append({"weight_no": weight_no, "shard_no": 1,
                                                "values": stacked_weights})

                layer_dict['weights'] = all_stacked_weights

                with open(os.path.join(final_weights_dir, "{}.json".format(layer_name)), "w") as fp:
                    json.dump(layer_dict, fp)

# def merge_shards(model_name):
#     final_weights_dir = os.path.join(model_name, "final_weights")
#     shards_dir = os.path.join(model_name, "shards")
#     os.makedirs(final_weights_dir, exist_ok=True)
#
#     filepaths = glob.glob(os.path.join(shards_dir, "{}_shard_*".format(model_name)))
#
#     for filepath in filepaths:
#         print("Processing:", filepath)
#         if "xception_shard_45" in filepath:
#             pass
#
#         with open(filepath, "r") as f:
#             weights = json.load(f)
#             for key, value in weights.items():
#                 # print(key, np.array(value))
#                 keys = key.split("/")
#                 layer_name = keys[0]
#                 weight_no = keys[1]
#                 if len(keys) >= 3:
#                     shard_no = keys[2].split(":")[1]
#                 else:
#                     shard_no = "1"
#
#                 existing_weights_file = os.path.join(final_weights_dir, "{}.json".format(layer_name))
#
#                 existing_weights = {}
#                 if os.path.exists(existing_weights_file):
#                     with open(existing_weights_file, "r") as fp:
#                         existing_weights = json.load(fp)
#
#                 existing_weight = existing_weights.get("{}/{}".format(layer_name, weight_no), None)
#
#                 print(existing_weight)
#                 if existing_weight is None:
#                     existing_weights["{}/{}".format(layer_name, weight_no)] = {shard_no: value}
#                 else:
#                     existing_weights["{}/{}".format(layer_name, weight_no)] = \
#                         existing_weight.update({shard_no: value})
#
#                 with open(os.path.join(final_weights_dir, "{}.json".format(layer_name)), "w") as fq:
#                     json.dump(existing_weights, fq)
#
#     # concatenate arrays
#     # concatenate_arrays(model_name)
#
#
# def concatenate_arrays(model_name):
#     final_weights_dir = os.path.join(model_name, "final_weights")
#     final_weights_dir2 = os.path.join(model_name, "final_weights2")
#     os.makedirs(final_weights_dir2, exist_ok=True)
#     filepaths = glob.glob(os.path.join(final_weights_dir, "*"))
#
#     for filepath in filepaths:
#         print("Processing:", filepath)
#         with open(filepath, "r") as f:
#             weights = json.load(f)
#             for key, value in weights.items():
#                 if type(value) is dict:
#                     if len(value.keys()) > 1:
#                         od = collections.OrderedDict(sorted(value.items()))
#                         stacked_weights = np.concatenate(list(od.values()), axis=-1)
#                         weights[key] = stacked_weights.tolist()
#                     else:
#                         weights[key] = list(value.values())[0]
#
#         with open(os.path.join(final_weights_dir2, os.path.basename(filepath)), "w") as f:
#             json.dump(weights, f)
#
#
# def validate_merged_shards(model_name):
#     final_weights_dir = os.path.join(model_name, "final_weights")
#     weights_dir = os.path.join(model_name, "weights")
#
#     for filepath in glob.glob("{}/*".format(weights_dir)):
#         # load both files
#         filename = os.path.basename(filepath)
#         # print("---------")
#         # print("Filename:", filename)
#         weights_dict = {}
#         if os.path.exists(os.path.join(weights_dir, filename)):
#             with open(os.path.join(weights_dir, filename), "r") as f:
#                 all_weights = json.load(f)
#                 for key, value in all_weights.items():
#                     # print("Original array shape:", np.array(value).shape)
#                     weights_dict[key] = [value]
#
#         if os.path.exists(os.path.join(final_weights_dir, filename)):
#             with open(os.path.join(final_weights_dir, filename), "r") as f:
#                 all_weights = json.load(f)
#                 for key, value in all_weights.items():
#                     # print("Merged array shape:", np.array(value).shape)
#                     weights_dict[key].append(value)
#
#         # print(weights_dict)
#         for key, value in weights_dict.items():
#             # print(key)
#             if np.array_equal(value[0], value[1]):
#                 # print("Equal")
#                 pass
#             else:
#                 print(os.path.basename(filename))
#                 print("Not")
