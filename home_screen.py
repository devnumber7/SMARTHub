# home_screen.py

from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
import logging
import os
import threading
from kivy.clock import Clock
from datetime import datetime

# Import the backend classes
from user_management import UserManager  # User management backend
from system_control import toggle_bluetooth, get_bluetooth_status  # System control backend

class ImageButton(ButtonBehavior, Image):
    """
    A custom widget combining ButtonBehavior and Image to create an image button.
    """
    pass

class HomeScreen(Screen):
    """
    Home Screen with navigation buttons, a real-time clock, and a settings icon.
    """
    def __init__(self, **kwargs):
        """
        Initializes the HomeScreen with a UserManager backend, a custom font, and all the UI elements.
        """
        super(HomeScreen, self).__init__(**kwargs)

        # Initialize the backend
        self.backend = UserManager()

        # Path to the custom font
        current_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(current_dir, 'fonts', 'SixtyFourConvergence.ttf')

        # Initialize clock format BEFORE using it
        self.use_24_hour = False

        # Initialize Bluetooth status BEFORE using it
        self.bluetooth_status = get_bluetooth_status()

        # Create the root FloatLayout
        self.layout = FloatLayout()

        # Create the main vertical BoxLayout for content
        main_box = BoxLayout(
            orientation='vertical',
            padding=[60, 40, 60, 40],  # [left, top, right, bottom]
            spacing=30,
            size_hint=(1, 0.8),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # Add a welcome label
        welcome_label = Label(
            text='WELCOME TO SMART HUB',
            font_size='32sp',
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=50,
            font_name=font_path,
            halign='center',
            valign='middle'
        )
        welcome_label.bind(size=welcome_label.setter('text_size'))
        main_box.add_widget(welcome_label)

        # Create a separate layout for buttons
        button_layout = BoxLayout(
            orientation='vertical',
            spacing=20,
            size_hint=(1, None)
        )
        button_layout.bind(minimum_height=button_layout.setter('height'))

        # Button size settings
        button_size_hint = (1, None)
        button_height = 30

        # Create buttons with appropriate sizing and spacing
        buttons = [
            {
                'text': 'Display Devices',
                'on_press': self.navigate_to_display_devices
            },
            {
                'text': 'Add a User',
                'on_press': self.navigate_to_add_user
            },
            {
                'text': 'Remove All Users',
                'on_press': self.confirm_remove_all,
                'background_color': (1, 0, 0, 1)  # Red color
            },
            {
                'text': 'Show Active VPN Connections',
                'on_press': self.navigate_to_active_vpn
            }
        ]

        for btn_info in buttons:
            btn = Button(
                text=btn_info['text'],
                size_hint=button_size_hint,
                height=button_height,
                font_size='8sp',
                font_name=font_path
            )
            if 'background_color' in btn_info:
                btn.background_color = btn_info['background_color']
            btn.bind(on_press=btn_info['on_press'])
            button_layout.add_widget(btn)

        # Add the button layout to the main box
        main_box.add_widget(button_layout)

        # Add the main content BoxLayout to the FloatLayout
        self.layout.add_widget(main_box)

        # Create a Label for the clock
        self.clock_label = Label(
            text=self.get_current_time(),  # Now safe to call get_current_time()
            font_size='20sp',
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(150, 40),
            pos_hint={'right': 0.98, 'top': 0.98},
            font_name=font_path,
            halign='right',
            valign='middle'
        )
        self.clock_label.bind(size=self.clock_label.setter('text_size'))
        self.layout.add_widget(self.clock_label)

        # Add a semi-transparent background to the clock label
        with self.clock_label.canvas.before:
            Color(0, 0, 0, 0.5)  # Semi-transparent black
            self.clock_bg = Rectangle(size=self.clock_label.size, pos=self.clock_label.pos)
        self.clock_label.bind(size=self.update_clock_bg, pos=self.update_clock_bg)

        # Add Settings Icon Button
        settings_icon_path = os.path.join(current_dir, 'images', 'settings_icon.png')  # Make sure this image exists
        self.settings_button = ImageButton(
            source=settings_icon_path,
            size_hint=(None, None),
            size=(40, 40),
            pos_hint={'x': 0.02, 'top': 0.98}
        )
        self.settings_button.bind(on_press=self.open_settings)
        self.layout.add_widget(self.settings_button)

        # Add the root layout to the screen
        self.add_widget(self.layout)

        # Schedule the clock to update every second
        Clock.schedule_interval(self.update_clock, 1)

    def open_settings(self, instance):
        """
        Opens the settings popup when the settings button is pressed.
        """
        # Create content for the settings popup
        popup_content = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Clock Format Toggle
        clock_format_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.2))
        clock_label = Label(
            text='24-Hour Clock:',
            font_size='18sp',
            color=(1, 1, 1, 1),
            font_name=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts', 'SixtyFourConvergence.ttf')
        )
        self.clock_switch = Button(
            text='On' if self.use_24_hour else 'Off',
            size_hint=(0.3, 1),
            font_size='18sp'
        )
        self.clock_switch.bind(on_press=self.toggle_clock_format)
        clock_format_layout.add_widget(clock_label)
        clock_format_layout.add_widget(self.clock_switch)
        popup_content.add_widget(clock_format_layout)

        # Bluetooth Toggle
        bluetooth_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.2))
        bluetooth_label = Label(
            text='Bluetooth:',
            font_size='18sp',
            color=(1, 1, 1, 1),
            font_name=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts', 'SixtyFourConvergence.ttf')
        )
        self.bluetooth_button = Button(
            text='On' if self.bluetooth_status else 'Off',
            size_hint=(0.3, 1),
            font_size='18sp'
        )
        self.bluetooth_button.bind(on_press=self.toggle_bluetooth)
        bluetooth_layout.add_widget(bluetooth_label)
        bluetooth_layout.add_widget(self.bluetooth_button)
        popup_content.add_widget(bluetooth_layout)

        # Close Button
        close_button = Button(
            text='Close',
            size_hint=(1, 0.2),
            font_size='18sp',
            font_name=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts', 'SixtyFourConvergence.ttf')
        )
        close_button.bind(on_press=lambda x: self.settings_popup.dismiss())
        popup_content.add_widget(close_button)

        # Create the popup
        self.settings_popup = Popup(
            title='Settings',
            content=popup_content,
            size_hint=(0.8, 0.6)
        )

        self.settings_popup.open()

    def toggle_clock_format(self, instance):
        """
        Toggles the clock format between 12-hour and 24-hour.
        """
        self.use_24_hour = not self.use_24_hour
        self.clock_switch.text = 'On' if self.use_24_hour else 'Off'
        self.update_clock(0)

    def get_current_time(self):
        """
        Returns the current time formatted as per the user's preference.
        """
        if self.use_24_hour:
            return datetime.now().strftime('%H:%M:%S')
        else:
            return datetime.now().strftime('%I:%M:%S %p')

    def update_clock(self, dt):
        """
        Updates the clock label with the current time.
        """
        self.clock_label.text = self.get_current_time()

    def update_clock_bg(self, *args):
        """
        Updates the background size and position to match the clock label.
        """
        self.clock_bg.size = self.clock_label.size
        self.clock_bg.pos = self.clock_label.pos

    def toggle_bluetooth(self, instance):
        """
        Toggles Bluetooth on/off.
        """
        # Use the backend function to toggle Bluetooth
        new_status = toggle_bluetooth(self.bluetooth_status)
        if new_status is not None:
            self.bluetooth_status = new_status
            self.bluetooth_button.text = 'On' if self.bluetooth_status else 'Off'
        else:
            self.display_message('Error', 'Failed to toggle Bluetooth. Please check permissions.')

    def navigate_to_add_user(self, instance):
        """
        Navigates to the AddUserScreen with a slide transition.
        """
        logging.debug("Navigating to AddUserScreen")
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'add_user'

    def confirm_remove_all(self, instance):
        """
        Displays a confirmation dialog before removing all users.
        """
        # Create content for the confirmation popup
        popup_content = BoxLayout(orientation='vertical', padding=20, spacing=20)
        warning_label = Label(
            text="Are you sure you want to remove all VPN users?\nThis action cannot be undone.",
            font_size='18sp',
            color=(1, 0, 0, 1),  # Red text for warning
            halign='center',
            valign='middle'
        )
        warning_label.bind(size=warning_label.setter('text_size'))
        popup_content.add_widget(warning_label)

        # Create buttons for confirmation
        button_layout = BoxLayout(orientation='horizontal', spacing=20, size_hint=(1, 0.3))
        yes_button = Button(
            text='Yes',
            size_hint=(0.5, 1),
            background_color=(1, 0, 0, 1),  # Red color
            font_size='18sp'
        )
        no_button = Button(
            text='No',
            size_hint=(0.5, 1),
            font_size='18sp'
        )
        button_layout.add_widget(yes_button)
        button_layout.add_widget(no_button)
        popup_content.add_widget(button_layout)

        # Create the popup
        self.confirm_popup = Popup(
            title='Confirm Removal',
            content=popup_content,
            size_hint=(0.8, 0.5)
        )

        # Bind the buttons
        yes_button.bind(on_press=self.remove_all_users)
        yes_button.bind(on_press=self.confirm_popup.dismiss)
        no_button.bind(on_press=self.confirm_popup.dismiss)

        self.confirm_popup.open()

    def remove_all_users(self, instance):
        """
        Calls the backend to remove all VPN users and displays the result.
        """
        logging.debug("Initiating removal of all VPN users")
        # Disable the button to prevent multiple clicks
        instance.disabled = True
        # Start the removal process in a separate thread
        threading.Thread(target=self.process_remove_all_users, args=(instance,), daemon=True).start()

    def process_remove_all_users(self, button_instance):
        """
        Processes the removal of all VPN users.
        Runs in a separate thread to prevent UI blocking.
        """
        result = self.backend.remove_all_users()
        # Schedule the UI update on the main thread
        Clock.schedule_once(lambda dt: self.handle_remove_all_response(result, button_instance), 0)

    def handle_remove_all_response(self, result, button_instance):
        """
        Handles the response from the backend after attempting to remove all users.
        """
        # Re-enable the button
        button_instance.disabled = False

        if result['success']:
            self.display_message('Success', result['message'])
        else:
            self.display_message('Error', result['message'])

    def display_message(self, title, message):
        """
        Displays a popup with the given title and message.
        """
        popup_content = BoxLayout(orientation='vertical', padding=20, spacing=20)
        message_label = Label(
            text=message,
            font_size='18sp',
            halign='center',
            valign='middle'
        )
        message_label.bind(size=message_label.setter('text_size'))
        popup_content.add_widget(message_label)

        close_button = Button(
            text='Close',
            size_hint=(1, 0.3),
            font_size='18sp'
        )
        popup_content.add_widget(close_button)

        popup = Popup(
            title=title,
            content=popup_content,
            size_hint=(0.8, 0.5)
        )

        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def navigate_to_active_vpn(self, instance):
        """
        Navigates to the ActiveVPNScreen.
        """
        logging.debug("Navigating to ActiveVPNScreen")
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'active_vpn'

    def navigate_to_display_devices(self, instance):
        """
        Navigates to the DisplayDevicesScreen.
        """
        logging.debug("Navigating to DisplayDevicesScreen")
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'display_devices'
