import subprocess
import os



#jrjr2
class PiVPNBackend:
    """
    Backend class to handle adding a PiVPN user via the bash script.
    """

    def __init__(self):
        # Path to the script that adds a new PiVPN user
        self.script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts/add_pivpn_user.sh')

    def add_user(self, username):
        """
        Calls the add_pivpn_user.sh script with the given username.
        Returns a dictionary with success status and message.
        """
        if not os.path.isfile(self.script_path):
            return {'success': False, 'message': f"Script {self.script_path} not found."}

        try:
            # Run the script with sudo to ensure permissions are correct
            command = ['sudo', 'bash', self.script_path, username]
            result = subprocess.run(command, capture_output=True, text=True, check=True)

            # Check the output for success message
            if 'SUCCESS' in result.stdout:
                return {'success': True, 'message': f"User '{username}' added successfully!\n{result.stdout}"}
            else:
                return {'success': False, 'message': f"Failed to add user '{username}'.\n{result.stderr}"}
        except subprocess.CalledProcessError as e:
            # Catch any errors and return a failure message
            return {'success': False, 'message': f"An error occurred while adding the user.\n{e.stderr}"}
