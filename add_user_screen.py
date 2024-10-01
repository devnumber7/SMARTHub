# add_user_screen.py

from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.uix.popup import Popup
import logging
import threading
import os

# Import the backend class
from backend import PiVPNBackend

class AddUserScreen(Screen):
    """
    Add User Screen with input for VPN username and navigation buttons.
    """
    def __init__(self, **kwargs):
        super(AddUserScreen, self).__init__(**kwargs)
        
        # Initialize the backend
        self.backend = PiVPNBackend()
        
        # Create the layout with a grey background
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        
        # Path to the custom font
        current_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(current_dir, 'fonts', 'SixtyFourConvergence.ttf')  # Ensure the extension is included
        
        # Add a prompt label with custom font
        prompt_label = Label(
            text='Enter username for your VPN client profile',
            font_size='20sp',
            color=(0, 0, 0, 1),  # Black text
            font_name=font_path,  # Custom font
            size_hint=(1, 0.3)
        )
        layout.add_widget(prompt_label)
        
        # Add TextInput for username with custom styling
        self.username_input = TextInput(
            hint_text='Username',
            multiline=False,
            size_hint=(0.6, 0.2),
            pos_hint={'center_x': 0.5},
            font_name=font_path,  # Apply custom font to input text
            font_size='18sp',
            background_normal='',  # Remove default background
            background_active='',  # Remove background when active
            foreground_color=(1, 1, 1, 1),  # White text
            background_color=(0, 0, 0, 1)  # Black background
        )
        layout.add_widget(self.username_input)
        
        # Add Submit button with custom font
        submit_button = Button(
            text='Submit',
            size_hint=(0.3, 0.2),
            pos_hint={'center_x': 0.5},
            font_name=font_path,  # Apply custom font to button text
            font_size='18sp'
        )
        submit_button.bind(on_press=self.submit_username)
        layout.add_widget(submit_button)
        
        # Add Back button to return to Home Screen
        back_button = Button(
            text='Back',
            size_hint=(0.3, 0.2),
            pos_hint={'center_x': 0.5},
            background_color=(1, 0, 0, 1),  # Red color for emphasis
            font_name=font_path,  # Apply custom font to button text
            font_size='18sp'
        )
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        
        self.add_widget(layout)
    
    def submit_username(self, instance):
        """
        Handles the submission of the username.
        Validates input and provides feedback.
        """
        username = self.username_input.text.strip()
        if username:
            logging.debug(f"Username entered: {username}")
            # Disable the submit button to prevent multiple clicks
            instance.disabled = True
            # Start a new thread to handle backend processing
            threading.Thread(target=self.process_add_user, args=(username, instance), daemon=True).start()
        else:
            logging.debug("No username entered")
            self.display_submission_failure()
    
    def process_add_user(self, username, submit_button):
        """
        Processes adding a user in the backend.
        Runs in a separate thread to prevent UI blocking.
        """
        # Call the backend to add the user
        result = self.backend.add_user(username)
        
        # Schedule the UI update on the main thread
        Clock.schedule_once(lambda dt: self.handle_backend_response(result, submit_button), 0)
    
    def handle_backend_response(self, result, submit_button):
        """
        Handles the response from the backend and updates the UI accordingly.
        """
        # Re-enable the submit button
        submit_button.disabled = False
        
        if result['success']:
            self.display_submission_success(result['message'])
        else:
            self.display_submission_failure(result['message'])
    
    def display_submission_success(self, message):
        """
        Displays a success message after successful submission.
        """
        # Create content for the popup
        popup_content = BoxLayout(orientation='vertical', padding=20, spacing=20)
        success_label = Label(text=message, font_size='18sp', color=(0, 0.5, 0, 1))
        close_button = Button(text='Close', size_hint=(1, 0.2), font_size='18sp', font_name=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts', 'SixtyFourConvergence.ttf'))
        popup_content.add_widget(success_label)
        popup_content.add_widget(close_button)
        
        # Create and open the popup
        popup = Popup(title='Success',
                      content=popup_content,
                      size_hint=(0.8, 0.4))
        
        # Bind the close button to dismiss the popup
        close_button.bind(on_press=popup.dismiss)
        popup.open()
    
    def display_submission_failure(self, message="Please enter a valid username."):
        """
        Displays an error message if the username input is invalid.
        """
        # Create content for the popup
        popup_content = BoxLayout(orientation='vertical', padding=20, spacing=20)
        error_label = Label(text=message, font_size='18sp', color=(0.8, 0, 0, 1))
        close_button = Button(text='Close', size_hint=(1, 0.2), font_size='18sp', font_name=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts', 'SixtyFourConvergence.ttf'))
        popup_content.add_widget(error_label)
        popup_content.add_widget(close_button)
        
        # Create and open the popup
        popup = Popup(title='Error',
                      content=popup_content,
                      size_hint=(0.8, 0.4))
        
        # Bind the close button to dismiss the popup
        close_button.bind(on_press=popup.dismiss)
        popup.open()
    
    def go_back(self, instance):
        """
        Navigates back to the Home Screen with a slide transition.
        """
        logging.debug("Returning to HomeScreen")
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'home'
