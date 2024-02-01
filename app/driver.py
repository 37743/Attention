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
# Disable graphical annotation
Config.set('input', 'mouse', 'mouse,disable_multitouch')
Config.set('graphics', 'resizable', 0)
# Config.set('graphics', 'borderless', 1)
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window
# Screens
from include.screen import splash
from include.screen import login
# JSON Reading
import json
# Eyetracker
# from script.EyeTracking.cv import GazeTracker
from script.EyeTracking.utilities import WINDOW_SIZE
Window.size = WINDOW_SIZE
Window.left = int((1366-WINDOW_SIZE[0])/2)
import threading

def thread(function):
    def wrap(*args, **kwargs):
        t = threading.Thread(target=function, args=args, kwargs=kwargs, daemon=True)
        t.start()
        return t
    return wrap

class Run(App):
    ''' Driver code for the application, contains a screen manager
    that controls which interface is shown to the user at a time.'''
    def build(self):
        # self.do_stuff()
        self.screen_manager = ScreenManager(transition = FadeTransition())
        self.version_data = ""
        with open("app/include/config/settings.json") as json_file:
            self.version_data = json.load(json_file)
        self.icon = "doc/icons/attention_icon.png"
        self.title = self.get_title()
        self.splash = splash.Splash(name="Splash Screen")
        self.login = login.Login(name="Login Page")
        screens = [self.splash, self.login]
        for screen in screens:
            self.screen_manager.add_widget(screen)
        return self.screen_manager
    
    # @thread
    # def do_stuff(self):
    #     ''' TODO: Use this part elsewhere '''
    #     et = GazeTracker()
    
    def get_title(self):
        ''' Build the title for the current version of the application.'''
        return "Attention\t-\t"+str(self.version_data['version'])\
            +"\t-\t"+str(self.version_data['config'][0]['date'])
    
if __name__ == '__main__':
    main = Run()
    main.run()