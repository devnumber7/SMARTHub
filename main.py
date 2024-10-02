# main_app.py

import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
import logging

# Import the screens
from home_screen import HomeScreen
from add_user_screen import AddUserScreen

# Ensure compatibility with the latest Kivy version
kivy.require('2.0.0')

# Configure logging for debugging purposes
logging.basicConfig(level=logging.DEBUG)


class SmartHubApp(App):
    """
    Main application class managing the window and screen transitions.
    """
    def build(self):
        # Set the window size to 800x480 pixels
        Window.size = (800, 480)
        Window.title = "SmartHub VPN Config Generator"

        # Initialize the ScreenManager with SlideTransition
        sm = ScreenManager(transition=SlideTransition(direction="left"))

        # Create instances of the screens
        home_screen = HomeScreen(name='home')
        add_user_screen = AddUserScreen(name='add_user')

        # Add screens to the ScreenManager
        sm.add_widget(home_screen)
        sm.add_widget(add_user_screen)

        logging.debug("SmartHubApp built successfully with Home and AddUser screens.")

        return sm

if __name__ == '__main__':
    SmartHubApp().run()
