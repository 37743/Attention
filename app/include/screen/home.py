# Egypt-Japan University of Science and Technology
# Attention - Team E-JUSTians
# Login Screen
# ---
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.behaviors import ToggleButtonBehavior
from script.EyeTracking.utilities import (DOSIS_FONT,
                                          YAHEI_FONT,
                                          SUPPORTED_TYPES,
                                          GRAY,
                                          CYAN,
                                          PURPLE)
from kivy.core.text import LabelBase
from kivy.animation import Animation
from functools import partial
from kivy.clock import Clock
# Tkinter for Filechooser interface
import tkinter as tk
from tkinter import filedialog
# MariaDB connector
import mysql.connector

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
    def __init__(self,
                 instance=None,
                 down='doc/images/Home_page_shapes/SquareBtn_shadow.png',
                 up='doc/images/Home_page_shapes/SquareBtn_invis.png',
                 **kwargs):
        self.down_state=down
        self.up_state=up
        super(ToggleButton, self).__init__(**kwargs)
        if instance == "home":
            self.state = 'down'
            self.source = self.down_state
        else:
            self.source = self.up_state

    def on_state(self, instance, value):
        if value == 'down':
            self.disabled = True
            self.source = self.down_state
        else:
            self.disabled = False
            self.source = self.up_state

