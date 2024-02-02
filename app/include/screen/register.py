# Egypt-Japan University of Science and Technology
# Attention - Team E-JUSTians
# Login Screen
# ---
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from script.EyeTracking.utilities import (WINDOW_SIZE,
                                          DOSIS_FONT,
                                          YAHEI_FONT,
                                          GRAY,
                                          CYAN,
                                          PURPLE)
from kivy.animation import Animation
from kivy.core.text import LabelBase
# MariaDB connector
import mysql.connector
import driver
from kivy.clock import Clock

def change_to_screen(*args, screen):
    App.get_running_app().screen_manager.current = screen
    return

class DateTextInput(TextInput):
    ''' Inherits from TextInput,
    limits number of characters to 2'''
    max_characters = 2
    def insert_text(self, substring, from_undo=False):
        if len(self.text) >= self.max_characters and self.max_characters >= 0:
            substring = ""
        TextInput.insert_text(self, substring, from_undo)
        if self.text != ""\
              and self.hint_text == "MM"\
                  and int(self.text) > 12:
            self.text = ""
        if self.text != ""\
              and self.hint_text == "DD"\
                  and int(self.text)> 31:
            self.text = "" 

class Register(Screen, FloatLayout):
    def _update_bg(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size

    def _register_error(self):
        list = [self.register_panel,self.register_layout,
                self.register_button,self.loginp_button,
                self.register_result]
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

    def _login_released(self, instance):
        list = [self.register_panel,self.register_layout,
                self.register_button,self.loginp_button,
                self.loginp_button,self.register_text,
                self.register_result]
        for widget in list:
            shake = Animation(opacity=0, t="in_cubic", d=1)
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
            Clock.schedule_once(lambda dt: change_to_screen(screen="Login Page"), 2)
            Clock.schedule_once(self._return_obj, 3)

    def _return_obj(self, instance):
        list = [self.register_panel,self.register_layout,
                self.register_button,self.loginp_button,
                self.loginp_button,self.register_text,
                self.register_result]
        for widget in list:
            shake = Animation(opacity=1, t="in_cubic", d=1)
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

    def _register_released(self, instance):
        textboxes = [self.user_box, self.pass_box,
                     self.conf_box, self.mail_box,
                     self.city_box, self.bd_day,
                     self.bd_month, self.bd_year]
        for box in textboxes:
            if len(box.text) == 0:
                self.register_result.text="Kindly fill all credentials."
                self._register_error()
                return
        if (self.pass_box.text != self.conf_box.text):
            self.register_result.text="Passwords do not match!"
            self._register_error()
            return
        try:
            db_cred = App.get_running_app().db_cred
            cn = mysql.connector.connect(
                            user=db_cred['user'],
                            password=db_cred['password'],
                            host=db_cred['host'],
                            database=db_cred['database'])
            print("Connected!")
            cr = cn.cursor()
            u = str(self.user_box.text)
            p = str(self.pass_box.text)
            e = str(self.mail_box.text)
            c = str(self.city_box.text)
            century = '20' if int(self.bd_year.text)<50 else '19'
            d = century+str(self.bd_year.text)+'-'\
                +str(self.bd_month.text)+'-'+str(self.bd_day.text)
            cr.execute(f"CALL add_user(\'{u}\',\'{p}\',\'{e}\',\'{c}\',\'{d}\')")
            cn.commit()
            cn.close()
            self.register_result.text="Successful registration!"
        except mysql.connector.Error as e:
            self.register_result.text="Invalid Credentials! Try again."
            self._register_error()
            print(f"{e}")

    def __init__(self, **kwargs):
        super(Register, self).__init__(**kwargs)
        with self.canvas.before:
            self.bg = Rectangle(source="doc/images/Register_shapes/Background.png",
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
                                pos_hint={"center_x": .31, "center_y": .19}
                                )
        self.circles_decor.add_widget(self.c1)
        self.c2 = Image(source="doc/icons/C2.png",
                                size_hint=(None,None),
                                size=(250,250),
                                pos_hint={"center_x": .75, "center_y": .61}
                                )
        self.circles_decor.add_widget(self.c2)
        self.add_widget(self.circles_decor)
        # Register Header Text
        self.register_text = BoxLayout(orientation="vertical",
                                      size_hint=(None,None),
                                      size=(500,80),
                                      spacing=-10,
                                      pos_hint={'center_x': .5, 'center_y': .81},)
        self.register_title = Label(text="Get started for free",
                                  font_name="Dosis",
                                  color=PURPLE,
                                  font_size=36,
                                  halign='center')
        self.register_text.add_widget(self.register_title)
        self.register_subtitle = Label(text="Free forever, no worries",
                                  font_name="YaHei",
                                  color=GRAY,
                                  font_size=16,
                                  halign='center')
        self.register_text.add_widget(self.register_subtitle)
        self.register_panel = Image(source="doc/images/Register_shapes/Register_reg.png",
                                size_hint=(None,None),
                                size=(540,395),
                                pos_hint={"center_x": .5, "center_y": .445},
                                opacity=.7)
        self.add_widget(self.register_panel)
        self.register_result = Label(text="",
                                  font_name="Dosis",
                                  color=CYAN,
                                  font_size=14,
                                  halign='center',
                                  pos_hint={'center_x':.5,'center_y':.735})
        self.add_widget(self.register_result)
        # Register Details
        self.register_layout = GridLayout(rows=3,
                                orientation='tb-lr',
                                size_hint=(None,None),
                                size=(550,345),
                                spacing=-30,
                                row_default_height=115,
                                row_force_default=True,
                                pos_hint={'center_x': .5, 'center_y': .52},)
        # Username
        self.user_layout = BoxLayout(orientation="vertical",
                                    size=(200,70),
                                    spacing=-40)
        self.user_label = Label(text="Username",
                                font_name="YaHei",
                                color=GRAY,
                                font_size=13,
                                halign='left',
                                pos_hint={'center_x': .25, 'center_y': .5})
        self.user_layout.add_widget(self.user_label)
        self.user_box = TextInput(multiline=False,
                                size_hint = (.75,.4),
                                font_name="YaHei",
                                cursor_color=GRAY,
                                font_size=13,
                                foreground_color=GRAY,
                                write_tab=False,
                                padding=(10,10),
                                hint_text = "",
                                background_normal="doc/images/Register_shapes/TextBox.png",
                                background_active="doc/images/Register_shapes/TextBox_active.png",
                                pos_hint={'center_x': .5, 'center_y': .5})
        self.user_layout.add_widget(self.user_box)
        self.register_layout.add_widget(self.user_layout)
        # Password
        self.pass_layout = BoxLayout(orientation="vertical",
                                    size=(200,70),
                                    spacing=-40)
        self.pass_label = Label(text="Password",
                                font_name="YaHei",
                                color=GRAY,
                                font_size=13,
                                halign='left',
                                pos_hint={'center_x': .25, 'center_y': .5})
        self.pass_layout.add_widget(self.pass_label)
        self.pass_box = TextInput(multiline=False,
                                size_hint = (.75,.4),
                                font_name="YaHei",
                                password=True,
                                cursor_color=GRAY,
                                font_size=13,
                                foreground_color=GRAY,
                                write_tab=False,
                                padding=(10,10),
                                hint_text = "",
                                background_normal="doc/images/Register_shapes/TextBox.png",
                                background_active="doc/images/Register_shapes/TextBox_active.png",
                                pos_hint={'center_x': .5, 'center_y': .5})
        self.pass_layout.add_widget(self.pass_box)
        self.register_layout.add_widget(self.pass_layout)
        # Confirmation Password
        self.conf_layout = BoxLayout(orientation="vertical",
                                    size=(200,70),
                                    spacing=-40)
        self.conf_label = Label(text="Confirmed Password",
                                font_name="YaHei",
                                color=GRAY,
                                font_size=13,
                                halign='left',
                                pos_hint={'center_x': .37, 'center_y': .5})
        self.conf_layout.add_widget(self.conf_label)
        self.conf_box = TextInput(multiline=False,
                                size_hint = (.75,.4),
                                font_name="YaHei",
                                password=True,
                                cursor_color=GRAY,
                                font_size=13,
                                foreground_color=GRAY,
                                write_tab=False,
                                padding=(10,10),
                                hint_text = "",
                                background_normal="doc/images/Register_shapes/TextBox.png",
                                background_active="doc/images/Register_shapes/TextBox_active.png",
                                pos_hint={'center_x': .5, 'center_y': .5})
        self.conf_layout.add_widget(self.conf_box)
        self.register_layout.add_widget(self.conf_layout)
        # Email
        self.mail_layout = BoxLayout(orientation="vertical",
                                    size=(200,70),
                                    spacing=-40)
        self.mail_label = Label(text="Email",
                                font_name="YaHei",
                                color=GRAY,
                                font_size=13,
                                halign='left',
                                pos_hint={'center_x': .2, 'center_y': .5})
        self.mail_layout.add_widget(self.mail_label)
        self.mail_box = TextInput(multiline=False,
                                size_hint = (.75,.4),
                                font_name="YaHei",
                                cursor_color=GRAY,
                                font_size=13,
                                foreground_color=GRAY,
                                write_tab=False,
                                padding=(10,10),
                                hint_text = "",
                                background_normal="doc/images/Register_shapes/TextBox.png",
                                background_active="doc/images/Register_shapes/TextBox_active.png",
                                pos_hint={'center_x': .5, 'center_y': .5})
        self.mail_layout.add_widget(self.mail_box)
        self.register_layout.add_widget(self.mail_layout)
        # City
        self.city_layout = BoxLayout(orientation="vertical",
                                    size=(200,70),
                                    spacing=-40)
        self.city_label = Label(text="City",
                                font_name="YaHei",
                                color=GRAY,
                                font_size=13,
                                halign='left',
                                pos_hint={'center_x': .19, 'center_y': .5})
        self.city_layout.add_widget(self.city_label)
        self.city_box = TextInput(multiline=False,
                                size_hint = (.75,.4),
                                font_name="YaHei",
                                cursor_color=GRAY,
                                font_size=13,
                                foreground_color=GRAY,
                                write_tab=False,
                                padding=(10,10),
                                hint_text = "",
                                background_normal="doc/images/Register_shapes/TextBox.png",
                                background_active="doc/images/Register_shapes/TextBox_active.png",
                                pos_hint={'center_x': .5, 'center_y': .5})
        self.city_layout.add_widget(self.city_box)
        self.register_layout.add_widget(self.city_layout)
        # Birth date
        self.bd_layout = BoxLayout(orientation="vertical",
                                    size=(200,70),
                                    spacing=-40)
        self.bd_label = Label(text="Birth Date",
                                font_name="YaHei",
                                color=GRAY,
                                font_size=13,
                                halign='left',
                                pos_hint={'center_x': .24, 'center_y': .5})
        self.bd_layout.add_widget(self.bd_label)
        self.bd_layout2 = BoxLayout(orientation="horizontal",
                                    size_hint = (.75,.4),
                                    pos_hint={'center_x': .5, 'center_y': .5},
                                    spacing=10)
        self.bd_day = DateTextInput(multiline=False,
                                font_name="YaHei",
                                input_filter='int',
                                cursor_color=GRAY,
                                font_size=13,
                                foreground_color=GRAY,
                                write_tab=False,
                                padding=(10,10),
                                hint_text = "DD",
                                background_normal="doc/images/Register_shapes/SquareBtn.png",
                                background_active="doc/images/Register_shapes/SquareBtn_active.png")
        self.bd_month = DateTextInput(multiline=False,
                                font_name="YaHei",
                                input_filter='int',
                                cursor_color=GRAY,
                                font_size=13,
                                foreground_color=GRAY,
                                write_tab=False,
                                padding=(10,10),
                                hint_text = "MM",
                                background_normal="doc/images/Register_shapes/SquareBtn.png",
                                background_active="doc/images/Register_shapes/SquareBtn_active.png")
        self.bd_year = DateTextInput(multiline=False,
                                font_name="YaHei",
                                input_filter='int',
                                cursor_color=GRAY,
                                font_size=13,
                                foreground_color=GRAY,
                                write_tab=False,
                                padding=(10,10),
                                hint_text = "YY",
                                background_normal="doc/images/Register_shapes/SquareBtn.png",
                                background_active="doc/images/Register_shapes/SquareBtn_active.png")
        self.bd_layout2.add_widget(self.bd_day)
        self.bd_layout2.add_widget(self.bd_month)
        self.bd_layout2.add_widget(self.bd_year)
        self.bd_layout.add_widget(self.bd_layout2)
        self.register_layout.add_widget(self.bd_layout)
        # Register & Login Page Redirect Button(s)
        self.register_button = Button(text="REGISTER", color = "ffffff",
                            font_name="Dosis",
                            size_hint=(None,None),
                            size=(140,37),
                            font_size=16,
                            pos_hint={'center_x': .5, 'center_y': .29},
                            background_normal=
                            "doc/images/Register_shapes/Btn1.png",
                            background_down=
                            "doc/images/Register_shapes/Btn1_down.png")
        self.register_button.bind(on_release=self._register_released)
        self.loginp_button = Button(text="Already have an account?", color = GRAY,
                            font_name="Dosis",
                            size_hint=(None,None),
                            size=(160,30),
                            font_size=14,
                            pos_hint={'center_x': .5, 'center_y': .23},
                            background_normal=
                            "doc/images/Register_shapes/Btn_invis.png",
                            background_down=
                            "doc/images/Register_shapes/Btn_invis.png")
        self.loginp_button.bind(on_release=self._login_released)
        self.add_widget(self.register_text)
        self.add_widget(self.register_layout)
        self.add_widget(self.register_button)
        self.add_widget(self.loginp_button)
        self.footer = Label(text="EGYPT-JAPAN UNIVERSITY OF SCIENCE AND TECHNOLOGY x BENHA UNIVERSITY HACKATHON - 2024",
                             color = PURPLE,
                             font_name="Dosis",
                             pos_hint={"center_x": .5, "center_y": .04},
                             font_size=11)
        self.add_widget(self.footer)