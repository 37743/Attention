# Egypt-Japan University of Science and Technology
# Attention - Team E-JUSTians
# Login Screen
# ---
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle
from kivy.uix.button import Button
from kivy.uix.label import Label
from script.EyeTracking.utilities import DOSIS_FONT, YAHEI_FONT, CYAN, PURPLE
from kivy.core.text import LabelBase

def change_to_screen(*args, screen):
    App.get_running_app().screen_manager.current = screen
    return

class Login(Screen, FloatLayout):
    def _update_bg(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size

    def __init__(self, **kwargs):
        super(Login, self).__init__(**kwargs)
        with self.canvas.before:
            self.bg = Rectangle(source="doc/images/login_shapes/Background.png",
                                size=self.size,
                                pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)
        LabelBase.register(name='Dosis', fn_regular=DOSIS_FONT)
        LabelBase.register(name='YaHei', fn_regular=YAHEI_FONT)

        self.footer = Label(text="EGYPT-JAPAN UNIVERSITY OF SCIENCE AND TECHNOLOGY x BENHA UNIVERSITY HACKATHON - 2024",
                             color = PURPLE,
                             font_name="Dosis",
                             pos_hint={"center_x": .5, "center_y": .04},
                             font_size=11)
        self.add_widget(self.footer)