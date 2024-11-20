# system_control.py

import subprocess
import logging

def toggle_bluetooth(current_status):
    """
    Toggles Bluetooth on or off based on the current status.

    @return Returns the new status (True for on, False for off).
    """
    try:
        if current_status:
            # Turn Bluetooth off
            subprocess.run(['sudo', 'rfkill', 'block', 'bluetooth'], check=True)
        else:
            # Turn Bluetooth on
            subprocess.run(['sudo', 'rfkill', 'unblock', 'bluetooth'], check=True)
        # Update status
        new_status = not current_status
        return new_status
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to toggle Bluetooth: {e}")
        return None  # Indicate failure

def get_bluetooth_status():
    """
    Checks if Bluetooth is currently on or off.
    @return Returns True if on, False if off.
    """
    result = subprocess.run(['rfkill', 'list', 'bluetooth'], capture_output=True, text=True)
    if 'Soft blocked: yes' in result.stdout or 'Hard blocked: yes' in result.stdout:
        return False
    else:
        return True
    
