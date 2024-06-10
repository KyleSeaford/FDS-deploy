# rain code with simulating data and email notification
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
api = Namespace('Rain', description='rain endpoint')

# Variable to keep track of whether a notification has been sent
sent = False

# Use a separate thread to run the data addition function
class DataAdder(threading.Thread):
    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()

    def run(self):
        global sent
        while not self._stop_event.is_set():
            rain = random.randint(0, 100)

            print("Rain: ", rain, "sent", sent)
            # sends email if rain is above 20 and a notification has not been sent
            if rain > 20 and sent == False:
                print("Rain Percentage is above 20%")
                send(f"A Rain Percentage of 20%+ has been detected.\nFailure to take immediate action may result in significant damage to property and wildlife.\nPlease navigate to your dashboard and take further action. *link to dashboard*", "URGENT: FireGuardPro Rain Alert")
                sent = True

            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            conn = sqlite3.connect('sensordata.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Rain (Rain, Time) VALUES (?, ?)', (rain, current_time))
            conn.commit()
            conn.close()

            time.sleep(5)

    def stop(self):        
        self._stop_event.set()
        print("Data addition stopped")

data_adder = DataAdder()
data_adder.start()

# endpoint to return the rain once
@api.route('/Rain', doc={"description": "Get the Rain Percentage"})
class HelloWorld(Resource):
    def get(self):
        # get last values from the database
        conn = sqlite3.connect('sensordata.db')
        cursor = conn.cursor()
        cursor.execute('SELECT `rain` FROM `Rain` ORDER BY `Time` DESC LIMIT 1')
        rains = cursor.fetchall()
        conn.close()
        if len(rains) > 0:
            rain = rains[0][0]
        else:
            rain = "No data available"

        return {'rain': rain}

# endpoint to get the last 10 record from the database
@api.route('/Rain10', doc={"description": "Get the last 10 records"})
class HelloWorld(Resource):
    def get(self):
        # get last values from the database
        conn = sqlite3.connect('sensordata.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM `Rain` ORDER BY `Time` DESC LIMIT 10')
        rains = cursor.fetchall()
        conn.close()

        return {'rain': rains}
    
# endpoint to reset notifications
@api.route('/Reset', doc={"description": "Reset the rain notifications"})
class HelloWorld(Resource):
    def get(self):
        global sent
        sent = False
        return {'message': 'Notifications reset successfully'}

# endpoint to stop the rain data addition
@api.route('/Stop', doc={"description": "Stop the rain data addition"})
class Stop(Resource):
    def get(self):
        data_adder.stop()
        data_adder.join() # Ensure the thread has finished
        return {'message': 'Rain Data addition stopped successfully'}
