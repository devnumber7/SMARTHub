#!/bin/bash

# add_pivpn_user.sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Function to display usage
usage() {
    echo "Usage: $0 <username>"
    exit 1
}

# Check if exactly one argument (username) is provided
if [ "$#" -ne 1 ]; then
    usage
fi

USERNAME="$1"

# Basic validation: Username should be alphanumeric and between 3 to 16 characters
if [[ ! "$USERNAME" =~ ^[a-zA-Z0-9_]{3,16}$ ]]; then
    echo "ERROR: Username must be 3-16 characters long and can include letters, numbers, and underscores."
    exit 1
fi

# Add the VPN user using PiVPN
# The '-n' flag specifies the username
# The '-y' flag auto-confirms prompts if supported
# Note: Adjust flags based on your PiVPN version and requirements
echo "Adding VPN user: $USERNAME"
pivpn add -n "$USERNAME" -y

# Check if the user was added successfully
if pivpn list | grep -qw "$USERNAME"; then
    # Assume PiVPN stores .ovpn files in /home/pi/ovpns/
    CONFIG_DIR="/home/pi/ovpns/"
    CONFIG_FILE="${CONFIG_DIR}${USERNAME}.ovpn"

    if [ -f "$CONFIG_FILE" ]; then
        echo "SUCCESS: VPN user '$USERNAME' added successfully."
        echo "Config file generated at: $CONFIG_FILE"
    else
        echo "ERROR: VPN user '$USERNAME' added, but config file not found in $CONFIG_DIR."
        exit 1
    fi
else
    echo "ERROR: Failed to add VPN user '$USERNAME'."
    exit 1
fi
