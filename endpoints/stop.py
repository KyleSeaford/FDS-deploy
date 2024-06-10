# code for the emergency stop endpoint
import os
from flask_restx import Namespace, Resource

api = Namespace('STOP', description='EMERGENCY STOP')

@api.route('/stop', doc={"description": "THIS WILL STOP ALL PYTHON PROCESSES, USE WITH CAUTION"})
class StopPython(Resource):
    def get(self):
        os.system('taskkill /F /IM python.exe /T')
        return 'All Python processes stopped'