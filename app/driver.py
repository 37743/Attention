# Egypt-Japan University of Science and Technology
# Attention - Team E-JUSTians
# Driver Code
# ---
import kivy
kivy.require('2.2.0')
# Kivy Packages
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, WipeTransition
from kivy.core.window import Window
from kivy.config import Config
from include.screen import splash
import json
# Disable graphical annotation
Config.set('input', 'mouse', 'mouse,disable_multitouch')
# Window, resizeable
Window.size = (1024, 640)
Window.minimum_width = 820
Window.minimum_height = 512

class Run(App):
    ''' Driver code for the application, contains a screen manager
    that controls which interface is shown to the user at a time.'''
    def build(self):
        self.screen_manager = ScreenManager(transition = WipeTransition())
        self.version_data = ""
        with open("app/include/config/settings.json") as json_file:
            self.version_data = json.load(json_file)
        self.icon = "doc/icons/attention_icon.png"
        self.title = self.get_title()
        self.splash = splash.Splash()
        screens = [self.splash]
        for screen in screens:
            self.screen_manager.add_widget(screen)
        return self.screen_manager
    def get_title(self):
        ''' Build the title for the current version of the application.'''
        return "Attention\t-\t"+str(self.version_data['version'])\
            +"\t-\t"+str(self.version_data['config'][0]['date'])
if __name__ == '__main__':
    main = Run()
    main.run()