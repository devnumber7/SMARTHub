# home_screen.py

from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
import logging
import os

class HomeScreen(Screen):
    """
    Home Screen with a welcome message and an 'Add a User' button.
    """
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        
        # Create the layout with a grey background
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        
        # Add a welcome label
        welcome_label = Label(
            text='WELCOME TO SMART HUB',
            font_size='24sp',
            color=(1, 1, 1, 1), 
            size_hint=(1, 0.3),
            font_name = 'fonts/SixtyFourConvergence'
        )
        layout.add_widget(welcome_label)
        
        # Add 'Add a User' button
        add_user_button = Button(
            text='Add a User',
            size_hint=(0.3, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            font_name = 'fonts/SixtyFourConvergence'
        )
        add_user_button.bind(on_press=self.navigate_to_add_user)
        layout.add_widget(add_user_button)
        
        self.add_widget(layout)
    
    def navigate_to_add_user(self, instance):
        """
        Navigates to the AddUserScreen with a slide transition.
        """
        logging.debug("Navigating to AddUserScreen")
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'add_user'
