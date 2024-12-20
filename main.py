import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.core.window import Window
import logging

# Import the screens
from home_screen import HomeScreen
from add_user_screen import AddUserScreen
from active_vpn_screen import ActiveVPNScreen
from display_devices_screen import DisplayDevicesScreen
from settings_screen import SettingsScreen

# Ensure compatibility with the latest Kivy version
kivy.require('2.0.0')

# Configure logging for debugging purposes
logging.basicConfig(level=logging.DEBUG)

class SmartHubApp(App):
    """
    Main application class managing the window and screen transitions.
    """
    def build(self):
        # Enable full-screen mode
        Window.fullscreen = 'auto'  # Use 'auto' or 'true' for full screen

        # Optionally, set the window size for non-fullscreen debugging
        # Window.size = (800, 480)
        Window.title = "SmartHub App"

        # Initialize the ScreenManager with SlideTransition
        sm = ScreenManager(transition=SlideTransition())

        # Create instances of the screens
        home_screen = HomeScreen(name='home')
        add_user_screen = AddUserScreen(name='add_user')
        active_vpn_screen = ActiveVPNScreen(name='active_vpn')
        display_devices_screen = DisplayDevicesScreen(name='display_devices')
        settings_screen = SettingsScreen(name='settings')

        # Add screens to the ScreenManager
        sm.add_widget(home_screen)
        sm.add_widget(add_user_screen)
        sm.add_widget(active_vpn_screen)
        sm.add_widget(display_devices_screen)
        sm.add_widget(settings_screen)

        logging.debug("SmartHubApp built successfully with Home, AddUser, and ActiveVPN screens.")

        return sm

if __name__ == '__main__':
    SmartHubApp().run()

