from flask import Flask, jsonify, request
from datetime import datetime
import pandas as pd
import tensorflow as tf
import keras
import numpy as np
from tensorflow.keras.layers import Layer
from keras.preprocessing import image
from keras.models import load_model
from tools.logging import logger
import os

BASE_DIR = "./"
DETECTION_THRESHOLD = .75
VERIFICATION_THRESHOLD = .75


class L1Dist(Layer):
    # Init method - inheritance
    def init(self, **kwargs):
        super().init()

    # Magical shit - similarity calculation
    def call(self, input_embedding, validation_embedding):
        return tf.math.abs(input_embedding - validation_embedding)


def preprocess(file_path):
    # Read in image from file path
    byte_img = tf.io.read_file(file_path)
    # Load in image
    img = tf.io.decode_jpeg(byte_img)
    # Resize image to 100x100x3
    img = tf.image.resize(img, (100, 100))
    # Scale image to be between 0 and 1
    img = img / 255.0
    # Return processed image
    return img


# takes the path from the path passed in and
# then loads the image into the array below
# then we must check what it predicted and return it
def imagePredicition(name, img_path):
    # split together the model name
    model_name = f"{name}.h5"
    model_path = os.path.join(BASE_DIR, 'application_data', 'models', model_name)
    logger.debug(f"Trying to get model {model_name}")
    # check for and grab our model
    if os.path.exists(model_path):
        logger.debug(f"got model {model_name}")
        model = tf.keras.models.load_model(model_path,
                                           custom_objects={'L1Dist': L1Dist,
                                                           'BinaerCrossentropy': tf.losses.BinaryCrossentropy})
    # Build results array
    named_folder = f"{name}_verify"
    results = []
    for image in os.listdir(os.path.join(BASE_DIR, 'application_data', 'verification_images', named_folder)):
        input_img = preprocess(img_path)
        validation_img = preprocess(
            os.path.join(BASE_DIR, 'application_data', 'verification_images', named_folder, image))
        result = model.predict(list(np.expand_dims([input_img, validation_img], axis=1)))
        results.append(result)

    # Detection Threshold: Metric above which a prediction is considered positive
    detection = np.sum(np.array(results) > DETECTION_THRESHOLD)

    # Verification Threshold: Proportion of positive predictions / total positive samples
    verification = detection / len(os.listdir(os.path.join('application_data', 'verification_images', named_folder)))
    verified = verification > VERIFICATION_THRESHOLD

    return verified
