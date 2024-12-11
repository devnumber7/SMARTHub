from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
import os
import threading
import logging
import requests  # Ensure requests is imported

# Import the backend module
from device_management import DeviceManagement

class DisplayDevicesScreen(Screen):
    """
    Screen to display a list of devices with their states (On/Off).
    """
    def __init__(self, **kwargs):
        super(DisplayDevicesScreen, self).__init__(**kwargs)

        # Initialize logging
        logging.basicConfig(level=logging.DEBUG)

        # Initialize the device management backend
        self.device_manager = DeviceManagement()

        # Path to the custom font
        current_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(current_dir, 'fonts', 'SixtyFourConvergence.ttf')

        # Main vertical layout
        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Title label
        title_label = Label(
            text='Active Devices',
            font_size='24sp',
            size_hint=(1, 0.1),
            font_name=font_path
        )
        self.main_layout.add_widget(title_label)

        # Scrollable area for the device list
        self.scroll_view = ScrollView(size_hint=(1, 0.8))

        # Grid layout inside the scroll view
        self.devices_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.devices_layout.bind(minimum_height=self.devices_layout.setter('height'))

        # Add the devices layout to the scroll view
        self.scroll_view.add_widget(self.devices_layout)

        # Add the scroll view to the main layout
        self.main_layout.add_widget(self.scroll_view)

        # Back and Refresh buttons
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)

        back_button = Button(
            text='Back',
            size_hint=(0.5, 1),
            font_name=font_path
        )
        back_button.bind(on_press=self.go_back)

        refresh_button = Button(
            text='Refresh',
            size_hint=(0.5, 1),
            font_name=font_path
        )
        refresh_button.bind(on_press=self.load_devices)

        button_layout.add_widget(back_button)
        button_layout.add_widget(refresh_button)
        self.main_layout.add_widget(button_layout)

        # Add the main layout to the screen
        self.add_widget(self.main_layout)

        # Load the devices
        self.load_devices()

    def load_devices(self, *args):
        """
        Starts a new thread to fetch devices from the backend.
        """
        logging.debug("Loading devices...")
        threading.Thread(target=self.fetch_devices, daemon=True).start()

    def fetch_devices(self):
        """
        Fetches devices from the backend and schedules the UI update.
        """
        devices = self.device_manager.get_devices()
        logging.debug(f"Fetched devices: {devices}")
        Clock.schedule_once(lambda dt: self.update_devices_ui(devices))

    def update_devices_ui(self, devices):
        """
        Updates the UI with the list of devices.
        """
        # Clear any existing widgets
        logging.debug("Clearing existing widgets.")
        self.devices_layout.clear_widgets()

        if devices:
            logging.debug(f"Updating UI with devices: {devices}")
            for device in devices:
                # Horizontal layout for each device entry
                device_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)

                # Device id label
                device_label = Label(
                    text=str(device['id']),
                    font_size='18sp',
                    font_name=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts', 'SixtyFourConvergence.ttf'),
                    size_hint=(0.3, 1),
                    halign='left',
                    valign='middle'
                )
                device_label.bind(size=device_label.setter('text_size'))

                # Device state label
                state_label = Label(
                    text=str(device['state']),
                    font_size='18sp',
                    font_name=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts', 'SixtyFourConvergence.ttf'),
                    size_hint=(0.2, 1),
                    halign='center',
                    valign='middle',
                    color=(0, 1, 0, 1) if str(device['state']).lower() == 'on' else (1, 0, 0, 1)
                )
                state_label.bind(size=state_label.setter('text_size'))

                # On/Off button
                toggle_button = Button(
                    text='Turn Off' if str(device['state']).lower() == 'on' else 'Turn On',
                    size_hint=(0.3, 1),
                    font_name=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts', 'SixtyFourConvergence.ttf')
                )
                toggle_button.device_id = device['id']  # Attach device ID to the button
                toggle_button.bind(on_press=self.toggle_device_state)

                # Add widgets to the device layout
                device_layout.add_widget(device_label)
                device_layout.add_widget(state_label)
                device_layout.add_widget(toggle_button)

                # Add device layout to the devices layout
                self.devices_layout.add_widget(device_layout)
        else:
            logging.debug("No devices found. Showing placeholder.")
            # If no devices are found or an error occurred
            no_device_label = Label(
                text='No active devices found.',
                font_size='18sp',
                font_name=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts', 'SixtyFourConvergence.ttf'),
                size_hint=(1, None),
                height=50
            )
            self.devices_layout.add_widget(no_device_label)

    def toggle_device_state(self, instance):
        """
        Toggles the state of the device and sends a POST request to update the backend.
        """
        device_id = instance.device_id
        current_state = None

        # Find the current state of the device
        for child in self.devices_layout.children:
            # child.children list is in reverse order in Kivy, so adjust accordingly
            device_label = child.children[2]  # device_label is the third child added
            if isinstance(device_label, Label) and device_label.text == device_id:
                state_label = child.children[1]  # state_label is the second child
                current_state = state_label.text.lower()
                break

        if current_state is None:
            logging.error(f"Could not find current state for device {device_id}")
            return

        # Determine the new action based on current state
        if current_state == 'on':
            action = 'deactivate'
        else:
            action = 'activate'

        # Update button text optimistically
        instance.text = 'Turning On...' if action == 'activate' else 'Turning Off...'
        instance.disabled = True

        # Start a new thread to send the POST request
        threading.Thread(target=self.send_toggle_request, args=(device_id, action, instance), daemon=True).start()

    def send_toggle_request(self, device_id, action, button_instance):
        """
        Sends a POST request to toggle the device state.
        """
        # Updated to match the working curl URL
        url = 'https://198.82.190.97:5000/control-method'
        data = {
            'action': action,
            'device_id': device_id
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        try:
            logging.debug(f"Sending POST request to {url} with data: {data}")
            response = requests.post(url, data=data, headers=headers, verify=False)
            logging.debug(f"Response Status: {response.status_code}, Body: {response.text}")

            # Check if the response is valid JSON
            try:
                response_data = response.json()
                new_state = response_data.get('state', 'OFF').upper()
            except ValueError as e:
                logging.error(f"Error parsing response as JSON: {e}")
                logging.error(f"Response body: {response.text}")
                # Fallback based on action
                new_state = 'ON' if action == 'activate' else 'OFF'

            # Schedule UI update on the main thread
            Clock.schedule_once(lambda dt: self.update_device_ui_after_toggle(device_id, new_state, button_instance))
        except requests.RequestException as e:
            logging.error(f"Error sending toggle request for device {device_id}: {e}")
            Clock.schedule_once(lambda dt: self.reset_button_state(button_instance, action))

    def update_device_ui_after_toggle(self, device_id, new_state, button_instance):
        """
        Updates the UI after successfully toggling the device state.
        """
        for child in self.devices_layout.children:
            # child.children list is in reverse order in Kivy, so adjust accordingly
            device_label = child.children[2]  # device_label is the third child added
            if isinstance(device_label, Label) and device_label.text == device_id:
                state_label = child.children[1]  # state_label is the second child
                state_label.text = new_state
                state_label.color = (0, 1, 0, 1) if new_state.lower() == 'on' else (1, 0, 0, 1)

                # Update the button text
                button_instance.text = 'Turn Off' if new_state.lower() == 'on' else 'Turn On'
                button_instance.disabled = False
                break

    def reset_button_state(self, button_instance, action):
        """
        Resets the button state if the POST request failed.
        """
        button_instance.text = 'Turn On' if action == 'activate' else 'Turn Off'
        button_instance.disabled = False

    def go_back(self, instance):
        """
        Navigates back to the Home Screen with a slide transition.
        """
        logging.debug("Returning to HomeScreen")
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'home'
