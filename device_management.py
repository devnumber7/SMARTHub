# device_management.py

import mariadb
import threading
import os
import logging


logging.basicConfig(level=logging.DEBUG)
class DeviceManagement:
    def __init__(self):
        try:
            self.conn = mariadb.connect(
                user=os.environ.get('DB_USER', 'test'),
                password=os.environ.get('DB_PASSWORD', 'SMART'),
                host=os.environ.get('DB_HOST', 'localhost'),
                port=int(os.environ.get('DB_PORT', 3306)),
                database=os.environ.get('DB_NAME', 'SMART')
            )
            logging.debug("Connection to MariaDB Platform successful!")
        except mariadb.Error as e:
            logging.debug(f"Error connecting to MariaDB Platform: {e}")
            self.conn = None


        

    def get_devices(self):
        """
        Retrieves the list of devices from the database.
        Returns a list of dictionaries with 'id' and 'state' keys.
        """
        if self.conn is None:
            return []

        try:
            cur = self.conn.cursor()
            query = "SELECT * FROM test"  # Replace 'test' with your actual table name
            cur.execute(query)
            device_list = []
            for row in cur:
                # Adjust row indices based on your table structure
                device_list.append({'id': str(row[0]), 'state': str(row[1])})
            cur.close()
            logging.debug(f"Devices fetched: {device_list}")
            logging.debug(f"Number of devices: {len(device_list)}")
            
            return device_list
        except mariadb.Error as e:
            logging.debug(f"Error fetching devices: {e}")
            return []
        


    def close_connection(self):
        if self.conn:
            self.conn.close()






