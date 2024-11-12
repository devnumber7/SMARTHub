# active_vpn_screen.py

from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
import logging
import threading
import os

# Import the backend class
from vpn_status import VPNStatusChecker

class ActiveVPNScreen(Screen):
    """
    Screen to display active VPN connections.
    """
    def __init__(self, **kwargs):
        super(ActiveVPNScreen, self).__init__(**kwargs)

        # Initialize the backend
        self.vpn_status_checker = VPNStatusChecker()

        # Path to the custom font
        current_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(current_dir, 'fonts', 'SixtyFourConvergence.ttf')

        # Create the main layout
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)

        # Add a title label
        title_label = Label(
            text='Active VPN Connections',
            font_size='24sp',
            color=(1, 1, 1, 1),
            size_hint=(1, 0.1),
            font_name=font_path
        )
        layout.add_widget(title_label)

        # Add a ScrollView to display the list of active connections
        self.scroll_view = ScrollView(size_hint=(1, 0.8))
        self.connections_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        self.connections_layout.bind(minimum_height=self.connections_layout.setter('height'))
        self.scroll_view.add_widget(self.connections_layout)
        layout.add_widget(self.scroll_view)

        # Add a Back button to return to the Home Screen
        back_button = Button(
            text='Back',
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5},
            font_name=font_path
        )
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

        # Flag to prevent multiple threads
        self.is_fetching = False

    def on_enter(self):
        """
        Called when the screen is displayed. Starts the periodic update.
        """
        logging.debug("ActiveVPNScreen entered, starting periodic updates.")
        # Start updating every 5 seconds
        self.update_event = Clock.schedule_interval(self.load_active_connections, 5)
        # Load connections immediately
        self.load_active_connections()

    def on_leave(self):
        """
        Called when the screen is left. Stops the periodic update.
        """
        logging.debug("ActiveVPNScreen left, stopping periodic updates.")
        if hasattr(self, 'update_event'):
            self.update_event.cancel()

    def load_active_connections(self, *args):
        """
        Loads the list of active VPN connections from the backend.
        """
        if not self.is_fetching:
            threading.Thread(target=self.fetch_active_connections, daemon=True).start()

    def fetch_active_connections(self):
        """
        Fetches the active VPN connections and updates the UI.
        """
        self.is_fetching = True
        active_connections = self.vpn_status_checker.get_active_vpn_clients()
        Clock.schedule_once(lambda dt: self.display_connections(active_connections), 0)
        self.is_fetching = False

    def display_connections(self, connections):
        """
        Displays the list of active VPN connections in the UI.
        """
        self.connections_layout.clear_widgets()

        if connections:
            for connection in connections:
                # Create a BoxLayout for each connection to display multiple details
                connection_box = BoxLayout(orientation='vertical', size_hint_y=None, height=100, padding=10, spacing=5)

                # Display IP Address
                ip_label = Label(
                    text=f"IP Address: {connection['ip_address']}",
                    font_size='16sp',
                    color=(1, 1, 1, 1),
                    halign='left',
                    valign='middle',
                    size_hint=(1, 0.3),
                    font_name=os.path.join(
                        os.path.dirname(os.path.abspath(__file__)),
                        'fonts',
                        'SixtyFourConvergence.ttf'
                    )
                )
                ip_label.bind(size=ip_label.setter('text_size'))
                connection_box.add_widget(ip_label)

                # Display Endpoint
                endpoint_label = Label(
                    text=f"Endpoint: {connection['endpoint']}",
                    font_size='16sp',
                    color=(1, 1, 1, 1),
                    halign='left',
                    valign='middle',
                    size_hint=(1, 0.3),
                    font_name=os.path.join(
                        os.path.dirname(os.path.abspath(__file__)),
                        'fonts',
                        'SixtyFourConvergence.ttf'
                    )
                )
                endpoint_label.bind(size=endpoint_label.setter('text_size'))
                connection_box.add_widget(endpoint_label)

                # Display Latest Handshake
                handshake_label = Label(
                    text=f"Last Handshake: {connection['latest_handshake']}",
                    font_size='16sp',
                    color=(1, 1, 1, 1),
                    halign='left',
                    valign='middle',
                    size_hint=(1, 0.3),
                    font_name=os.path.join(
                        os.path.dirname(os.path.abspath(__file__)),
                        'fonts',
                        'SixtyFourConvergence.ttf'
                    )
                )
                handshake_label.bind(size=handshake_label.setter('text_size'))
                connection_box.add_widget(handshake_label)

                self.connections_layout.add_widget(connection_box)
        else:
            no_connection_label = Label(
                text='No active VPN connections.',
                font_size='18sp',
                color=(1, 1, 1, 1),
                size_hint=(1, 0.2),
                font_name=os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    'fonts',
                    'SixtyFourConvergence.ttf'
                )
            )
            self.connections_layout.add_widget(no_connection_label)

    def go_back(self, instance):
        """
        Navigates back to the Home Screen with a slide transition.
        """
        logging.debug("Returning to HomeScreen")
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'home'
