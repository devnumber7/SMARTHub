# home_screen.py

from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
import logging
import os

from kivy.clock import Clock
from datetime import datetime

# Import the backend classes
from user_management import UserManager  # User management backend

class SettingsButton(ButtonBehavior, Image):
    """
    A custom button with an image for the settings icon.
    """
    pass

class HomeScreen(Screen):
    """
    Home Screen with navigation buttons and a real-time clock.
    """
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        # Initialize the backend
        self.backend = UserManager()

        # Path to the custom font and images
        current_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(current_dir, 'fonts', 'SixtyFourConvergence.ttf')
        settings_icon_path = os.path.join(current_dir, 'images', 'settings.png')  # Ensure this path is correct

        # Initialize clock format and Bluetooth status
        self.use_24_hour = False

        # Root layout
        self.layout = FloatLayout()

        # Add the settings button
        self.settings_button = SettingsButton(
            source=settings_icon_path,
            size_hint=(None, None),
            size=(40, 40),  # Adjust size as needed
            pos_hint={'x': 0.02, 'y': 0.876}  # Top-left corner with some padding
        )
        self.settings_button.bind(on_press=self.navigate_to_settings)
        self.layout.add_widget(self.settings_button)

        # Button layout
        button_layout = BoxLayout(
            orientation='vertical',
            spacing=25,
            size_hint=(0.6, 0.6),  # Reduced size for more spacing
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # Create buttons with transparent background
        buttons = [
            {'text': 'Display Devices', 'on_press': self.navigate_to_display_devices},
            {'text': 'Add a User', 'on_press': self.navigate_to_add_user},
            {'text': 'Remove All Users', 'on_press': self.confirm_remove_all},
            {'text': 'Show Active VPN Connections', 'on_press': self.navigate_to_active_vpn}
        ]

        for btn_info in buttons:
            btn = Button(
                text=btn_info['text'],
                size_hint=(1, None),
                height=40,  # Compact height
                font_size='20sp',
                font_name=font_path,
                background_color=(0, 0, 0, 0),  # Transparent background
                color=(1, 1, 1, 1)  # White text
            )
            btn.bind(on_press=btn_info['on_press'])
            button_layout.add_widget(btn)

        self.layout.add_widget(button_layout)

        # Clock label
        self.clock_label = Label(
            text=self.get_current_time(),
            font_size='22sp',
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(180, 50),
            pos_hint={'right': 0.98, 'top': 0.98},
            font_name=font_path,
            halign='right',
            valign='middle'
        )
        self.clock_label.bind(size=self.clock_label.setter('text_size'))
        self.layout.add_widget(self.clock_label)

        # Add semi-transparent background to the clock
        with self.clock_label.canvas.before:
            Color(0, 0, 0, 0.4)  # Semi-transparent black
            self.clock_bg = Rectangle(size=self.clock_label.size, pos=self.clock_label.pos)
        self.clock_label.bind(size=self.update_clock_bg, pos=self.update_clock_bg)

        # Add the root layout to the screen
        self.add_widget(self.layout)

        # Schedule the clock update
        Clock.schedule_interval(self.update_clock, 1)

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
        Removes all users using the backend.
        """
        logging.debug("Removing all users")
        success = self.backend.remove_all_users()
        if success:
            logging.info("All users have been removed successfully.")
            # Optionally, show a success popup
            popup = Popup(
                title='Success',
                content=Label(text='All VPN users have been removed.'),
                size_hint=(0.6, 0.4)
            )
            popup.open()
        else:
            logging.error("Failed to remove all users.")
            # Optionally, show an error popup
            popup = Popup(
                title='Error',
                content=Label(text='Failed to remove all VPN users.'),
                size_hint=(0.6, 0.4)
            )
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

    def navigate_to_settings(self, instance):
        """
        Navigates to the SettingsScreen.
        """
        logging.debug("Navigating to SettingsScreen")
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'settings'
