# smoke code with simulating data and email notification
from flask_restx import Namespace, Resource, Api
from flask import Flask
import random
import datetime
import sqlite3
import time
import threading

from endpoints.eamilnoti import *

app = Flask(__name__)
api = Api(app)
api = Namespace('Smoke', description='smoke endpoint')


# endpoint to return the smoke once
@api.route('/Smoke', doc={"description": "Get the Smoke Percentage"})
class HelloWorld(Resource):
    def get(self):
        smoke = random.randint(0, 100)

        return {'smoke': smoke}

# endpoint to get the last 10 record from the database
@api.route('/Smoke10', doc={"description": "Get the last 10 records"})
class HelloWorld(Resource):
    def get(self):
        nums = ["72", "1", "54", "23", "12", "45", "67", "89", "90", "100"]

        return {'smoke': nums}

# endpoint to reset notifications
@api.route('/Reset', doc={"description": "Reset the smoke notifications"})
class HelloWorld(Resource):
    def get(self):
        return {'message': 'Notifications reset successfully'}

