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
            smoke = random.randint(0, 100)

            print("Smoke: ", smoke, "sent", sent)
            # sends email if smoke is above 80 and a notification has not been sent
            if smoke > 80 and sent == False:
                print("Smoke Percentage is above 80%")
                send(f"A smoke Percentage of 80%+ has been detected.\nFailure to take immediate action may result in significant damage to property and wildlife.\nPlease navigate to your dashboard and take further action. *link to dashboard*", "URGENT: FireGuardPro Smoke Alert")
                sent = True

            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            conn = sqlite3.connect('sensordata.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Smoke (Smoke, Time) VALUES (?, ?)', (smoke, current_time))
            conn.commit()
            conn.close()

            time.sleep(5)

    def stop(self):        
        self._stop_event.set()
        print("Data addition stopped")

data_adder = DataAdder()
data_adder.start()

# endpoint to return the smoke once
@api.route('/Smoke', doc={"description": "Get the Smoke Percentage"})
class HelloWorld(Resource):
    def get(self):
        # get last values from the database
        conn = sqlite3.connect('sensordata.db')
        cursor = conn.cursor()
        cursor.execute('SELECT `smoke` FROM `Smoke` ORDER BY `Time` DESC LIMIT 1')
        smokes = cursor.fetchall()  
        conn.close()
        if len(smokes) > 0:
            smoke = smokes[0][0]
        else:
            smoke = "No data available"

        return {'smoke': smoke}

# endpoint to get the last 10 record from the database
@api.route('/Smoke10', doc={"description": "Get the last 10 records"})
class HelloWorld(Resource):
    def get(self):
        # get last values from the database
        conn = sqlite3.connect('sensordata.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM `Smoke` ORDER BY `Time` DESC LIMIT 10')
        smokes = cursor.fetchall()  
        conn.close()

        return {'smoke': smokes}

# endpoint to reset notifications
@api.route('/Reset', doc={"description": "Reset the smoke notifications"})
class HelloWorld(Resource):
    def get(self):
        global sent
        sent = False
        return {'message': 'Notifications reset successfully'}


# endpoint to stop the smoke data addition
@api.route('/Stop', doc={"description": "Stop the smoke data addition"})
class Stop(Resource):
    def get(self):
        data_adder.stop()
        data_adder.join()  # Ensure the thread has finished
        return {'message': 'Smoke data addition stopped successfully'}
