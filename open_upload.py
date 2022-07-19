from flask import request
from flask_json import json_response
from flask import jsonify
import json
from binascii import a2b_base64
from tools.logging import logger
from tools.model import imagePredicition
import os

TEMP_FOLDER = './application_data/input_image'


def constructImage(data):
    logger.debug("Trying to construct image")
    chunks = data.split(',')
    file_data = a2b_base64(chunks[1])
    imgPath = os.path.join(TEMP_FOLDER, 'image.jpeg')
    temp = open(imgPath, 'wb')
    temp.write(file_data)
    temp.close()
    logger.debug("Image constructed, trying to return path")
    return imgPath


# should delete the temp image, untested
def delete_temp_file(tempFile):
    if os.path.exists(tempFile):
        os.remove(tempFile)
    else:
        logger.debug("The file does not exist")


def handle_request():
    logger.debug("Open_Upload called test3")
    if request.method == 'POST':
        jsonData = request.get_json()
        # check if the post has a username
        logger.debug("getting username")
        username_from_user = jsonData['username']
        logger.debug(username_from_user)
        logger.debug("getting file")
        # turn the data into an image
        data = jsonData['file']
        filepath = constructImage(data)
        # all the model names are lower case
        username_from_user = username_from_user.lower()
        # if user does not select file, browser also
        logger.debug("File accepted and being processed")
        logger.debug("Trying to save file")
        # save the file to temp
        # send the image to the prediction
        logger.debug("Sending image to model")
        prediction = imagePredicition(username_from_user, filepath)
        logger.debug(prediction)
        result = str(prediction)
        # delete the file uploaded for testing
        logger.debug("Deleting image used")
        delete_temp_file(filepath)
        # return the prediction to user
        logger.debug("Sending back response")
        return json_response(status=200, message=result)
    elif request.method == 'GET':
        return json_response(status=200, message="Request was a GET, we don't handle those here")

    else:
        return json_response(status=500, message="Could not handle request")