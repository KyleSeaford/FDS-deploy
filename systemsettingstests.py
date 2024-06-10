# Unit tests for the systemsettings endpoint
import unittest
import tempfile
import sqlite3
import json
import os
from endpoints.systemsettings import systemsettings
from endpoints.systemsettings import api as namespaceSystemSettings
from flask import Flask
from flask_restx import Api
from flask_cors import CORS

class SystemSettingsTestCase(unittest.TestCase):
    def setUp(self):
        """Set up for unit tests, function is executed before tests begin"""

        # Create a temporary file to use as a test database
        self.db_fd, self.db_path = tempfile.mkstemp()

        # Initialize the database with the test schema and data
        self.init_db()

        # Override the database path in the SystemSettings class
        systemsettings(self.db_path)

        # Create the Flask test client
        self.app = Flask(__name__)
        CORS(self.app)  # Allow CORS for all routes
        self.api = Api(self.app, version='1.0', title='PI Firmware', description='Pi Side Firmware Controller')
        self.api.add_namespace(namespaceSystemSettings, path='/systemsettings')
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def tearDown(self):
        """Tear down for unit tests, function is executed after tests have been executed"""

        # Close and remove the temporary database
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def init_db(self):
        """Initialize the database with the test schema and data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE Settings (Sname TEXT, Svalue TEXT)')
        cursor.execute('INSERT INTO Settings (Sname, Svalue) VALUES (?, ?)', ('Setting1', 'Value1'))
        cursor.execute('INSERT INTO Settings (Sname, Svalue) VALUES (?, ?)', ('Setting2', 'Value2'))
        conn.commit()
        conn.close()

    def test_get_settings(self):
        """Test confirms that GET /systemsettings/Settings will return a list of all the system settings"""

        # Arrange 
        expected_result = [
            {'Name': 'Setting1', 'Value': 'Value1'},
            {'Name': 'Setting2', 'Value': 'Value2'}
        ]

        # Act
        response = self.client.get('/systemsettings/Settings') # Make a GET request to the /systemsettings/Settings endpoint

        # Assert
        self.assertEqual(response.status_code, 200) # Check that the response status code is 200 OK
        actual_result = json.loads(response.data) # Parse the JSON response        
        self.assertEqual(actual_result, expected_result) # Check that the response contains the expected data

    def test_get_setting(self):
        """Test confirms that GET /systemsettings/Setting/ will return a setting value"""

        # Arrange
        expected_result = 'Value1'

        # Act
        response = self.client.get('/systemsettings/Setting/Setting1') # Make a GET request to the /systemsettings/Settings endpoint
        
        # Assert
        self.assertEqual(response.status_code, 200) # Check that the response status code is 200 OK
        actual_result = json.loads(response.data) # Parse the JSON response
        self.assertEqual(actual_result, expected_result) # Check that the response contains the expected data

    def test_get_setting_bad_setting_name(self):
        """Test confirms that GET /systemsettings/Setting/ will return 400 when the setting name does not exisit"""

        # Arrange
        sname = 'Bad_Setting_Name'
        expected_message = f'Invalid setting name. {sname} does not exisit'

        # Act
        response = self.client.get(f'/systemsettings/Setting/{sname}') # Make a GET request to the /systemsettings/Settings endpoint
        
        # Assert
        self.assertEqual(response.status_code, 400) # Check that the response status code is 400 BAD
        self.assertEqual(response.status, '400 BAD REQUEST') # Check the response status message        
        response_json = response.get_json() # Extract the JSON data from the response    
        self.assertIn('message', response_json) # Ensure the 'message' key is in the response
        self.assertEqual(response_json['message'], expected_message) # Check that the response message contains the expected message
    
    def test_post_setting(self):
        """Test confirms that POST /systemsettings/Setting will add a new setting"""
        
        # Arrange 
        expected_result = [
            {'Name': 'Setting1', 'Value': 'Value1'},
            {'Name': 'Setting2', 'Value': 'Value2'},
            {'Name': 'Setting3', 'Value': 'Value3'}
        ]

        # Act
        response = self.client.post('/systemsettings/Setting', json={"Name":"Setting3", "Value":"Value3"}) # Make a POST request to the /systemsettings/Setting endpoint

        # Assert
        print("post response", response)
        self.assertEqual(response.status_code, 201) # Check that the response status code is 201 CREATED
        response = self.client.get('/systemsettings/Settings') # Make a GET request to the /systemsettings/Settings endpoint to get all settings which should include the new setting
        actual_result = json.loads(response.data) # Parse the JSON response        
        self.assertEqual(actual_result, expected_result) # Check that the response contains the old settings and the new setting
    
    def test_post_setting_no_post_data(self):
        """Test confirms that POST /systemsettings/Setting will return 415 when post request does not contain the json data"""
        
        # Arrange 

        # Act
        response = self.client.post('/systemsettings/Setting') # Make a POST request to the /systemsettings/Setting endpoint without json data

        # Assert
        self.assertEqual(response.status_code, 400) # Check that the response status code is 415
        self.assertEqual(response.status, '400 BAD REQUEST') # Check the response status message   

    def test_post_setting_bad_post_data(self):
        """Test confirms that POST /systemsettings/Setting will return 415 when post request contain bad json data"""
        
        # Arrange 
        badJsonData = {'Bad':'bob1'} # Json data should include Name and Value
        expected_message = f'Input payload validation failed'

        # Act
        response = self.client.post('/systemsettings/Setting', json=badJsonData) # Make a POST request to the /systemsettings/Setting endpoint with bad json data

        # Assert
        self.assertEqual(response.status_code, 400) # Check that the response status code is 400
        self.assertEqual(response.status, '400 BAD REQUEST') # Check the response status message        
        response_json = response.get_json() # Extract the JSON data from the response    
        self.assertIn('message', response_json) # Ensure the 'message' key is in the response
        self.assertEqual(response_json['message'], expected_message) # Check that the response message contains the expected message
    
    def test_post_setting_exists_post_data(self):
        """Test confirms that POST /systemsettings/Setting will return 400 when setting already exists"""
        
        # Arrange 
        badJsonData = {"Name":"Setting1", "Value":"Value10"} # Json data contains an already exisiting setting name
        expected_message = f'Setting Setting1 already exisits'

        # Act
        response = self.client.post('/systemsettings/Setting', json=badJsonData) # Make a POST request to the /systemsettings/Setting endpoint with bad json data

        # Assert
        self.assertEqual(response.status_code, 400) # Check that the response status code is 400
        self.assertEqual(response.status, '400 BAD REQUEST') # Check the response status message        
        response_json = response.get_json() # Extract the JSON data from the response    
        self.assertIn('message', response_json) # Ensure the 'message' key is in the response
        self.assertEqual(response_json['message'], expected_message) # Check that the response message contains the expected message
    
if __name__ == '__main__':
    unittest.main()