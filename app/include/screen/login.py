# Egypt-Japan University of Science and Technology
# Attention - Team E-JUSTians
# Login Screen
# ---
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from script.EyeTracking.utilities import (DOSIS_FONT,
                                          YAHEI_FONT,
                                          GRAY,
                                          CYAN,
                                          PURPLE)
from kivy.core.text import LabelBase

def change_to_screen(*args, screen):
    App.get_running_app().screen_manager.current = screen
    return

class Login(Screen, FloatLayout):
    def _update_bg(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size

    def _login_released(self, instance):
        pass

    def __init__(self, **kwargs):
        super(Login, self).__init__(**kwargs)
        with self.canvas.before:
            self.bg = Rectangle(source="doc/images/login_shapes/Background.png",
                                size=self.size,
                                pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)
        LabelBase.register(name='Dosis', fn_regular=DOSIS_FONT)
        LabelBase.register(name='YaHei', fn_regular=YAHEI_FONT)
        self.bw_logo = Image(source="doc/icons/logo_B&W.png",
                            size_hint=(None,None),
                            size=(90,90),
                            pos_hint={"center_x": .06, "center_y": .91})
        self.add_widget(self.bw_logo)
        # Decorative Circles
        self.circles_decor = FloatLayout()
        self.c1 = Image(source="doc/icons/C1.png",
                                size_hint=(None,None),
                                size=(200,200),
                                allow_stretch=True,
                                keep_ratio=True,
                                pos_hint={"center_x": .36, "center_y": .24})
        self.circles_decor.add_widget(self.c1)
        self.c2 = Image(source="doc/icons/C2.png",
                                size_hint=(None,None),
                                size=(250,250),
                                allow_stretch=True,
                                keep_ratio=True,
                                pos_hint={"center_x": .7, "center_y": .56})
        self.circles_decor.add_widget(self.c2)
        self.add_widget(self.circles_decor)
        # Login Header Text
        self.login_text = BoxLayout(orientation="vertical",
                                      size_hint=(None,None),
                                      size=(500,80),
                                      spacing=-10,
                                      pos_hint={'center_x': .5, 'center_y': .81},)
        self.login_title = Label(text="Welcome back",
                                  font_name="Dosis",
                                  color=PURPLE,
                                  font_size=36,
                                  halign='center')
        self.login_text.add_widget(self.login_title)
        self.login_subtitle = Label(text="Enter your details below",
                                  font_name="YaHei",
                                  color=GRAY,
                                  font_size=16,
                                  halign='center')
        self.login_text.add_widget(self.login_subtitle)
        self.login_panel = Image(source="doc/images/login_shapes/login_reg.png",
                                size_hint=(None,None),
                                size=(300,360),
                                pos_hint={"center_x": .5, "center_y": .46},
                                allow_stretch=True,
                                keep_ratio=True,
                                opacity=.7)
        self.add_widget(self.login_panel)
        # Login Details
        self.login_layout = BoxLayout(orientation="vertical",
                                size_hint=(None,None),
                                size=(300,225),
                                spacing=-40,
                                pos_hint={'center_x': .5, 'center_y': .57},)
        self.user_label = Label(text="Username",
                                font_name="YaHei",
                                color=GRAY,
                                font_size=13,
                                halign='left',
                                pos_hint={'center_x': .24, 'center_y': .5})
        self.login_layout.add_widget(self.user_label)
        self.user_box = TextInput(multiline=False,
                                size_hint = (.75,.4),
                                font_name="YaHei",
                                cursor_color=GRAY,
                                font_size=13,
                                foreground_color=GRAY,
                                write_tab=False,
                                padding=(10,15),
                                hint_text = "",
                                background_normal="doc/images/login_shapes/TextBox.png",
                                background_active="doc/images/login_shapes/TextBox_active.png",
                                pos_hint={'center_x': .5, 'center_y': .5})
        self.login_layout.add_widget(self.user_box)
        self.pass_label = Label(text="Password",
                                font_name="YaHei",
                                color=GRAY,
                                font_size=13,
                                halign='left',
                                pos_hint={'center_x': .24, 'center_y': .5})
        self.login_layout.add_widget(self.pass_label)
        self.pass_box = TextInput(multiline=False,
                                size_hint = (.75,.4),
                                font_name="YaHei",
                                password=True,
                                cursor_color=GRAY,
                                font_size=13,
                                foreground_color=GRAY,
                                write_tab=False,
                                padding=(10,15),
                                hint_text = "",
                                background_normal="doc/images/login_shapes/TextBox.png",
                                background_active="doc/images/login_shapes/TextBox_active.png",
                                pos_hint={'center_x': .5, 'center_y': .5})
        self.login_layout.add_widget(self.pass_box)
        # Login & Create Account Button(s)
        self.login_button = Button(text="LOGIN", color = "ffffff",
                            font_name="Dosis",
                            size_hint=(None,None),
                            size=(140,37),
                            font_size=16,
                            pos_hint={'center_x': .5, 'center_y': .33},
                            background_normal=
                            "doc/images/login_shapes/Btn1.png",
                            background_down=
                            "doc/images/login_shapes/Btn1_down.png")
        self.login_button.bind(on_release=self._login_released)
        self.register_button = Button(text="Create an account", color = GRAY,
                            font_name="Dosis",
                            size_hint=(None,None),
                            size=(125,30),
                            font_size=14,
                            pos_hint={'center_x': .5, 'center_y': .27},
                            background_normal=
                            "doc/images/login_shapes/Btn_invis.png",
                            background_down=
                            "doc/images/login_shapes/Btn_invis.png")
        self.add_widget(self.login_text)
        self.add_widget(self.login_layout)
        self.add_widget(self.login_button)
        self.add_widget(self.register_button)
        self.footer = Label(text="EGYPT-JAPAN UNIVERSITY OF SCIENCE AND TECHNOLOGY x BENHA UNIVERSITY HACKATHON - 2024",
                             color = PURPLE,
                             font_name="Dosis",
                             pos_hint={"center_x": .5, "center_y": .04},
                             font_size=11)
        self.add_widget(self.footer)