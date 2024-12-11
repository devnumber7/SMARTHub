# settings_screen.py

from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.switch import Switch
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
import logging
import os

from settings import Settings # Ensure this backend handles Bluetooth operations


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        
        # Initialize the backend
        self.backend = Settings()

        # Path configurations
        current_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(current_dir, 'fonts', 'SixtyFourConvergence.ttf')  # Using Roboto for better readability
        icon_path = os.path.join(current_dir, 'images', 'settings.png')  # Ensure this path is correct

        # Root layout
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20, size_hint=(1, 1))

        # Header Section
        header_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)
        
        # Settings Icon
        with header_layout.canvas.before:
              # White background for the header
            self.header_bg = Rectangle(pos=self.pos, size=(Window.width, 60))
        
        header_label = Label(
            text="Settings",
            font_size='24sp',
            font_name=font_path,
            color=(0, 0, 0, 1),  # Black text for contrast
            halign='left',
            valign='middle'
        )
        header_label.bind(size=header_label.setter('text_size'))
        
        header_layout.add_widget(header_label)
        self.layout.add_widget(header_layout)

        # Divider Line
        with self.layout.canvas.before:
            Color(0.8, 0.8, 0.8, 1)  # Light grey color for divider
            self.divider = Rectangle(pos=(20, Window.height - 80), size=(Window.width - 40, 2))
        self.layout.bind(size=self.update_divider)

        # Content Section
        content_layout = BoxLayout(orientation='vertical', spacing=20, size_hint=(1, 0.8))
        
        # Bluetooth Toggle
        bluetooth_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50, padding=(10, 10))
        
        bluetooth_label = Label(
            text="Bluetooth",
            font_size='20sp',
            font_name=font_path,
            color=(1, 1, 1, 1),  # Black text
            halign='left',
            valign='middle'
        )
        bluetooth_label.bind(size=bluetooth_label.setter('text_size'))
        
        self.bluetooth_switch = Switch(
            active=self.backend.is_bluetooth_enabled(),  # Backend should provide this method
            size_hint=(None, None),
            size=(50, 30),
           
        )
        self.bluetooth_switch.bind(active=self.on_bluetooth_toggle)
        
        bluetooth_layout.add_widget(bluetooth_label)
        bluetooth_layout.add_widget(self.bluetooth_switch)
        
        content_layout.add_widget(bluetooth_layout)
        
        # Additional Settings can be added here following the same pattern

        self.layout.add_widget(content_layout)

        # Footer Section with Back Button
        footer_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        
        back_button = Button(
            text='Back',
            size_hint=(None, None),
            size=(100, 40),
            font_size='18sp',
            font_name=font_path,
          #  background_color=(0.2, 0.6, 0.86, 1),  # Material Design primary color
            color=(1, 1, 1, 1)  # White text
        )
        back_button.bind(on_press=self.navigate_back)
        footer_layout.add_widget(back_button)
        self.layout.add_widget(footer_layout)

        # Add the root layout to the screen
        self.add_widget(self.layout)

    def update_divider(self, *args):
        """
        Update the divider line position and size when the window size changes.
        """
        self.divider.pos = (20, Window.height - 80)
        self.divider.size = (Window.width - 40, 2)

    def on_bluetooth_toggle(self, switch, value):
        """
        Handles the Bluetooth toggle switch.
        """
        if value:
            logging.debug("Bluetooth enabled")
            success = self.backend.enable_bluetooth()
            if success:
                self.show_popup("Bluetooth Enabled", "Bluetooth has been turned on.")
            else:
                logging.error("Failed to enable Bluetooth.")
                self.show_popup("Error", "Failed to enable Bluetooth.")
                switch.active = False  # Revert the switch if failed
        else:
            logging.debug("Bluetooth disabled")
            success = self.backend.disable_bluetooth()
            if success:
                self.show_popup("Bluetooth Disabled", "Bluetooth has been turned off.")
            else:
                logging.error("Failed to disable Bluetooth.")
                self.show_popup("Error", "Failed to disable Bluetooth.")
                switch.active = True  # Revert the switch if failed

    def show_popup(self, title, message):
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
            font_size='18sp',
            background_color=(0.2, 0.6, 0.86, 1),  # Consistent with back button
            color=(1, 1, 1, 1)
        )
        popup_content.add_widget(close_button)

        popup = Popup(
            title=title,
            content=popup_content,
            size_hint=(0.6, 0.4),
            auto_dismiss=False
        )

        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def navigate_back(self, instance):
        """
        Navigates back to the HomeScreen with a slide transition.
        """
        logging.debug("Navigating back to HomeScreen")
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'home'
