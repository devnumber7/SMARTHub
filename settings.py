import logging
import subprocess

class Settings:
    def __init__(self):
        pass

    def is_bluetooth_enabled(self):
        """
        Check if Bluetooth service is active.
        Returns True if active, False otherwise.
        """
        try:
            result = subprocess.run(
                ['systemctl', 'is-active', 'bluetooth'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            status = result.stdout.strip()
            logging.debug(f"Bluetooth service status: {status}")
            return status == 'active'
        except subprocess.CalledProcessError as e:
            logging.error(f"Error checking Bluetooth status: {e.stderr.strip()}")
            return False
        

    
    def enable_bluetooth(self):
        """
        Enable Bluetooth service.
        Returns True if successful, False otherwise.
        """
        try:
            # Start the Bluetooth service
            subprocess.run(
                ['rfkill', 'unblock', 'bluetooth'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
           
            logging.info("Bluetooth has been enabled successfully.")
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"Error enabling Bluetooth: {e.stderr.strip()}")
            return False

    def disable_bluetooth(self):
        """
        Disable Bluetooth service.
        Returns True if successful, False otherwise.
        """
        try:
            # Stop the Bluetooth service
            subprocess.run(
                ['rfkill', 'block', 'bluetooth'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
        
            logging.info("Bluetooth has been disabled successfully.")
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"Error disabling Bluetooth: {e.stderr.strip()}")
            return False
  
    


