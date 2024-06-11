import requests

def get_location():
    response = requests.get('http://ip-api.com/json/')
    data = response.json()
    return data['city']