from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

# Splash Screen class
class SplashScreen(Screen):
    def on_enter(self):
        # Automatically switch to the main screen after 3 seconds
        Clock.schedule_once(self.switch_to_main, 3)

    def switch_to_main(self, dt):
        self.manager.current = 'main'

# Main Screen class
class MainScreen(Screen):
    pass

# Screen Manager to control navigation between screens
class ScreenManagement(ScreenManager):
    pass

# Main App Class
class MyApp(App):
    def build(self):
        return ScreenManagement()

if __name__ == '__main__':
    MyApp().run()
