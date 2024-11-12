# qr_code_generator.py

import os
import logging
import qrcode

class QRCodeGenerator:
    """
    Generates QR codes for VPN configuration files.
    """

    def __init__(self):
        # Directory to store QR code images
        self.qr_image_dir = '/tmp'
        os.makedirs(self.qr_image_dir, exist_ok=True)

    def generate_qr_code(self, username, config_data):
        """
        Generates a QR code for the user's VPN config data and saves it to disk.
        Returns the path to the generated QR code image.
        """
        try:
            # Generate the QR code
            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(config_data)
            qr.make(fit=True)

            # Create an image from the QR code
            img = qr.make_image(fill_color="black", back_color="white")

            # Save the QR code image to the specified directory
            qr_image_path = os.path.join(self.qr_image_dir, f"{username}_qrcode.png")
            img.save(qr_image_path)

            logging.debug(f"QR code generated for user '{username}' at {qr_image_path}.")
            return qr_image_path

        except Exception as e:
            logging.exception(f"Error generating QR code for user '{username}'.")
            return None
