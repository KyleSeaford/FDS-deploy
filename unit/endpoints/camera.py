# camera code with simulating imgs, on a real unit this would be replaced with a camera module and a function to take a photo
# img will just be for visualizing on the dashboard
from flask import send_file
from flask_restx import Namespace, Resource
import random
import os

api = Namespace('Camera', description='camera endpoint')


@api.route('/camera', doc={"description": "take photo on camera"})
class HelloWorld(Resource):
    def get(self):
        # list all images in the directory
        # change image_dir to the directory where the images are stored
        image_dir = "/home/harry/FDS/Pi/endpoints/cameraImgs/"
        images = os.listdir(image_dir)
        random_image = random.choice(images)
        image_path = os.path.join(image_dir, random_image)
        return send_file(image_path, mimetype='image/jpeg')