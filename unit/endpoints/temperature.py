# temperature code with simulating data and email notification
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
api = Namespace('Temp', description='Temp endpoint')

# endpoint to return the temperature once
@api.route('/Temp', doc={"description": "Get the temperature"})
class HelloWorld(Resource):
    def get(self):
        temp = random.randint(0, 100)

        return {'temp': temp}

# endpoint to get the last 10 record from the database
@api.route('/Temp10', doc={"description": "Get the last 10 records"})
class HelloWorld(Resource):
    def get(self):
        nums = ["72", "1", "54", "23", "12", "45", "67", "89", "90", "100"]

        return {'temp': nums}

# endpoint to reset notifications
@api.route('/Reset', doc={"description": "Reset the temperature notifications"})
class HelloWorld(Resource):
    def get(self):
        return {'message': 'Notifications reset successfully'}
