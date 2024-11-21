from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import os

from mariadb_connector import MariaDBConnector

class DisplayDevicesScreen(Screen):
    """
    Screen to display a list of devices with their states (On/Off).
    """
    def __init__(self, **kwargs):
        super(DisplayDevicesScreen, self).__init__(**kwargs)

        # Initialize the backend
        self.connector = MariaDBConnector()

        # Path to the custom font
        current_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(current_dir, 'fonts', 'SixtyFourConvergence.ttf')

        # Main vertical layout
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Title label
        title_label = Label(
            text='Active Devices',
            font_size='24sp',
            size_hint=(1, 0.1),
            font_name=font_path
        )
        main_layout.add_widget(title_label)

        # Scrollable area for the device list
        scroll_view = ScrollView(size_hint=(1, 0.8))

        # Grid layout inside the scroll view to list devices
        devices_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        devices_layout.bind(minimum_height=devices_layout.setter('height'))

        # Placeholder device data (to be replaced with backend data)
        dummy_devices = [
            {'name': 'Device 1', 'state': 'On'},
            {'name': 'Device 2', 'state': 'Off'},
            {'name': 'Device 3', 'state': 'On'},
            {'name': 'Device 4', 'state': 'Off'},
            {'name': 'Device 5', 'state': 'On'},
            {'name': 'Device 6', 'state': 'Off'},
            {'name': 'Device 7', 'state': 'On'},
            {'name': 'Device 8', 'state': 'Off'},
            {'name': 'Device 9', 'state': 'On'},
            {'name': 'Device 10', 'state': 'Off'},
            # Add more devices as needed
        ]

        # Create UI elements for each device
        for device in dummy_devices:
            # Horizontal layout for each device entry
            device_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)

            # Device name label
            device_label = Label(
                text=device['name'],
                font_size='18sp',
                font_name=font_path,
                size_hint=(0.7, 1),
                halign='left',
                valign='middle'
            )
            device_label.bind(size=device_label.setter('text_size'))

            # Device state label
            state_label = Label(
                text=device['state'],
                font_size='18sp',
                font_name=font_path,
                size_hint=(0.3, 1),
                halign='right',
                valign='middle',
                color=(0, 1, 0, 1) if device['state'] == 'On' else (1, 0, 0, 1)  # Green for On, Red for Off
            )
            state_label.bind(size=state_label.setter('text_size'))

            # Add labels to the device layout
            device_layout.add_widget(device_label)
            device_layout.add_widget(state_label)

            # Add device layout to the devices layout
            devices_layout.add_widget(device_layout)

        # Add the devices layout to the scroll view
        scroll_view.add_widget(devices_layout)

        # Add the scroll view to the main layout
        main_layout.add_widget(scroll_view)

        # Back button to return to the home screen
        back_button = Button(
            text='Back',
            size_hint=(0.2, 0.1),
            font_name=font_path
        )
        back_button.bind(on_press=self.go_back)
        main_layout.add_widget(back_button)

        # Add the main layout to the screen
        self.add_widget(main_layout)

    def go_back(self, instance):
        """
        Returns to the HomeScreen when the back button is pressed.
        """
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'home'





