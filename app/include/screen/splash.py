# Egypt-Japan University of Science and Technology
# Attention - Team E-JUSTians
# Splash Screen
# ---
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle

class Splash(Screen, FloatLayout):
    ''' Splash screen for the application,
    connected to the login/main menu screen.'''
    def _update_bg(self, instance, value):
        ''' Synchronizes background with window dimensions.'''
        self.bg.pos = instance.pos
        self.bg.size = instance.size

    def __init__(self, **kwargs):
        ''' Code to-be run when the Splash object is called.'''
        super(Splash, self).__init__(**kwargs)
        with self.canvas.before:
            self.bg = Rectangle(source = "doc/icons/attention_icon.png",
                                size = self.size,
                                pos = self.pos)
        self.bind(size = self._update_bg, pos = self._update_bg)