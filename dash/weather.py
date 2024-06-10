from flask import Flask, jsonify
from flask_cors import CORS
import requests
import urllib.request
import json

app = Flask(__name__)
CORS(app)  # Allow CORS for all routes

def get_location():
    response_ip = requests.get('https://httpbin.org/ip')
    ip = response_ip.json()['origin']
    response_location = requests.get(f'http://ip-api.com/json/{ip}')
    location_data = response_location.json()
    return location_data['city']


def get_conditions_all():
    address = get_location()
    response = urllib.request.urlopen(f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{address}/today?unitGroup=metric&include=current&key=PCL8VTTZCDPPNRMWBPUGY2DFQ&contentType=json")
    weather_data = json.loads(response.read().decode('utf-8'))
    # Extract current conditions
    current_conditions = weather_data['currentConditions']

    return current_conditions


def get_conditions():
    address = get_location()
    response = urllib.request.urlopen(f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{address}/today?unitGroup=metric&include=current&key=PCL8VTTZCDPPNRMWBPUGY2DFQ&contentType=json")
    weather_data = json.loads(response.read().decode('utf-8'))
    
    # Extract current conditions
    current_conditions = weather_data['currentConditions']
    
    conditions = current_conditions['conditions']

    return conditions

def get_windspeed():
    address = get_location()
    response = urllib.request.urlopen(f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{address}/today?unitGroup=metric&include=current&key=PCL8VTTZCDPPNRMWBPUGY2DFQ&contentType=json")
    weather_data = json.loads(response.read().decode('utf-8'))
    
    # Extract current conditions
    current_conditions = weather_data['currentConditions']

    windspeed = current_conditions['windspeed']

    return windspeed


