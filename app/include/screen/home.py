# Egypt-Japan University of Science and Technology
# Attention - Team E-JUSTians
# Login Screen
# ---
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.behaviors import ToggleButtonBehavior
from script.EyeTracking.utilities import (DOSIS_FONT,
                                          YAHEI_FONT,
                                          GRAY,
                                          CYAN,
                                          PURPLE)
from kivy.core.text import LabelBase
from kivy.animation import Animation
from functools import partial
from kivy.clock import Clock

def change_to_screen(*args, screen):
    App.get_running_app().screen_manager.current = screen
    return

def hide_layout(*args, self, layout):
    hide = Animation(pos_hint={'center_x':5,'center_y':.5}, t='in_cubic', d=2)
    hide &= Animation(opacity=0, t='in_cubic', d=1)
    layout = "self."+str(layout)+"_layout"
    exec(f"hide.start({layout})")

def show_layout(*args, self, layout):
    show = Animation(pos_hint={'center_x':.5,'center_y':.5}, t='out_cubic', d=2)
    show &= Animation(opacity=1, t='in_cubic', d=2)
    layout = "self."+str(layout)+"_layout"
    exec(f"show.start({layout})")

class ToggleButton(ToggleButtonBehavior, Image):
    def __init__(self, instance=None, **kwargs):
        super(ToggleButton, self).__init__(**kwargs)
        if instance == "home":
            self.state = 'down'
            self.source = 'doc/images/Home_page_shapes/SquareBtn_shadow.png'
        else:
            self.source = 'doc/images/Home_page_shapes/SquareBtn_invis.png'

    def on_state(self, instance, value):
        if value == 'down':
            self.disabled = True
            self.source = 'doc/images/Home_page_shapes/SquareBtn_shadow.png'
        else:
            self.disabled = False
            self.source = 'doc/images/Home_page_shapes/SquareBtn_invis.png'

