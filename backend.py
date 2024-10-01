# backend.py

import subprocess
import logging
import os

class PiVPNBackend:
    """
    Backend class to interact with PiVPN commands via a separate Bash script.
    """
    def __init__(self):
        # Path to the Bash script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.script_path = os.path.join(current_dir, 'scripts', 'add_pivpn_user.sh')
        
        # Verify that the script exists
        if not os.path.isfile(self.script_path):
            logging.error(f"Bash script not found at: {self.script_path}")
            raise FileNotFoundError(f"Bash script not found at: {self.script_path}")

    def add_user(self, username):
        """
        Adds a new VPN user by executing the Bash script.
        
        Args:
            username (str): The username for the VPN client.
        
        Returns:
            dict: A dictionary containing 'success' (bool) and 'message' (str).
        """
        try:
            # Construct the command to execute the Bash script
            command = [self.script_path, username]
            logging.debug(f"Executing command: {' '.join(command)}")

            # Execute the Bash script
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True  # Raises CalledProcessError if the command exits with non-zero status
            )

            logging.debug(f"Bash Script Output:\n{result.stdout}")

            # Parse the output to determine success or failure
            if "SUCCESS" in result.stdout:
                # Extract the config file path
                lines = result.stdout.splitlines()
                config_file_line = next((line for line in lines if "Config file generated at:" in line or "Config file located at:" in line), None)
                if config_file_line:
                    config_file = config_file_line.split(":")[1].strip()
                    message = f"VPN user '{username}' added successfully. Config file located at: {config_file}"
                else:
                    message = "VPN user added successfully, but config file location could not be determined."
                return {'success': True, 'message': message}
            else:
                # Extract error message
                error_message = next((line for line in result.stdout.splitlines() if line.startswith("ERROR")), "An unknown error occurred.")
                return {'success': False, 'message': error_message}

        except subprocess.CalledProcessError as e:
            # Handle errors from the Bash script
            error_message = e.stderr.strip() if e.stderr else 'An error occurred while adding the user.'
            logging.error(f"Bash Script Error: {error_message}")
            return {'success': False, 'message': error_message}
        except Exception as e:
            # Handle unexpected errors
            logging.exception("Unexpected error occurred in PiVPNBackend.add_user")
            return {'success': False, 'message': str(e)}
