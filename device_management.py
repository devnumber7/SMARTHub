# device_management.py

import mariadb
import os
import logging

logging.basicConfig(level=logging.DEBUG)

class DeviceManagement:
    def __init__(self):
        try:
            self.conn = mariadb.connect(
                user=os.environ.get('DB_USER', 'SMART'),
                password=os.environ.get('DB_PASSWORD', 'SMARTHOME'),
                host=os.environ.get('DB_HOST', 'localhost'),
                port=int(os.environ.get('DB_PORT', 3306)),
                database=os.environ.get('DB_NAME', 'SMART_DB')
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
            query = "SELECT id, state FROM devices"  # Adjust if needed for your DB schema
            cur.execute(query)
            device_list = []
            for row in cur:
                device_list.append({'id': str(row[0]), 'state': str(row[1])})
            cur.close()
            logging.debug(f"Query executed, fetched devices: {device_list}")
            return device_list
        except mariadb.Error as e:
            logging.debug(f"Error fetching devices: {e}")
            return []

    def get_device_state(self, device_id):
        """
        Retrieves the state of a single device by its ID.
        Returns 'ON', 'OFF', or None if not found.
        """
        if self.conn is None:
            return None

        try:
            cur = self.conn.cursor()
            query = "SELECT state FROM devices WHERE id = ?"
            cur.execute(query, (device_id,))
            result = cur.fetchone()
            cur.close()
            if result:
                return str(result[0])
            return None
        except mariadb.Error as e:
            logging.debug(f"Error fetching device state: {e}")
            return None

    def close_connection(self):
        """
        Closes the database connection.
        """
        if self.conn:
            self.conn.close()
            logging.debug("Database connection closed.")