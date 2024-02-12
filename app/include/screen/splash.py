# Egypt-Japan University of Science and Technology
# Attention - Team E-JUSTians
# Splash Screen
# ---
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from script.eyetracking.utilities import (DOSIS_FONT,
                                          YAHEI_FONT)
from kivy.core.text import LabelBase
from kivy.clock import (mainthread,
                        Clock)
from kivy.animation import Animation
import threading
import time

def change_to_screen(*args, screen):
    ''' Changes the current screen in the Kivy application'''
    App.get_running_app().screen_manager.current = screen
    return

def thread(function):
    ''' Creates a new thread with a process using the input function'''
    def wrap(*args, **kwargs):
        t = threading.Thread(target=function, args=args, kwargs=kwargs, daemon=True)
        t.start()
        return t
    return wrap

class Splash(Screen, FloatLayout):
    ''' Represents the Splash Screen'''
    def _update_bg(self, instance, value):
        ''' Updates the background size and position
          based on the screen size'''
        self.bg.pos = instance.pos
        self.bg.size = instance.size

    def _load_program(self, instance):
        ''' Simulates a loading process with a placeholder time delay'''
        self.logobutton.disabled = True
        start_time = time.time()
        end_time = start_time + 6  # 6 seconds
        # TODO: Load actual material instead of placebo waiting time.
        self._update_loading_pct(start_time, end_time)
    
    @mainthread
    def _update_pct(self, new_pct):
        self.loading_text.text = "Loading.. {p}%".format(p=new_pct)

    @thread
    def _update_loading_pct(self, start_time, end_time, *args):
        ''' Updates the loading text label with the current progress percentage'''
        now = time.time()
        while now < end_time:
            prog_pct = min(100, round((time.time() - start_time) * 100 / (end_time - start_time)))
            self._update_pct(prog_pct)
            if (prog_pct == 100):
                print(prog_pct)
                splashanim = Animation(size=(1500,1500), t="in_back", d=2)
                splashanim.start(self.circle_fade)
                Clock.schedule_once(lambda dt: change_to_screen(screen="Login Page"), 3)
                break

    def _login_released(self, instance):
        '''  Triggers on button release, 
        starting an animation and changing the screen after a delay'''
        if (self.loading_text.text[-4:] == "100%"):
            splashanim = Animation(size=(1500,1500), t="in_back", d=2)
            splashanim.start(self.circle_fade)
            Clock.schedule_once(lambda dt: change_to_screen(screen="Login Page"), 4)
            self.check_click.cancel()

    def _login_thread(self, instance):
        ''' Start loading up the program, including database connection'''
        login_thread = threading.Thread(target=self._load_program)
        login_thread.start()

    def __init__(self, **kwargs):
        ''' Sets up UI elements and registering fonts'''
        super(Splash, self).__init__(**kwargs)
        with self.canvas.before:
            self.bg = Rectangle(source="doc/images/splash_screen/BG.png",
                                size=self.size,
                                pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)
        LabelBase.register(name='Dosis', fn_regular=DOSIS_FONT)
        LabelBase.register(name='YaHei', fn_regular=YAHEI_FONT)
        self.logobutton = Button(size_hint=(None,None),
                                 size=(353,255),
                                 pos_hint={"center_x": .5, "center_y": .6},
                                 background_normal="doc/icons/logo_c.png",
                                 background_disabled_normal="doc/icons/logo_c.png",
                                 background_down="doc/icons/logo_B&W.png")
        self.logobutton.bind(on_release=self._load_program)
        self.loading_text = Label(text="Press to boot-up!",
                                  font_name="Dosis",
                                  color="ffffff",
                                  font_size=24,
                                  pos_hint={'center_x': .5, 'center_y': .35},
                                  halign='center')
        self.add_widget(self.logobutton)
        self.add_widget(self.loading_text)
        self.footer = Label(text="EGYPT-JAPAN UNIVERSITY OF SCIENCE AND TECHNOLOGY x BENHA UNIVERSITY HACKATHON - 2024",
                             color = "ffffff",
                             font_name="Dosis",
                             pos_hint={"center_x": .5, "center_y": .04},
                             font_size=11)
        self.add_widget(self.footer)
        self.circle_fade = Image(source="doc/icons/C3.png",
                                size_hint=(None,None),
                                size=(0,0),
                                opacity=1,
                                allow_stretch=True,
                                pos_hint={"center_x": .5, "center_y": .5})
        self.circle_fade.texture.mag_filter = 'nearest'
        self.add_widget(self.circle_fade)