# holds the system settings endpoint which allows the user to add, update, delete and get system settings
from flask_restx import Namespace, Resource, Api, fields, reqparse
from flask import Flask, request
import platform
from database_extensions import database_extensions

app = Flask(__name__)
api = Api(app)
api = Namespace('SystemSettings', description='System Settings Endpoint')

databaseName = '../Pi/sensordata.db'
class systemsettings():    
    def __init__(self, db = 'sensordata.db'):
        global databaseName
        databaseName = db

SettingName = 'Name'
SettingValue = 'Value'

parserAdd = reqparse.RequestParser()
parserAdd.add_argument(SettingName, type=str, help='Setting Name', required=True)
parserAdd.add_argument(SettingValue, type=str, help='Setting Value', required=True)

parserUpdate = reqparse.RequestParser()
parserUpdate.add_argument(SettingValue, type=str, help='Setting Value', required=True)

### Route /Settings ########################################   
@api.route('/Settings', doc={"description": "Get all settings"})
class GetSettings(Resource):
    def get(self):
        result = []
        for record in database_extensions(databaseName).fetchAll('SELECT Sname, Svalue FROM `Settings` ORDER BY Sname ASC'):
            result.append({'Name' : record[0], 'Value': record[1]})
        return result

### Route /Setting/<string:sname> ########################################     
@api.route('/Setting/<string:sname>', doc={"description": "Get one setting value"})
@api.param('sname', 'Setting Name')
class GetSetting(Resource):
    def get(self, sname):
        try:
            return database_extensions(databaseName).fetchSingleValue(f"SELECT Svalue FROM `Settings` where sname='{sname}' limit 1")
        except:
            return {'message': f'Invalid setting name. {sname} does not exisit'}, 400
        
    @api.doc(parser=parserUpdate)
    def put(self, sname):
        args = parserUpdate.parse_args()
        svalue = args[SettingValue]

        db = database_extensions(databaseName)
        recordExisits = db.fetchSingleValue(f"select count(*) from `Settings` where Sname='{sname}'")
        if recordExisits == 1:
            return {'message': f'Setting {sname} dose not exisit'}, 400
        
        db.execute(f"update `Settings` set Svalue='{svalue}' where Sname='{sname}'");

        return {'message': 'Setting successfully updated'}, 200
    

@api.route('/Setting/delete', doc={"description": "Delete a setting"})
class DeleteSetting(Resource):
    @api.doc(parser=parserAdd)
    def post(self):
        args = parserAdd.parse_args()
        sname = args['Name']
        
        db = database_extensions(databaseName)
        recordExists = db.fetchSingleValue(f"SELECT COUNT(*) FROM `Settings` WHERE Sname='{sname}'")
        if recordExists == 0:
            return {'message': f'Setting {sname} does not exist'}, 400
        
        db.execute(f"DELETE FROM `Settings` WHERE Sname='{sname}'")
        return {'message': 'Setting successfully deleted'}, 200

### Route /Setting ########################################         
@api.route('/Setting', doc={"description": "Add a new setting"})
class AddSetting(Resource):
    @api.doc(parser=parserAdd)
    def post(self):
        args = parserAdd.parse_args()
        sname = args[SettingName]
        svalue = args[SettingValue]
        
        db = database_extensions(databaseName)
        recordExisits = db.fetchSingleValue(f"select count(*) from `Settings` where Sname='{sname}'")
        if recordExisits == 1:
            return {'message': f'Setting {sname} already exisits'}, 400
        
        db.execute(f"INSERT INTO `Settings` (Sname, Svalue) VALUES ('{sname}', '{svalue}')")
        return {'message': 'Setting added successfully'}, 201
    
def get_system_name():
    system_name = platform.system()
    return system_name

@api.route('/Setting/systemName', doc={"description": "get system name"})
class HelloWorld(Resource):
    def get(self):
        systemName = get_system_name()
        return {'system name': systemName}