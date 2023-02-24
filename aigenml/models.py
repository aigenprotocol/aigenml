from tensorflow import keras


def get_text_classification_model():
    max_features = 20000
    embedding_dim = 128

    # A integer input for vocab indices.
    inputs = keras.Input(shape=(None,), dtype="int64")

    # Next, we add a layer to map those vocab indices into a space of dimensionality
    # 'embedding_dim'.
    x = keras.layers.Embedding(max_features, embedding_dim)(inputs)
    x = keras.layers.Dropout(0.5)(x)

    # Conv1D + global max pooling
    x = keras.layers.Conv1D(128, 7, padding="valid", activation="relu", strides=3)(x)
    x = keras.layers.Conv1D(128, 7, padding="valid", activation="relu", strides=3)(x)
    x = keras.layers.GlobalMaxPooling1D()(x)

    # We add a vanilla hidden layer:
    x = keras.layers.Dense(128, activation="relu")(x)
    x = keras.layers.Dropout(0.5)(x)

    # We project onto a single unit output layer, and squash it with a sigmoid:
    predictions = keras.layers.Dense(1, activation="sigmoid", name="predictions")(x)

    model = keras.Model(inputs, predictions)

    # Compile the model with binary crossentropy loss and an adam optimizer.
    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

    return model


def get_dense3_model():
    model = keras.Sequential()
    model.add(keras.layers.Dense(12, input_shape=(8,), activation='relu'))
    model.add(keras.layers.Dense(8, activation='relu'))
    model.add(keras.layers.Dense(1, activation='sigmoid'))
    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
    return model


def get_keras_model(name):
    if name == "resnet50":
        model = keras.applications.ResNet50(
            weights="/Users/apple/Downloads/resnet50_weights_tf_dim_ordering_tf_kernels.h5")
    elif name == "vgg16":
        model = keras.applications.VGG16(weights="imagenet")
    elif name == "xception":
        model = keras.applications.Xception(
            weights="/Users/apple/Downloads/xception_weights_tf_dim_ordering_tf_kernels.h5")
    elif name == "mobilenet":
        model = keras.applications.MobileNet(weights="/Users/apple/Downloads/mobilenet_1_0_224_tf.h5")
    elif name == "dense3":
        model = get_dense3_model()
    elif name == "text_classification":
        model = get_text_classification_model()
    else:
        model = None

    return model
