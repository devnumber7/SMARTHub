# vpn_status.py

import subprocess
import logging
import re
from datetime import datetime

class VPNStatusChecker:
    """
    Checks the status of VPN connections and clients using WireGuard commands.
    """

    def get_active_vpn_clients(self):
        """
        Retrieves the list of active VPN clients by parsing the output of 'wg show'.
        Returns a list of dictionaries containing peer information.
        """
        try:
            # Execute the 'wg show' command to get the current status
            result = subprocess.run(['sudo', 'wg', 'show', 'all', 'dump'], capture_output=True, text=True)
            
            if result.returncode != 0:
                logging.error(f"Error executing 'wg show': {result.stderr}")
                return []

            active_clients = []
            # The 'wg show all dump' provides a machine-readable output
            # Format: interface, public_key, preshared_key, endpoint, allowed_ips, latest_handshake, transfer_rx, transfer_tx
            for line_number, line in enumerate(result.stdout.splitlines(), start=1):
                parts = line.strip().split('\t')
                
                if len(parts) < 8:
                    logging.warning(f"Line {line_number}: Expected at least 8 fields, got {len(parts)}. Line content: {line}")
                    continue
                
                # Safely unpack the first 8 fields, ignoring any extra fields
                interface, public_key, preshared_key, endpoint, allowed_ips, latest_handshake, transfer_rx, transfer_tx = parts[:8]

                # Extract the IP address from allowed_ips (assuming the first IP is primary)
                ip_match = re.search(r'(\d{1,3}\.){3}\d{1,3}', allowed_ips)
                ip_address = ip_match.group() if ip_match else "Unknown"

                # Convert latest_handshake from Unix timestamp to readable format
                if latest_handshake.isdigit() and int(latest_handshake) > 0:
                    handshake_time = datetime.fromtimestamp(int(latest_handshake)).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    handshake_time = "Never"

                client_info = {
                    'interface': interface,
                    'public_key': public_key,
                    'endpoint': endpoint,
                    'allowed_ips': allowed_ips,
                    'latest_handshake': handshake_time,
                    'transfer_rx': transfer_rx,
                    'transfer_tx': transfer_tx,
                    'ip_address': ip_address
                }
                active_clients.append(client_info)

            logging.debug(f"Active VPN clients: {active_clients}")
            return active_clients

        except Exception as e:
            logging.exception("An error occurred while fetching active VPN clients.")
            return []
