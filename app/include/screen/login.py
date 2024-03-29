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
from script.eyetracking.utilities import (DOSIS_FONT,
                                          YAHEI_FONT,
                                          GRAY,
                                          CYAN,
                                          PURPLE)
from kivy.animation import Animation
from kivy.core.text import LabelBase
# MariaDB connector
import mysql.connector
from kivy.clock import Clock
from include.screen import home

def change_to_screen(*args, screen):
    App.get_running_app().screen_manager.current = screen
    return

class Login(Screen, FloatLayout):
    def _update_bg(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size

    def _login_error(self):
        ''' Shakes the layout, played when
        credentials are false'''
        list = [self.login_panel,self.login_layout,
                self.login_button,self.register_button]
        for widget in list:
            shake = Animation(pos_hint={"center_x": .51,
                                        "center_y": widget.pos_hint['center_y']},
                                        t="in_out_elastic", d=.5)\
                    + Animation(pos_hint={"center_x": .49,
                                        "center_y": widget.pos_hint['center_y']},
                                        t="in_out_elastic", d=.5)\
                    + Animation(pos_hint={"center_x": .5,
                                        "center_y": widget.pos_hint['center_y']},
                                        t="in_out_elastic", d=.5)
            shake.start(widget)

    def _register_released(self, instance):
        ''' Hides login panel and moves the decoration before 
        changing screen to the register page'''
        list = [self.login_panel,self.login_layout,
                self.login_result,self.login_button,
                self.register_button,self.login_text]
        for widget in list:
            shake = Animation(opacity=0, t="in_cubic", d=1)
            shake.start(widget)
        circles = [self.c1, self.c2]
        for widget in circles:
            if widget == self.c1:
                factor = -.05
            else:
                factor = .05
            move = Animation(pos_hint={"center_x": widget.pos_hint['center_x']+factor,
                                        "center_y":widget.pos_hint['center_y']+factor},
                                        t="in_out_cubic", d=1)
            move.start(widget)
            Clock.schedule_once(lambda dt: change_to_screen(screen="Register Page"), 2)
            Clock.schedule_once(self._return_obj, 3)

    def _return_obj(self, instance):
        ''' Reverse of \'_register_released,\'
          returns all widgets to place with full opacity'''
        list = [self.login_panel,self.login_layout,
        self.login_result,self.login_button,
        self.register_button,self.login_text]
        for widget in list:
            shake = Animation(opacity=1, t="in_cubic", d=1)
            shake.start(widget)
        circles = [self.c1, self.c2]
        for widget in circles:
            if widget == self.c1:
                factor = .05
            else:
                factor = -.05
            move = Animation(pos_hint={"center_x": widget.pos_hint['center_x']+factor,
                                        "center_y":widget.pos_hint['center_y']+factor},
                                        t="in_out_cubic", d=1)
            move.start(widget)

    def _login_released(self, instance):
        ''' Connects to database and verifies the input credentials'''
        try:
            app = App.get_running_app()
            db_cred = app.db_cred
            cn = mysql.connector.connect(
                            user=db_cred['user'],
                            password=db_cred['password'],
                            host=db_cred['host'],
                            database=db_cred['database'])
            cr = cn.cursor()
            u, p= str(self.user_box.text), str(self.pass_box.text)
            cr.execute(f"SELECT verify_login(\'{u}\',\'{p}\') AS verify_login")
            if cr.fetchall()[0][0] == 1:
                self.login_result.text=f"Welcome, {u}!"
                app.user = u
                app.home = home.Home(name="Home Page")
                app.screen_manager.add_widget(app.home)
                Clock.schedule_once(lambda dt: change_to_screen(screen="Home Page"), 2)
            else:
                self.login_result.text="Invalid Credentials! Try again."
                self._login_error()
            cn.close()
        except mysql.connector.Error as e:
            self.login_result.text="Server is currently offline."
            self._login_error()
            print(f"{e}")

    def __init__(self, **kwargs):
        super(Login, self).__init__(**kwargs)
        with self.canvas.before:
            self.bg = Rectangle(source="doc/images/Login_shapes/Background.png",
                                size=self.size,
                                pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)
        LabelBase.register(name='Dosis', fn_regular=DOSIS_FONT)
        LabelBase.register(name='YaHei', fn_regular=YAHEI_FONT)
        self.bw_logo = Image(source="doc/icons/logo_B&W_small.png",
                            size_hint=(None,None),
                            pos_hint={"center_x": .06, "center_y": .91})
        self.add_widget(self.bw_logo)
        #region Decorative Circles
        self.circles_decor = FloatLayout()
        self.c1 = Image(source="doc/icons/C1.png",
                                size_hint=(None,None),
                                size=(200,200),
                                pos_hint={"center_x": .36, "center_y": .24}
                                )
        self.circles_decor.add_widget(self.c1)
        self.c2 = Image(source="doc/icons/C2.png",
                                size_hint=(None,None),
                                size=(250,250),
                                pos_hint={"center_x": .7, "center_y": .56}
                                )
        self.circles_decor.add_widget(self.c2)
        self.add_widget(self.circles_decor)
        #endregion
        #region Login Header Text
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
        self.login_panel = Image(source="doc/images/Login_shapes/Login_reg.png",
                                size_hint=(None,None),
                                size=(300,360),
                                pos_hint={"center_x": .5, "center_y": .46},
                                opacity=.7)
        self.add_widget(self.login_panel)
        #endregion
        #region Login Details
        self.login_layout = BoxLayout(orientation="vertical",
                                size_hint=(None,None),
                                size=(300,225),
                                padding=(0,15),
                                spacing=-40,
                                pos_hint={'center_x': .5, 'center_y': .57},)
        self.login_result = Label(text="Kindly enter your credentials.",
                                  font_name="Dosis",
                                  size_hint=(1,.6),
                                  color=CYAN,
                                  font_size=16,
                                  halign='center')
        self.login_layout.add_widget(self.login_result)
        self.user_label = Label(text="Username",
                                font_name="YaHei",
                                color=GRAY,
                                font_size=13,
                                halign='left',
                                pos_hint={'center_x': .24, 'center_y': .5})
        self.login_layout.add_widget(self.user_label)
        self.user_box = TextInput(text="",
                                  multiline=False,
                                  size_hint = (.75,.4),
                                  font_name="YaHei",
                                  cursor_color=GRAY,
                                  font_size=13,
                                  foreground_color=GRAY,
                                  write_tab=False,
                                  padding=(10,10),
                                  hint_text = "",
                                  background_normal="doc/images/Login_shapes/TextBox.png",
                                  background_active="doc/images/Login_shapes/TextBox_active.png",
                                  pos_hint={'center_x': .5, 'center_y': .5})
        self.login_layout.add_widget(self.user_box)
        self.pass_label = Label(text="Password",
                                font_name="YaHei",
                                color=GRAY,
                                font_size=13,
                                halign='left',
                                pos_hint={'center_x': .24, 'center_y': .5})
        self.login_layout.add_widget(self.pass_label)
        self.pass_box = TextInput(text="",
                                multiline=False,
                                size_hint = (.75,.4),
                                font_name="YaHei",
                                password=True,
                                cursor_color=GRAY,
                                font_size=13,
                                foreground_color=GRAY,
                                write_tab=False,
                                padding=(10,10),
                                hint_text = "",
                                background_normal="doc/images/Login_shapes/TextBox.png",
                                background_active="doc/images/Login_shapes/TextBox_active.png",
                                pos_hint={'center_x': .5, 'center_y': .5})
        self.login_layout.add_widget(self.pass_box)
        #endregion
        #region Login & Create Account Button(s)
        self.login_button = Button(text="LOGIN", color = "ffffff",
                            font_name="Dosis",
                            size_hint=(None,None),
                            size=(140,37),
                            font_size=16,
                            pos_hint={'center_x': .5, 'center_y': .33},
                            background_normal=
                            "doc/images/Login_shapes/Btn1.png",
                            background_down=
                            "doc/images/Login_shapes/Btn1_down.png")
        self.login_button.bind(on_release=self._login_released)
        self.register_button = Button(text="Create an account", color = GRAY,
                            font_name="Dosis",
                            size_hint=(None,None),
                            size=(125,30),
                            font_size=14,
                            pos_hint={'center_x': .5, 'center_y': .27},
                            background_normal=
                            "doc/images/Login_shapes/Btn_invis.png",
                            background_down=
                            "doc/images/Login_shapes/Btn_invis.png")
        self.register_button.bind(on_release=self._register_released)
        self.add_widget(self.login_text)
        self.add_widget(self.login_layout)
        self.add_widget(self.login_button)
        self.add_widget(self.register_button)
        #endregion
        self.footer = Label(text="EGYPT-JAPAN UNIVERSITY OF SCIENCE AND TECHNOLOGY x BENHA UNIVERSITY HACKATHON - 2024",
                             color = PURPLE,
                             font_name="Dosis",
                             pos_hint={"center_x": .5, "center_y": .04},
                             font_size=11)
        self.add_widget(self.footer)