class Home(Screen, FloatLayout):
    def _update_bg(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size
    
    def _navigate(self, instance, final):
        init = self._get_curr()
        self._set_curr(new_curr=final)
        hide_layout(self=self, layout=init)
        show_layout(self=self, layout=final)

    def _set_curr(self, new_curr):
        self.curr = new_curr

    def _get_curr(self):
        return self.curr
    
    def __init__(self, **kwargs):
        super(Home, self).__init__(**kwargs)
        with self.canvas.before:
            self.bg = Rectangle(source="doc/images/Home_page_shapes/Background.png",
                                size=self.size,
                                pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)
        LabelBase.register(name='Dosis', fn_regular=DOSIS_FONT)
        LabelBase.register(name='YaHei', fn_regular=YAHEI_FONT)
        self.bw_logo = Image(source="doc/icons/logo_B&W_small.png",
                            size_hint=(None,None),
                            pos_hint={"center_x": .06, "center_y": .91})
        self.add_widget(self.bw_logo)
        # Navigation Bar
        self.curr = "home"
        self.nav_bar = BoxLayout(orientation="vertical",
                                 size_hint=(1,.5),
                                 pos_hint={"center_x": .05, "center_y": .5})
        # Home Navigation
        self.home_nav = FloatLayout()
        self.home_but = ToggleButton(group="nav",
                                     instance="home",
                                     size_hint=(None,None),
                                     size=(52,56),
                                     state="down",
                                     pos_hint={'center_x': .5, 'center_y': .5})
        self.home_but.bind(on_release=partial(self._navigate,
                                              final="home"))
        self.home_icon = Image(source="doc/icons/home.png",
                                size_hint=(None,None),
                                size=(50,50),
                                pos_hint={"center_x": .5, "center_y": .5})
        # Add Navigation
        self.add_nav = FloatLayout()
        self.add_but = ToggleButton(group="nav",
                                    size_hint=(None,None),
                                    size=(52,56),
                                    pos_hint={'center_x': .5, 'center_y': .5})
        self.add_but.bind(on_release=partial(self._navigate,
                                              final="add"))
        self.add_icon = Image(source="doc/icons/add.png",
                                size_hint=(None,None),
                                pos_hint={"center_x": .5, "center_y": .5})
        # Star Navigation
        self.star_nav = FloatLayout()
        self.star_but = ToggleButton(group="nav",
                                     size_hint=(None,None),
                                     size=(52,56),
                                     pos_hint={'center_x': .5, 'center_y': .5})
        self.star_but.bind(on_release=partial(self._navigate,
                                              final="star"))
        self.star_icon = Image(source="doc/icons/star.png",
                                size_hint=(None,None),
                                pos_hint={"center_x": .5, "center_y": .5})
        # Profile Navigation
        self.profile_nav = FloatLayout()
        self.profile_but = ToggleButton(group="nav",
                                        size_hint=(None,None),
                                        size=(52,56),
                                        pos_hint={'center_x': .5, 'center_y': .5})
        self.profile_but.bind(on_release=partial(self._navigate,
                                              final="profile"))
        self.profile_icon = Image(source="doc/icons/profile.png",
                                size_hint=(None,None),
                                pos_hint={"center_x": .5, "center_y": .5})
        # Home Layout
        self.home_layout = FloatLayout(pos_hint={"center_x": .5, "center_y": .5})
        self.home_panel = Image(source="app/doc/images/Home_page_shapes/panel_reg.png",
                                size_hint=(None,None),
                                size=(500,500),
                                pos_hint={"center_x": .5, "center_y": .5})
        self.home_title = Label(text="Home Panel Test",
                                  font_name="Dosis",
                                  color=PURPLE,
                                  font_size=36,
                                  halign='center',
                                  pos_hint={"center_x": .5, "center_y": .5})
        # Add Material Layout
        self.add_layout = FloatLayout(pos_hint={"center_x": 5, "center_y": .5},
                                      opacity=0)
        self.add_panel = Image(source="app/doc/images/Home_page_shapes/panel_reg.png",
                                size_hint=(None,None),
                                size=(500,500),
                                pos_hint={"center_x": .5, "center_y": .5})
        self.add_title = Label(text="Add Material Panel Test",
                                  font_name="Dosis",
                                  color=PURPLE,
                                  font_size=36,
                                  halign='center',
                                  pos_hint={"center_x": .5, "center_y": .5})
        # Star Layout
        self.star_layout = FloatLayout(pos_hint={"center_x": 5, "center_y": .5},
                                      opacity=0)
        self.star_panel = Image(source="app/doc/images/Home_page_shapes/panel_reg.png",
                                size_hint=(None,None),
                                size=(500,500),
                                pos_hint={"center_x": .5, "center_y": .5})
        self.star_title = Label(text="Star Panel Test",
                                  font_name="Dosis",
                                  color=PURPLE,
                                  font_size=36,
                                  halign='center',
                                  pos_hint={"center_x": .5, "center_y": .5})
        # Profile Layout
        self.profile_layout = FloatLayout(pos_hint={"center_x": 5, "center_y": .5},
                                      opacity=0)
        self.profile_panel = Image(source="app/doc/images/Home_page_shapes/panel_reg.png",
                                size_hint=(None,None),
                                size=(500,500),
                                pos_hint={"center_x": .5, "center_y": .5})
        self.profile_title = Label(text="Profile Panel Test",
                                  font_name="Dosis",
                                  color=PURPLE,
                                  font_size=36,
                                  halign='center',
                                  pos_hint={"center_x": .5, "center_y": .5})
        for widget in ["home","add","star","profile"]:
            exec(f"self.{widget}_nav.add_widget(self.{widget}_but)")
            exec(f"self.{widget}_nav.add_widget(self.{widget}_icon)")
            exec(f"self.nav_bar.add_widget(self.{widget}_nav)")
            exec(f"self.{widget}_layout.add_widget(self.{widget}_panel)")
            exec(f"self.{widget}_layout.add_widget(self.{widget}_title)")
            exec(f"self.add_widget(self.{widget}_layout)")
        self.add_widget(self.nav_bar)
        self.footer = Label(text="EGYPT-JAPAN UNIVERSITY OF SCIENCE AND TECHNOLOGY x BENHA UNIVERSITY HACKATHON - 2024",
                             color = PURPLE,
                             font_name="Dosis",
                             pos_hint={"center_x": .5, "center_y": .04},
                             font_size=11)
        self.add_widget(self.footer)