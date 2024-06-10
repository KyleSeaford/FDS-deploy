# MARK: FlaskTest.py server file
# Description: This file is a test file for the Flask server. It will be used to show the dashboard 

from flask import Flask, render_template, jsonify
import datetime
import requests
from flask_cors import CORS
import json

from location import get_location
from weather import *

app = Flask(__name__)
CORS(app)  # Allow CORS for all routes


def get_public_ip_address():
    response = requests.get('https://httpbin.org/ip')
    return response.json()['origin']


# MARK: App routes dashboard
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/location')
def Location():
    return jsonify({'location': get_location()})

@app.route('/weather')
def weather():
    return jsonify({'weather': get_conditions_all()})

@app.route('/conditions')
def con():
    return jsonify({'conditions': get_conditions()})

@app.route('/windspeed')
def wind():
    return jsonify({'windspeed': get_windspeed()})

@app.route('/ip')
def ip():
    return jsonify({'Public ip': get_public_ip_address()})

@app.route('/current_date')
def current_date():
    return jsonify({'current_date': datetime.datetime.now().strftime("%Y-%m-%d")})

@app.route('/current_time')
def current_time():
    return jsonify({'current_time': datetime.datetime.now().strftime("%H:%M:%S")})


# add the addresses of the units for the different zones
zone1_addresses_full = ['192.168.127.133', '192.168.127.134']
zone2_addresses_full = ['']
zone3_addresses_full = ['']
zone4_addresses_full = ['']
zone5_addresses_full = ['']
zone6_addresses_full = ['']
zone7_addresses_full = ['']
zone8_addresses_full = ['']
zone9_addresses_full = ['']
zone10_addresses_full = ['']
zone11_addresses_full = ['']
zone12_addresses_full = ['']
zone13_addresses_full = ['']

# fill in the addresses for all the units
unitaddresses_full = [address for address in zone1_addresses_full + zone2_addresses_full + zone3_addresses_full + zone4_addresses_full + zone5_addresses_full + zone6_addresses_full + zone7_addresses_full + zone8_addresses_full + zone9_addresses_full + zone10_addresses_full + zone11_addresses_full + zone12_addresses_full + zone13_addresses_full if address]

# MARK: Reset all units
@app.route('/notifications')
def notifications():
    for unit in unitaddresses_full:
        unitaddress_temp = 'http://' + unit + ':5500/Temp/Reset'
        unitaddress_smoke = 'http://' + unit + ':5500/smoke/Reset'
        unitaddress_rain = 'http://' + unit + ':5500/rain/Reset'
        # reset the temperature, smoke and rain data
        requests.get(unitaddress_temp)
        requests.get(unitaddress_smoke)
        requests.get(unitaddress_rain)
        # Make a request to the unit address 
        
    # Return an empty response
    return '', 204

# MARK: Temp data
@app.route('/temp/<int:unit>')
def temp_int(unit):
    return jsonify({'error': 'unit not found'})

@app.route('/temp/<unit>')
def temp_string(unit):
    # get the temperature from the unit
    unitaddress = 'http://' + unit + ':5500/Temp/Temp'
    response = requests.get(unitaddress)
    return json.loads(response.text)
  
@app.route('/tempdata')
def temps():

    temps = []

    unitaddresses = unitaddresses_full
    for unit in unitaddresses:
        unitaddress = 'http://' + unit + ':5500/Temp/Temp'
        response = requests.get(unitaddress)

        temp_data = json.loads(response.text)
        temps.append({'unit': unit, 'temp': temp_data['temp']})

    return jsonify(temps)

# MARK: Smoke data
@app.route('/smoke/<int:unit>')
def smoke_int(unit):
    return jsonify({'error': 'unit not found'})

@app.route('/smoke/<unit>')
def smoke_string(unit):
    # get the smoke from the unit
    unitaddress = 'http://' + unit + ':5500/smoke/smoke'
    response = requests.get(unitaddress)
    return json.loads(response.text)

@app.route('/smokedata')
def smokes():

    smokes = []

    unitaddresses = unitaddresses_full
    for unit in unitaddresses:
        unitaddress = 'http://' + unit + ':5500/smoke/smoke'
        response = requests.get(unitaddress)

        smoke_data = json.loads(response.text)
        smokes.append({'unit': unit, 'smoke': smoke_data['smoke']})

    return jsonify(smokes)

# MARK: Rain data
@app.route('/rain/<int:unit>')
def rain_int(unit):
    return jsonify({'error': 'unit not found'})

