# display_devices_screen.py

from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
import os
import threading

# Import the backend module
from device_management import DeviceManagement

class DisplayDevicesScreen(Screen):
    """
    Screen to display a list of devices with their states (On/Off).
    """
    def __init__(self, **kwargs):
        super(DisplayDevicesScreen, self).__init__(**kwargs)

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

        # Grid layout inside the scroll view to list devices
        self.devices_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.devices_layout.bind(minimum_height=self.devices_layout.setter('height'))

        # Add the devices layout to the scroll view
        self.scroll_view.add_widget(self.devices_layout)

        # Add the scroll view to the main layout
        self.main_layout.add_widget(self.scroll_view)

        # Back button to return to the home screen
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
        refresh_button.bind(on_press=lambda x: self.load_devices())

        button_layout.add_widget(back_button)
        button_layout.add_widget(refresh_button)
        self.main_layout.add_widget(button_layout)

        # Add the main layout to the screen
        self.add_widget(self.main_layout)

        # Load the devices
        self.load_devices()

    def load_devices(self):
        """
        Starts a new thread to fetch devices from the backend.
        """
        threading.Thread(target=self.fetch_devices, daemon=True).start()

    def fetch_devices(self):
        """
        Fetches devices from the backend and schedules the UI update.
        """
        devices = self.device_manager.get_devices()
        # Schedule the UI update on the main thread
        Clock.schedule_once(lambda dt: self.update_devices_ui(devices))

    def update_devices_ui(self, devices):
        """
        Updates the UI with the list of devices.
        """
        # Clear any existing widgets
        self.devices_layout.clear_widgets()

        if devices:
            for device in devices:
                # Horizontal layout for each device entry
                device_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)

                # Device id label
                device_label = Label(
                    text=str(device['id']),
                    font_size='18sp',
                    font_name=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts', 'SixtyFourConvergence.ttf'),
                    size_hint=(0.7, 1),
                    halign='left',
                    valign='middle'
                )
                device_label.bind(size=device_label.setter('text_size'))

                # Device state label
                state_label = Label(
                    text=str(device['state']),
                    font_size='18sp',
                    font_name=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts', 'SixtyFourConvergence.ttf'),
                    size_hint=(0.3, 1),
                    halign='right',
                    valign='middle',
                    color=(0, 1, 0, 1) if str(device['state']).lower() == 'on' else (1, 0, 0, 1)  # Green for On, Red for Off
                )
                state_label.bind(size=state_label.setter('text_size'))

                # Add labels to the device layout
                device_layout.add_widget(device_label)
                device_layout.add_widget(state_label)

                # Add device layout to the devices layout
                self.devices_layout.add_widget(device_layout)
        else:
            # If no devices are found or an error occurred
            no_device_label = Label(
                text='No active devices found.',
                font_size='18sp',
                font_name=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts', 'SixtyFourConvergence.ttf'),
                size_hint=(1, None),
                height=50
            )
            self.devices_layout.add_widget(no_device_label)

    def go_back(self, instance):
        """
        Returns to the HomeScreen when the back button is pressed.
        """
        # Close the database connection
        self.device_manager.close_connection()
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'home'

