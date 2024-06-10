# main entry point for the firmware. It is for the units
from flask import Flask
from flask_restx import Api
from flask_cors import CORS

from endpoints.temperature import api as namespaceTemperature
from endpoints.smoke import api as namespaceSmoke
from endpoints.rain import api as namespaceRain
from endpoints.camera import api as namespaceCamera
from endpoints.systemsettings import api as namespaceSystemSettings
from endpoints.stop import api as namespaceStop 

app = Flask(__name__)
CORS(app)  # Allow CORS for all routes
api = Api(app, version='1.0', title='Unit Firmware', description='Unit Side Firmware Controller API')

api.add_namespace(namespaceTemperature, path='/Temp')
api.add_namespace(namespaceSmoke, path='/smoke')
api.add_namespace(namespaceRain, path='/rain')
api.add_namespace(namespaceCamera, path='/camera')
api.add_namespace(namespaceSystemSettings, path='/systemsettings')
api.add_namespace(namespaceStop, path='/stop')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500, debug=False)