@app.route('/rain/<unit>')
def rain_string(unit):
    # get the smoke from the unit
    unitaddress = 'http://' + unit + ':5500/rain/rain'
    response = requests.get(unitaddress)
    return json.loads(response.text)
  
@app.route('/raindata')
def rains():

    rains = []

    unitaddresses = unitaddresses_full
    for unit in unitaddresses:
        unitaddress = 'http://' + unit + ':5500/rain/rain'
        response = requests.get(unitaddress)

        rain_data = json.loads(response.text)
        rains.append({'unit': unit, 'rain': rain_data['rains']})

    return jsonify(rains)

# MARK: Camera data
@app.route('/camera/<int:unit>')
def camera_int(unit):
    return jsonify({'error': 'unit not found'})

@app.route('/camera/<unit>')
def camera_string(unit):
    # get the smoke from the unit
    unitaddress = 'http://' + unit + ':5500/camera/camera'
    return jsonify(unitaddress)


@app.route('/cameradata')
def cameras():

    cameras = []

    unitaddresses = unitaddresses_full
    for unit in unitaddresses:
        unitaddress = 'http://' + unit + ':5500/camera/camera'

        cameras.append({'unit': unit, 'camera': unitaddress})
    
    return jsonify(cameras)

# MARK: zone 1 app routes
@app.route('/zone1tempdata')
def zone1temps():

    temps = []

    unitaddresses = zone1_addresses_full
    for unit in unitaddresses:
        unitaddress = 'http://' + unit + ':5500/Temp/Temp'
        response = requests.get(unitaddress)

        temp_data = json.loads(response.text)
        temps.append({'unit': unit, 'temp': temp_data['temp']})

    return jsonify(temps)

@app.route('/zone1temp10data')
def zone1temps10():
    
        temps = []
    
        unitaddresses = zone1_addresses_full
        for unit in unitaddresses:
            unitaddress = 'http://' + unit + ':5500/Temp/Temp10'
            response = requests.get(unitaddress)
    
            temp_data = json.loads(response.text)
            temps.append({'unit': unit, 'temp': temp_data['temp']})
    
        return jsonify(temps[:10])

@app.route('/zone1smokedata')
def zone1smokes():

    smokes = []

    unitaddresses = zone1_addresses_full
    for unit in unitaddresses:
        unitaddress = 'http://' + unit + ':5500/smoke/Smoke'
        response = requests.get(unitaddress)

        smoke_data = json.loads(response.text)
        smokes.append({'unit': unit, 'smoke': smoke_data['smoke']})

    return jsonify(smokes)

@app.route('/zone1smoke10data')
def zone1smokes10():

    smokes = []

    unitaddresses = zone1_addresses_full
    for unit in unitaddresses:
        unitaddress = 'http://' + unit + ':5500/smoke/Smoke10'
        response = requests.get(unitaddress)

        smoke_data = json.loads(response.text)
        smokes.append({'unit': unit, 'smoke': smoke_data['smoke']})

    return jsonify(smokes[:10])


@app.route('/zone1raindata')
def zone1rains():

    rains = []

    unitaddresses = zone1_addresses_full
    for unit in unitaddresses:
        unitaddress = 'http://' + unit + ':5500/rain/Rain'
        response = requests.get(unitaddress)

        rain_data = json.loads(response.text)
        rains.append({'unit': unit, 'rain': rain_data['rain']})

    return jsonify(rains)

@app.route('/zone1rain10data')
def zone1rains10():

    rains = []

    unitaddresses = zone1_addresses_full
    for unit in unitaddresses:
        unitaddress = 'http://' + unit + ':5500/rain/Rain10'
        response = requests.get(unitaddress)

        rain_data = json.loads(response.text)
        rains.append({'unit': unit, 'rain': rain_data['rain']})

    return jsonify(rains[:10])


@app.route('/zone1cameradata')
def zone1cameras():
    cameras = []

    # Generate a new list of unit addresses on each request
    unitaddresses = zone1_addresses_full
    for unit in unitaddresses:
        unitaddress = 'http://' + unit + ':5500/camera/camera'

        cameras.append({'unit': unit, 'camera': unitaddress})
    
    return jsonify(cameras)

# MARK: zone 2 app routes
# in the production version, the code for zone 2 will be similar to the code for zone 1
# fill in the addresses of the units in zone 2
zone2_addresses_full = ['']



# MARK: ip and debug mode
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)