# user_management.py

import subprocess
import os
import logging

class UserManager:
    """
    Handles VPN user management tasks such as adding, listing, and removing users.
    """

    def __init__(self):
        # Directory where VPN config files are stored
        self.config_dir = '/home/SMART/configs'  # Adjust this path as necessary

    def add_user(self, username):
        """
        Adds a VPN user.
        Returns a dictionary with success status and message.
        """
        # Validate the username
        if not self.validate_username(username):
            return {
                'success': False,
                'message': "Invalid username. It must be alphanumeric and between 3-16 characters."
            }

        try:
            # Add the VPN user using the PiVPN command
            add_command = ['sudo', 'pivpn', 'add', '-n', username]
            result = subprocess.run(add_command, capture_output=True, text=True)

            if result.returncode != 0:
                logging.error(f"Error adding user '{username}': {result.stderr}")
                return {
                    'success': False,
                    'message': f"Failed to add VPN user '{username}'."
                }

            # User added successfully
            logging.info(f"User '{username}' added successfully.")
            return {
                'success': True,
                'message': f"User '{username}' added successfully."
            }

        except subprocess.CalledProcessError as e:
            logging.exception(f"Error while adding user '{username}'.")
            return {
                'success': False,
                'message': f"An error occurred while adding the user '{username}'."
            }

    def validate_username(self, username):
        """
        Validates the VPN username. Must be alphanumeric and between 3-16 characters.
        """
        return bool(username) and username.isalnum() and 3 <= len(username) <= 16

    def list_users(self):
        """
        Lists all existing VPN users.
        Returns a list of usernames.
        """
        try:
            # List users using PiVPN
            list_command = ['sudo', 'pivpn', 'list']
            result = subprocess.run(list_command, capture_output=True, text=True)

            if result.returncode != 0:
                logging.error(f"Error listing users: {result.stderr}")
                return []

            users = []
            for line in result.stdout.splitlines():
                # Adjust parsing based on the output format of 'pivpn list'
                if line.strip() and not line.startswith(':::'):
                    parts = line.strip().split()
                    if parts:
                        username = parts[0]
                        users.append(username)
            return users

        except Exception as e:
            logging.exception("An error occurred while listing users.")
            return []

    def remove_all_users(self):
        """
        Removes all VPN users.
        Returns a dictionary with success status and message.
        """
        try:
            users = self.list_users()
            if not users:
                return {
                    'success': True,
                    'message': "No VPN users found to remove."
                }

            # Remove each user
            for username in users:
                remove_command = ['sudo', 'pivpn', 'remove', '-y', username]
                result = subprocess.run(remove_command, capture_output=True, text=True)
                if result.returncode != 0:
                    logging.error(f"Error removing user '{username}': {result.stderr}")
                    # Continue removing other users even if one fails
                    continue
                else:
                    logging.debug(f"User '{username}' removed successfully.")

            return {
                'success': True,
                'message': "All VPN users have been removed successfully."
            }

        except Exception as e:
            logging.exception("An unexpected error occurred while removing all users.")
            return {
                'success': False,
                'message': f"An unexpected error occurred: {str(e)}"
            }
