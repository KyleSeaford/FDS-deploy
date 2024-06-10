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
            temp = random.randint(0, 100)

            print("Temperature: ", temp, "sent", sent)

            if temp > 50 and sent == False:
                print("Temperature is above 50 degrees")
                send(f"A Temperature of 50°C+ has been detected.\nFailure to take immediate action may result in significant damage to property and wildlife.\nPlease navigate to your dashboard and take further action. *link to dashboard*", "URGENT: FireGuardPro Temperature Alert")
                sent = True

            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            conn = sqlite3.connect('sensordata.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Temp (Temp, Time) VALUES (?, ?)', (temp, current_time))
            conn.commit()
            conn.close()

            time.sleep(5)

    def stop(self):        
        self._stop_event.set()
        print("Data addition stopped")

data_adder = DataAdder()
data_adder.start()

# endpoint to return the temperature once
@api.route('/Temp', doc={"description": "Get the temperature"})
class HelloWorld(Resource):
    def get(self):
        # get last values from the database
        conn = sqlite3.connect('sensordata.db')
        cursor = conn.cursor()
        cursor.execute('SELECT `temp` FROM `Temp` ORDER BY `Time` DESC LIMIT 1')
        temps = cursor.fetchall()  
        conn.close()
        if len(temps) > 0:
            temp = temps[0][0]
        else:
            temp = "No data available"

        return {'temp': temp}

# endpoint to get the last 10 record from the database
@api.route('/Temp10', doc={"description": "Get the last 10 records"})
class HelloWorld(Resource):
    def get(self):
        # get last values from the database
        conn = sqlite3.connect('sensordata.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM `Temp` ORDER BY `Time` DESC LIMIT 10')
        temps = cursor.fetchall()  
        conn.close()

        return {'temp': temps}

# endpoint to reset notifications
@api.route('/Reset', doc={"description": "Reset the temperature notifications"})
class HelloWorld(Resource):
    def get(self):
        global sent
        sent = False
        return {'message': 'Notifications reset successfully'}

# endpoint to stop the temperature data addition
@api.route('/Stop', doc={"description": "Stop the temperature data addition"})
class Stop(Resource):
    def get(self):
        data_adder.stop()
        data_adder.join()  # Ensure the thread has finished
        return {'message': 'Temperature data addition stopped successfully'}
