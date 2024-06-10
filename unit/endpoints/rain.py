# rain code with simulating data and email notification
from flask_restx import Namespace, Resource, Api
from flask import Flask
import random

from endpoints.eamilnoti import *

app = Flask(__name__)
api = Api(app)
api = Namespace('Rain', description='rain endpoint')

# endpoint to return the rain once
@api.route('/Rain', doc={"description": "Get the Rain Percentage"})
class HelloWorld(Resource):
    def get(self):
        global sent
        rain = random.randint(0, 100)

        return {'rain': rain}

# endpoint to get the last 10 record from the database
@api.route('/Rain10', doc={"description": "Get the last 10 records"})
class HelloWorld(Resource):
    def get(self):
        nums = ["15", "20", "25", "30", "35", "40", "45", "50", "55", "60"]
        return {'rain': nums}
    
# endpoint to reset notifications
@api.route('/Reset', doc={"description": "Reset the rain notifications"})
class HelloWorld(Resource):
    def get(self):
        return {'message': 'Notifications reset successfully'}