import json
import os.path
import re
import unicodedata

import numpy as np
import tensorflow as tf


def get_keys(filepaths):
    for filepath in filepaths:
        with open(filepath, "r") as f:
            print(os.path.basename(filepath), ":", list(json.load(f).keys()))


def search_key(key, filepaths):
    for filepath in filepaths:
        with open(filepath, "r") as f:
            weights = json.load(f)
            keys = list(weights.keys())
            for key1 in keys:
                if key in key1:
                    print("Filename", os.path.basename(filepath))
                    print("Shape:", np.array(weights[key1]).nbytes)


def get_weights_by_key(key, filepaths):
    for filepath in filepaths:
        with open(filepath, "r") as f:
            weights = json.load(f)
            keys = list(weights.keys())
            for key1 in keys:
                if key in key1:
                    return weights[key1]
    return None


def compare_weights(model, model1):
    for layer in model.layers:
        print("Layer:", layer.name)
        for index, weight in enumerate(layer.weights):
            weight1 = model1.get_layer(layer.name).get_weights()[index]

            if np.array_equal(weight, weight1):
                # print("Yes")
                pass
            else:
                print("No")
                return False

    return True


def compare_predictions(model, model1):
    img_path = 'elephant.webp'
    img = tf.keras.preprocessing.image.load_img(img_path, target_size=(model1.input_shape[1], model1.input_shape[2]))
    x = tf.keras.preprocessing.image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = tf.keras.applications.xception.preprocess_input(x)

    preds = model.predict(x)
    print('Predicted:', tf.keras.applications.xception.decode_predictions(preds, top=3)[0])

    preds1 = model1.predict(x)
    print('Predicted1:', tf.keras.applications.xception.decode_predictions(preds1, top=3)[0])


def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


if __name__ == '__main__':
    # get_keys(glob.glob("../xception/weights/*"))
    # print(search_key("block14_sepconv2", glob.glob("../xception/final_weights/*")))
    # print(search_key("block14_sepconv1/weight:2", glob.glob("../xception/shards/*")))

    # print(get_weights_by_key("block14_sepconv1/weight:2",  glob.glob("../xception/shards/*")))
    # print(np.array(get_weights_by_key("block14_sepconv2/weight:2",
    #                                   glob.glob("../xception/final_weights/*"))["1"]).shape)
    # print(np.array(get_weights_by_key("block14_sepconv2/weight:2",
    #                                   glob.glob("../xception/final_weights/*"))["2"]).shape)

    # print(np.fmin(get_weights_by_key("block14_sepconv2/weight:2",  glob.glob("../xception/final_weights/*")),
    #                      get_weights_by_key("block14_sepconv2/weight:2",  glob.glob("../xception/weights/*"))))
    pass