class Home(Screen, FloatLayout):
    def _update_bg(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size
    
    def _navigate(self, instance, final):
        init = self._get_curr()
        self._set_curr(new_curr=final)
        hide_layout(self=self, layout=init)
        show_layout(self=self, layout=final)

    def _add_file(self, instance):
        root = tk.Tk()
        root.withdraw()

        self.file_path = filedialog.askopenfilename(title = "Select Study Material",
                                            filetypes=[("PDF files", "*.pdf"),("Text files", "*.txt")])
        if len(self.file_path) > 0:
            for type in SUPPORTED_TYPES:
                if self.file_path.rsplit(".")[1] == type:
                    for widget in ToggleButtonBehavior.get_widgets(groupname="mat"):
                        widget.state = "normal"
                        widget.source = widget.up_state
                    exec(f"self.mat_{type}.state = \"down\"")
                    exec(f"self.mat_{type}.source = self.mat_{type}.down_state")
                    exec(f"self.add_panel_icon.source = \"app/doc/images/Add_page/{type}_gray.png\"")
                    self.add_text.pos_hint = {'center_x':.5,
                                              'center_y':.3}
                    self.add_text.text = self.file_path.rsplit("/")[-1]
    
    def _upload_file(self, instance):
        showtext = Animation(opacity=1, d=.5)
        hidetext = Animation(opacity=0, d=.5)
        self.mat_result = Label(text="Kindly upload a file!",
                                font_name="Dosis",
                                color=CYAN,
                                font_size=22,
                                halign='center',
                                opacity=0,
                                pos_hint={"center_x": .5, "center_y": 1.3})
        self.add_layout.add_widget(self.mat_result)
        if (self.file_path):
            try:
                db_cred = App.get_running_app().db_cred
                cn = mysql.connector.connect(
                                user=db_cred['user'],
                                password=db_cred['password'],
                                host=db_cred['host'],
                                database=db_cred['database'])
                print("Connected!")
                cr = cn.cursor()
                b = open(self.file_path, "rb").read()
                n,d = self.file_path.rsplit("/")[-1].rsplit(".")
                u = App.get_running_app().user
                sql = "CALL add_doc(%s,%s,%s,%s)"
                cr.execute(sql, (b,n,d,u))
                cn.commit()
                cn.close()
                for widget in ToggleButtonBehavior.get_widgets(groupname="mat"):
                    widget.state = "normal"
                    widget.source = widget.up_state
                self.mat_result.text = "File uploaded successfully!"
            except mysql.connector.Error as e:
                self.mat_result.text = "ERROR: Re-name or change the file!"
                print(f"{e}")
        self.file_path = ""
        self.add_panel_icon.source="app/doc/images/Add_page/add_file.png"
        self.add_text.text = "ADD NEW MATERIAL"
        self.add_text.pos_hint ={"center_x": .5, "center_y": .43}
        Clock.schedule_once(lambda dt: showtext.start(self.mat_result), .5)
        Clock.schedule_once(lambda dt: hidetext.start(self.mat_result), 5)
        Clock.schedule_once(lambda dt: self.add_layout.remove_widget(self.mat_result), 6)

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
        self.file_path = ""
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
        # book Navigation
        self.book_nav = FloatLayout()
        self.book_but = ToggleButton(group="nav",
                                     size_hint=(None,None),
                                     size=(52,56),
                                     pos_hint={'center_x': .5, 'center_y': .5})
        self.book_but.bind(on_release=partial(self._navigate,
                                              final="book"))
        self.book_icon = Image(source="doc/icons/book.png",
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
                                    size_hint_y=.5,
                                    opacity=0)
        self.add_panel_layout = FloatLayout(pos_hint={"center_x": .5, "center_y": .75})
        self.add_panel = Button(text="",
                                size_hint=(None,None),
                                size=(383,307),
                                pos_hint={'center_x': .5, 'center_y': .5},
                                opacity=.2,
                                background_normal=
                                "doc/images/Add_page/add_file_reg.png",
                                background_down=
                                "doc/images/Add_page/add_file_reg.png")
        self.add_panel.bind(on_release=self._add_file)
        self.add_panel_layout.add_widget(self.add_panel)
        self.add_panel_icon = Image(source="app/doc/images/Add_page/add_file.png",
                                    size_hint=(None,None),
                                    pos_hint={"center_x": .5, "center_y": .55})
        self.add_panel_layout.add_widget(self.add_panel_icon)
        self.add_text = Label(text="ADD NEW MATERIAL",
                                  font_name="YaHei",
                                  color=GRAY,
                                  font_size=16,
                                  halign='center',
                                  pos_hint={"center_x": .5, "center_y": .43})
        self.add_panel_layout.add_widget(self.add_text)
        self.mat_text = Label(text="Choose the type of material",
                                  font_name="YaHei",
                                  color=GRAY,
                                  font_size=14,
                                  halign='left',
                                  pos_hint={"center_x": .42, "center_y": .25})
        self.mat_layout = BoxLayout(orientation="horizontal",
                                    size_hint=(.3,1),
                                    spacing=20,
                                    pos_hint={"center_x": .47, "center_y": .1})
        self.mat_pdf = ToggleButton(group="mat",
                                    size_hint=(None,None),
                                    size=(52,52),
                                    up="doc/images/Add_page/pdf.png",
                                    down="doc/images/Add_page/pdf_down.png",
                                    pos_hint={'center_x': .5, 'center_y': .5})
        self.mat_txt = ToggleButton(group="mat",
                                    size_hint=(None,None),
                                    size=(52,52),
                                    up="doc/images/Add_page/txt.png",
                                    down="doc/images/Add_page/txt_down.png",
                                    pos_hint={'center_x': .5, 'center_y': .5})
        self.mat_vid = ToggleButton(group="mat",
                                    size_hint=(None,None),
                                    size=(52,52),
                                    up="doc/images/Add_page/video.png",
                                    down="doc/images/Add_page/video_down.png",
                                    disabled=True,
                                    # opacity=.5,
                                    pos_hint={'center_x': .5, 'center_y': .5})
        self.mat_wav = ToggleButton(group="mat",
                                    size_hint=(None,None),
                                    size=(52,52),
                                    up="doc/images/Add_page/audio.png",
                                    down="doc/images/Add_page/audio_down.png",
                                    disabled=True,
                                    # opacity=.5,
                                    pos_hint={'center_x': .5, 'center_y': .5})
        self.upload_button = Button(text="UPLOAD", color = "ffffff",
                                    font_name="Dosis",
                                    size_hint=(None,None),
                                    size=(140,37),
                                    font_size=16,
                                    pos_hint={'center_x': .5, 'center_y': -.1},
                                    background_normal=
                                    "doc/images/Add_page/Btn1.png",
                                    background_down=
                                    "doc/images/Add_page/Btn1_down.png")
        self.upload_button.bind(on_release=self._upload_file)
        self.add_layout.add_widget(self.add_panel_layout)
        self.add_layout.add_widget(self.mat_text)
        self.mat_layout.add_widget(self.mat_pdf)
        self.mat_layout.add_widget(self.mat_txt)
        self.mat_layout.add_widget(self.mat_vid)
        self.mat_layout.add_widget(self.mat_wav)
        self.add_layout.add_widget(self.mat_layout)
        self.add_layout.add_widget(self.upload_button)
        self.add_widget(self.add_layout)
        # Reading Layout
        self.book_layout = FloatLayout(pos_hint={"center_x": 5, "center_y": .5},
                                      opacity=0)
        self.book_panel = Image(source="app/doc/images/Home_page_shapes/panel_reg.png",
                                size_hint=(None,None),
                                size=(500,500),
                                pos_hint={"center_x": .5, "center_y": .5})
        self.book_title = Label(text="Book Panel Test",
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
        for widget in ["home","add","book","profile"]:
            exec(f"self.{widget}_nav.add_widget(self.{widget}_but)")
            exec(f"self.{widget}_nav.add_widget(self.{widget}_icon)")
            exec(f"self.nav_bar.add_widget(self.{widget}_nav)")
        for widget in ["home","book","profile"]:
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