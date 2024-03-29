# Egypt-Japan University of Science and Technology
# Attention - Team E-JUSTians
# Driver Code
# ---
# import os
# os.environ["KIVY_NO_CONSOLELOG"] = "1"
import kivy
kivy.require('2.2.0')
# Kivy Packages
from kivy.config import Config
# Window Configuration
# Disable graphical annotation
Config.set('input', 'mouse', 'mouse,disable_multitouch')
# Config.set('graphics', 'resizable', 0)
# Config.set('graphics', 'borderless', 1)
from script.eyetracking.utilities import WINDOW_SIZE
from kivy.core.window import Window
Window.size = WINDOW_SIZE
Window.left = int((1366-WINDOW_SIZE[0])/2)
from kivy.app import App
from kivy.uix.screenmanager import (ScreenManager,
                                    FadeTransition)
# Screens
from include.screen import (splash,
                            login,
                            register)
# JSON Reading
import json

class Run(App):
    ''' Driver code for the application, contains a screen manager
    that controls which interface is shown to the user at a time.'''
    def build(self):
        self.screen_manager = ScreenManager(transition = FadeTransition())
        self.version_data = ""
        with open("app/include/config/settings.json") as json_file:
            self.version_data = json.load(json_file)
        self.db_cred = {}
        # File is omitted, added to .gitignore for security reasons. ^^
        # TODO: Repl`ace with an API that obtains the data.
        with open("app/include/config/sqlauth.json") as db_file:
                self.db_cred = json.load(db_file)
        # vv Stores current application user
        self.user = ""
        self.icon = "doc/icons/attention_icon.png"
        self.title = self.get_title()
        self.splash = splash.Splash(name="Splash Screen")
        self.login = login.Login(name="Login Page")
        self.register = register.Register(name="Register Page")
        screens = [
                    self.splash,
                    self.login,
                    self.register,
                    ]
        for screen in screens:
            self.screen_manager.add_widget(screen)
        return self.screen_manager
    
    def get_title(self):
        ''' Build the title for the current version of the application.'''
        return "Attention\t-\t"+str(self.version_data['version'])\
            +"\t-\t"+str(self.version_data['config'][0]['date'])
    
    def open_settings(self, *largs):
        pass

if __name__ == '__main__':
    main = Run()
    main.run()