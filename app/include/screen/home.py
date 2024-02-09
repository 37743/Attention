# Egypt-Japan University of Science and Technology
# Attention - Team E-JUSTians
# Home Screen
# ---
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.graphics import Rectangle
from kivy.core.text import LabelBase
from kivy.animation import Animation
from functools import partial
from kivy.clock import Clock
# Scripts & Variables
from script.eyetracking.utilities import (DOSIS_FONT,
                                          YAHEI_FONT,
                                          SUPPORTED_TYPES,
                                          TXT_LIMIT,
                                          GRAY,
                                          CYAN,
                                          PURPLE)
from script.datetextinput import DateTextInput
from script.togglebutton import ToggleButton
# Tkinter for Filechooser interface
import tkinter as tk
from tkinter import filedialog
# MariaDB connector
import mysql.connector
# Multiprocessing
import threading
# PDF Text Extraction
from io import BytesIO
from pdfminer.high_level import extract_text
# Time Manipulation
from datetime import (datetime,
                      timedelta)
# Eyetracker
from script.eyetracking.cv import (GazeTracker, penalty)

def change_to_screen(*args, screen):
    App.get_running_app().screen_manager.current = screen
    return

def hide_layout(*args, self, layout):
    hide = Animation(pos_hint={'center_x':5,'center_y':.5}, t='in_cubic', d=2)
    hide &= Animation(opacity=0, t='in_cubic', d=1)
    layout = "self."+str(layout)+"_layout"
    if layout == "self.profile_layout":
        hide_again = Animation(pos_hint={'center_x':4.82,'center_y': .72}, t='in_cubic', d=2)
        hide_again &= Animation(opacity=1, t='in_cubic', d=1)
        hide_again.start(self.profile_border)
    exec(f"hide.start({layout})")

def show_layout(*args, self, layout):
    show = Animation(pos_hint={'center_x':.5,'center_y':.5}, t='out_cubic', d=2)
    show &= Animation(opacity=1, t='in_cubic', d=2)
    layout = "self."+str(layout)+"_layout"
    print(layout)
    if layout == "self.profile_layout":
        show_again = Animation(pos_hint={'center_x':.32,'center_y': .72}, t='out_cubic', d=2)
        show_again &= Animation(opacity=1, t='in_cubic', d=2)
        show_again.start(self.profile_border)
    exec(f"show.start({layout})")

def make_img(encoded_data, path):
    filepath=path
    with open(filepath, 'wb') as f:
        f.write(encoded_data)
    return filepath

def thread(function):
    ''' Creates a new thread with a process using the input function'''
    def wrap(*args, **kwargs):
        t = threading.Thread(target=function, args=args, kwargs=kwargs, daemon=True)
        t.start()
        return t
    return wrap

class NewPopup(Popup):
    def __init__(self, func, doc_idx, title_text,
                 label_text, button_text, **kwargs):
        super(NewPopup, self).__init__(**kwargs)
        self.popup_layout = BoxLayout(orientation="vertical",
                                      pos_hint={'center_x': .5, 'center_y': .6},
                                      spacing=10)
        self.popup_layout.add_widget(Label(text=label_text,
                                           halign="center",
                                           markup=True,
                                           line_height=1.2,
                                           font_name="Dosis",
                                           color=CYAN,
                                           font_size=18,
                                           ))
        self.popup_but = Button(text=button_text, color = "ffffff",
                                    font_name="Dosis",
                                    size_hint=(None,None),
                                    size=(140,37),
                                    font_size=16,
                                    pos_hint={'center_x': .5, 'center_y': .5},
                                    background_normal=
                                    "doc/images/Add_page/Btn1.png",
                                    background_down=
                                    "doc/images/Add_page/Btn1_down.png")
        self.popup_but.bind(on_release=partial(func,
                                               popup_obj=self,
                                               doc=doc_idx))
        self.popup_layout.add_widget(self.popup_but)
        self.title = title_text
        self.title_font = "Dosis"
        self.title_color = PURPLE
        self.title_size=32
        self.title_align="center"
        self.separator_height = 0
        self.background = "app/doc/images/Reading_page/popup_reg.png"
        self.size = (350,200)
        self.size_hint=(None,None)
        self.add_widget(self.popup_layout)

class Home(Screen, FloatLayout):
    def _update_bg(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size
    
    def _navigate(self, instance, final):
        init = self._get_curr()
        self._set_curr(new_curr=final)
        hide_layout(self=self, layout=init)
        show_layout(self=self, layout=final)

    def _leaderboard(self):
        result = []
        try:
            db_cred = App.get_running_app().db_cred
            cn = mysql.connector.connect(
                            user=db_cred['user'],
                            password=db_cred['password'],
                            host=db_cred['host'],
                            database=db_cred['database'])
            print("Connected!")
            cr = cn.cursor()
            u = self.user
            cr.callproc("get_ldrb")
            for res in cr.stored_results():
                fetch = res.fetchall()
                for row in fetch:
                    result.append(row)
            cn.close()
        except mysql.connector.Error as e:
            print(f"{e}")
        for i in [1,0,2]: # 2nd, 1st and 3rd respectively
            top_layout = FloatLayout()
            top_panel = Image(source="app/doc/images/Home_page_shapes/ldr_BG.png",
                            size=(125/(i*.3+1),161/(i*.3+1)),
                            size_hint=(None,None),
                            pos_hint={"center_x": .5, "center_y": .5})
            top_layout.add_widget(top_panel)
            top_pfp = "doc/images/Profile_page/pfp_default.png"\
            if (result[i][2] == b'') else make_img(result[i][2],
                               f"app/doc/images/Home_page_shapes/top_{i+1}")
            top_pfp_layout = FloatLayout(size=(75/(i*.3+1),75/(i*.3+1)),
                                      size_hint=(None,None),
                                      pos_hint={'center_x': .5, 'center_y': .7-i*.05})
            top_pfp_layout.add_widget(Image(source=top_pfp,
                                            size=(75,75),
                                            pos_hint={"center_x": .5, "center_y": .5}))
            top_pfp_layout.add_widget(Image(source="doc/images/Home_page_shapes/top_border.png",
                                            size=(75,75),
                                            pos_hint={"center_x": .5, "center_y": .5}))
            top_pfp_layout.add_widget(Image(source=f"doc/images/Home_page_shapes/{i+1}.png",
                                            size_hint=(None,None),
                                            size=(35/(i*.3+1),42/(i*.3+1)),
                                            pos_hint={"center_x": .8, "center_y": .15}))
            top_pfp_layout.add_widget(Label(text=result[i][0] if len(result[i][0]) < 10\
                                                                      else result[i][0][:10] + "..",
                                        font_name="Dosis",
                                        color="ffffff",
                                        font_size=18,
                                        halign='center',
                                        pos_hint={"center_x": .5, 'center_y': -.2}))
            xp = str(result[i][1]) if len(str(result[i][1])) < 6\
                        else str(result[i][1])[:6] + ".."
            top_pfp_layout.add_widget(Label(text=f"XP: {xp}",
                                        font_name="Dosis",
                                        color=CYAN,
                                        font_size=16,
                                        halign='center',
                                        pos_hint={"center_x": .5, 'center_y': -.6}))
            top_layout.add_widget(top_pfp_layout)
            self.topu_layout.add_widget(top_layout)
        for idx, row in enumerate(result):
            row_layout = BoxLayout(orientation="horizontal")
            row_layout.add_widget(Label(text=f"#{idx+1}",
                                        font_name="YaHei",
                                        color=GRAY,
                                        font_size=14,
                                        halign='left',
                                        pos_hint={'right': 0}))
            row_layout.add_widget(Label(text=result[idx][0],
                                        font_name="YaHei",
                                        color=GRAY,
                                        font_size=14,
                                        halign='left',
                                        pos_hint={'right': 0}))
            row_layout.add_widget(Label(text=str(result[idx][1]),
                                        font_name="YaHei",
                                        color=GRAY,
                                        font_size=14,
                                        halign='left',
                                        pos_hint={'right': 0}))
            self.home_ldrb_grid.add_widget(row_layout)
        return result
    
    def _add_file(self, instance):
        root = tk.Tk()
        root.withdraw()

        self.file_path = filedialog.askopenfilename(title = "Select Study Material",
                                            filetypes=[("PDF, Text files", "*.pdf *.txt")])
        if len(self.file_path) > 0:
            for type in SUPPORTED_TYPES[0]:
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

    def _warning(self, instance, popup_obj, doc):
        popup_obj.dismiss()
        # TODO: Add more to this

    def _time_inc(self, instance):
        date = datetime.strptime(self.book_timer.text, "%H:%M:%S")
        date += timedelta(seconds=1)
        self.book_timer.text = datetime.strftime(date, "%H:%M:%S")
        print(f"Recent:{penalty.recent} - "\
                +f"Blinks:{penalty.blinks} - "\
                +f"Left:{penalty.left} - "\
                +f"Center:{penalty.center} - "\
                +f"Right:{penalty.right}")
        self.warning = self.warning + 1 if penalty.recent != "center" else 0
        if (self.warning > 5):
            Clock.unschedule(self._time_inc)
            penalty.pause = True
            # Reset
            self.warning = 0
            self.pause_popup = NewPopup(self._warning, None, "Paused",
                                        f"WARNING!\n"\
                                        +f"[color={PURPLE}]"+
                                        f"You have not read anything in a while.",
                                        "RESUME")
            self.pause_popup.bind(on_dismiss=self._read_unpause)
            self.pause_popup.open()

    def _update_txt(self, doc):
        self.doc_page.text = f"{self.documents[doc][3]}/{len(self.whole_doc)}"
        self.doc_text.text = self.whole_doc[int(self.doc_page.text.rsplit("/")[0])-1]
        # Start timer once loading has finished
        self.timer = Clock.schedule_interval(self._time_inc, 1)

    def _flip_page(self, instance, direction):
        # 1-indexed to 0-indexed for proper text mapping
        curr_page = int(self.doc_page.text.rsplit("/")[0])
        if self.doc_page.text.rsplit("/")[1] == "0":
            return
        if (curr_page == len(self.whole_doc)\
            and direction == "next")\
            or\
            ((curr_page-1 == 0) and direction == "prev"):
            return
        curr_page = curr_page if direction == "next"\
              else curr_page-2
        # New page 
        self.doc_text.text = self.whole_doc[curr_page]
        self.doc_page.text = f"{curr_page+1}/{len(self.whole_doc)}"

    @thread
    def _extract_pdf(self, input, doc):
        self.whole_doc = extract_text(BytesIO(input))
        self.whole_doc = [self.whole_doc[i:i+TXT_LIMIT]\
                               for i in range(0, len(self.whole_doc), TXT_LIMIT)]
        self._update_txt(doc)
        penalty.reset = True
    
    def _read_start(self, instance, doc):
        if (self.book_title.text == self.documents[doc][0]):
            return
        Clock.unschedule(self._time_inc)
        self.start_popup = NewPopup(self._read_doc, doc, self.documents[doc][0],
                                    f"Ready?\n"\
                                    +f"[color={PURPLE}]"+
                                    "WARNING: The timer will start ticking![/color]",
                                    "YES")
        self.start_popup.bind(on_dismiss=self._read_unpause)
        self.start_popup.open()

    def _read_doc(self, instance, popup_obj, doc):
        popup_obj.dismiss()
        # Assert that it is false.
        penalty.end = False
        if (self.refresh_but in self.book_mat_layout.children):
            self.book_mat_layout.remove_widget(self.refresh_but)
            self.book_mat_layout.add_widget(self.pause_but)
        self.gt = self._start_tracker()
        self.book_timer.text = "00:00:00"
        Clock.unschedule(self._time_inc)
        self.doc_text.text = "Loading.."
        self.book_title.text = self.documents[doc][0]
        if (self.documents[doc][2] == "pdf"):
            self._extract_pdf(input=self.documents[doc][1], doc=doc)
        # TXT files
        else:
            self.whole_doc = self.documents[doc][1].decode()
            self.whole_doc = [self.whole_doc[i:i+TXT_LIMIT]\
                               for i in range(0, len(self.whole_doc), TXT_LIMIT)]
            self._update_txt(doc)
            penalty.reset = True

    def _read_pause(self, instance):
        Clock.unschedule(self._time_inc)
        penalty.pause = True
        self.pause_popup = NewPopup(self._save_prog, None, "Paused",
                                    f"Do you want to end session?\n"\
                                    +f"[color={PURPLE}]"+
                                    f"XP Gained:{penalty.center}",
                                    "YES")
        self.pause_popup.bind(on_dismiss=self._read_unpause)
        self.pause_popup.open()

    def _read_unpause(self, instance):
        penalty.pause = False
        Clock.schedule_interval(self._time_inc, 1)

    def _save_prog(self, instance, popup_obj, doc):
        popup_obj.dismiss()
        Clock.unschedule(self._time_inc)
        penalty.end = True
        doc = self.book_title.text
        self.book_title.text = "Document Title"
        self.book_timer.text = "00:00:00"
        user = self.user
        xp = penalty.center
        pg = int(self.doc_page.text.rsplit("/")[0])
        self.doc_page.text = "0/0"
        self.doc_text.text = ""
        try:
            db_cred = App.get_running_app().db_cred
            cn = mysql.connector.connect(
                            user=db_cred['user'],
                            password=db_cred['password'],
                            host=db_cred['host'],
                            database=db_cred['database'])
            print("Connected!")
            cr = cn.cursor()
            u = self.user
            cr.callproc("save_prog", (user,doc,xp,pg))
            cn.commit()
            print("Success!")
            cn.close()
        except mysql.connector.Error as e:
            print(f"{e}")

    def _refresh_doc(self, instance):
        self.doc_layout.clear_widgets()
        result=[]
        try:
            db_cred = App.get_running_app().db_cred
            cn = mysql.connector.connect(
                            user=db_cred['user'],
                            password=db_cred['password'],
                            host=db_cred['host'],
                            database=db_cred['database'])
            print("Connected!")
            cr = cn.cursor()
            u = self.user
            cr.callproc("get_doc", (u,))
            for res in cr.stored_results():
                fetch = res.fetchall()
                for row in fetch:
                    result.append(row)
            cn.close()
        except mysql.connector.Error as e:
            print(f"{e}")
        self.documents = result
        for doc in self.documents:
            doc_name = doc[0]
            if (len(doc[0])>10):
                doc_name = doc[0][:10]+".."
            self.doc_layout.add_widget(Button(text=doc_name,
                                              font_name="Dosis",
                                              size=(125,35),
                                              color=PURPLE,
                                              font_size=16,
                                              background_normal=
                                              "doc/images/Reading_page/btn_invis.png",
                                              background_down=
                                              "doc/images/Reading_page/btn_shadow.png"))
        # Kivy inserts new widgets at index 0,
        # here we reverse the list to get the correct order.
        for idx, widget in enumerate(reversed(self.doc_layout.children)):
            widget.bind(on_release=partial(self._read_start, doc=idx))
        return

    def _update_password(self, user, cursor):
        if ((len(self.pass_box.text) < 6)\
             or (self.pass_box.text != self.conf_box.text)):
            print("Password has not changed.")
            return
        p = self.pass_box.text
        sql = "CALL update_pwd(%s,%s)"
        cursor.execute(sql, (user, p))
        print("Password has changed!")
        return
    
    def _update_details(self, instance):
        try:
            db_cred = App.get_running_app().db_cred
            cn = mysql.connector.connect(
                            user=db_cred['user'],
                            password=db_cred['password'],
                            host=db_cred['host'],
                            database=db_cred['database'])
            print("Connected!")
            cr = cn.cursor()
            u = self.user
            b = open(self.profile_pic.source, "rb").read()\
                if (self.profile_pic.source != "doc/images/Profile_page/pfp_default.png")\
                else b''
            m = str(self.mail_box.text) if (len(self.mail_box.text)>0)\
                else str(self.mail_box.hint_text)
            c = str(self.city_box.text) if (len(self.city_box.text)>0)\
                else str(self.city_box.hint_text)
            century = ''
            if self.bd_year.text != "":
                century = '20' if int(self.bd_year.text)<50 else '19'
            d = century+str(self.bd_year.text)+'-'\
                +str(self.bd_month.text)+'-'+str(self.bd_day.text)\
                if (self.bd_year.text!="" and self.bd_month.text!=""\
                     and self.bd_day.text!="")\
                else ('20' if int(self.bd_year.hint_text)<50 else '19')\
                    + str(self.bd_year.hint_text)+'-'+str(self.bd_month.hint_text)\
                        +'-'+str(self.bd_day.hint_text)
            sql = "CALL update_details(%s,%s,%s,%s,%s)"
            cr.execute(sql, (u,b,m,c,d))
            print("Data updated successfully!")
            self._update_password(u, cr)
            cn.commit()
            cn.close()
            Clock.schedule_once(self._logout_released, 1)
        except mysql.connector.Error as e:
            print(f"{e}")

    def _set_curr(self, new_curr):
        self.curr = new_curr

    def _get_curr(self):
        return self.curr
    
    def _get_details(self, e_user):
        result = {}
        try:
            db_cred = App.get_running_app().db_cred
            cn = mysql.connector.connect(
                            user=db_cred['user'],
                            password=db_cred['password'],
                            host=db_cred['host'],
                            database=db_cred['database'])
            print("Connected!")
            cr = cn.cursor()
            cr.callproc("get_details", (e_user,))
            for res in cr.stored_results():
                result = res.fetchall()[0]
            cn.close()
        except mysql.connector.Error as e:
            print(f"{e}")
        return result
        
    def _get_badge(self, xp):
        if xp <= 1000:
            return ("dash",1000)
        elif xp <= 3000:
            return ("bronze",3000)
        elif xp <= 5000:
            return ("silver",5000)
        else:
            return ("gold",9999999)

    def _add_pfp(self, instance):
        root = tk.Tk()
        root.withdraw()

        self.file_path = filedialog.askopenfilename(title = "Select Profile Picture",
                                            filetypes=[("Image files", "*.png *.jpeg *.jpg")])
        if len(self.file_path) > 0:
            for type in SUPPORTED_TYPES[1]:
                if self.file_path.rsplit(".")[1] == type:
                    self.profile_pic.source = self.file_path

    @thread
    def _start_tracker(self):
        GazeTracker()
    
    def _logout_released(self, instance):
        app = App.get_running_app()
        app.login.login_result.text = "Logged out!"
        app.login.pass_box.text = ""
        change_to_screen(screen="Login Page")
        Clock.schedule_once(lambda dt: app.screen_manager.remove_widget(app.home), 2)
        
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
        # User's Essentials
        self.user = App.get_running_app().user
        self.curr = "home"
        self.file_path = ""
        self.documents = []
        self.warning = 0
        #region Navigation Bar
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
        #endregion
        #region Home Layout
        self.home_layout = FloatLayout(pos_hint={"center_x": .5, "center_y": .5})
        self.home_panel = Image(source="app/doc/images/Home_page_shapes/leaderboard_table_BG.png",
                                size_hint=(None,None),
                                size=(600,467),
                                pos_hint={"center_x": .5, "center_y": .47})
        self.home_title = Label(text="Leaderboard",
                                  font_name="Dosis",
                                  color=PURPLE,
                                  font_size=36,
                                  halign='center',
                                  pos_hint={"center_x": .5, "center_y": .9})
        self.topu_layout = BoxLayout(orientation="horizontal",
                                    size_hint=(None,None),
                                    size=(550,161),
                                    padding=(50,0),
                                    pos_hint={"center_x": .5, "center_y": .73})
        self.rank_layout = BoxLayout(orientation="horizontal",
                                     size_hint_x=None,
                                     size=(550,35),
                                     pos_hint={"center_x": .5, "center_y": .58})
        self.rank_layout.add_widget(Label(text="Rank",
                                    font_name="YaHei",
                                    color=GRAY,
                                    font_size=18,
                                    halign='center'))
        self.rank_layout.add_widget(Label(text="Username",
                                    font_name="YaHei",
                                    color=GRAY,
                                    font_size=18,
                                    halign='center'))
        self.rank_layout.add_widget(Label(text="Total XP",
                                    font_name="YaHei",
                                    color=GRAY,
                                    font_size=18,
                                    halign='center'))
        self.home_scroll = ScrollView(size=(550,280),
                                     size_hint=(None, None),
                                     pos_hint={"center_x": .505, "center_y": .34},
                                     bar_color = PURPLE,
                                     bar_inactive_color = GRAY,
                                     bar_width = 8,
                                     scroll_type = ['bars','content'])
        self.home_ldrb_grid = GridLayout(cols=1,
                                         spacing=5,
                                         col_default_width=540,
                                         col_force_default=True,
                                         row_default_height=35,
                                         row_force_default=True,
                                         size_hint_y=None)
        self.home_ldrb_grid.bind(minimum_height=\
                                self.home_ldrb_grid.setter('height'))
        self._leaderboard()
        for widget in ["home"]:
            exec(f"self.{widget}_layout.add_widget(self.{widget}_panel)")
            exec(f"self.{widget}_layout.add_widget(self.{widget}_title)")
        self.home_scroll.add_widget(self.home_ldrb_grid)
        self.home_layout.add_widget(self.topu_layout)
        self.home_layout.add_widget(self.rank_layout)
        self.home_layout.add_widget(self.home_scroll)
        self.add_widget(self.home_layout)
        #endregion
        #region Add Material Layout
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
        #endregion
        #region Reading Layout
        self.book_layout = FloatLayout(pos_hint={"center_x": 5, "center_y": .5},
                                      opacity=0)
        self.book_panel = Image(source="app/doc/images/Home_page_shapes/book_panel.png",
                                size_hint=(None,None),
                                size=(536,503),
                                opacity=.2,
                                pos_hint={"center_x": .5, "center_y": .48})
        self.book_title = Label(text="Document Title",
                                  font_name="Dosis",
                                  color=PURPLE,
                                  font_size=36,
                                  halign='center',
                                  pos_hint={"center_x": .5, "center_y": .92})
        self.book_mat_layout = FloatLayout(pos_hint={"center_x": .85, "center_y": .5})
        self.book_panel2 = Image(source="app/doc/images/Home_page_shapes/book_panel_2.png",
                                size_hint=(None,None),
                                size=(185,503),
                                opacity=.2,
                                pos_hint={"center_x": .5, "center_y": .48})
        self.book_timer = Label(text="00:00:00",
                                  font_name="YaHei",
                                  color=GRAY,
                                  font_size=36,
                                  halign='center',
                                  pos_hint={"center_x": .5, "center_y": .92})
        self.doc_scroll = ScrollView(size=(150,390),
                                     size_hint=(None, None),
                                     pos_hint={"center_x": .5, "center_y": .53},
                                     bar_color = PURPLE,
                                     bar_inactive_color = GRAY,
                                     bar_width = 8,
                                     scroll_type = ['bars','content'])
        self.doc_layout = GridLayout(cols=1,
                                     spacing=5,
                                     col_default_width=125,
                                     col_force_default=True,
                                     row_default_height=35,
                                     row_force_default=True,
                                     size_hint_y=None)
        self.doc_layout.bind(minimum_height=self.doc_layout.setter('height'))
        self.doc_scroll.add_widget(self.doc_layout)
        self.doc_text = Label(text="",
                              text_size=(450,400),
                              font_name="YaHei",
                              color=PURPLE,
                              font_size=16,
                              halign='left',
                              valign='top',
                              pos_hint={"center_x": .505, "center_y": .53})
        self.doc_page = Label(text="0/0",
                              font_name="YaHei",
                              color=PURPLE,
                              font_size=16,
                              halign='center',
                              pos_hint={"center_x": .5, "center_y": .15})     
        self.refresh_but = Button(text="",
                                size_hint=(None,None),
                                size=(52,56),
                                pos_hint={'center_x': .5, 'center_y': .15},
                                background_normal=
                                "doc/images/Reading_page/refresh.png",
                                background_down=
                                "doc/images/Reading_page/refresh_down.png")
        self.refresh_but.bind(on_release=self._refresh_doc)
        self.pause_but = Button(text="PAUSE/END", color = "ffffff",
                                    font_name="Dosis",
                                    size_hint=(None,None),
                                    size=(140,37),
                                    font_size=16,
                                    pos_hint={'center_x': .5, 'center_y': .15},
                                    background_normal=
                                    "doc/images/Add_page/Btn1.png",
                                    background_down=
                                    "doc/images/Add_page/Btn1_down.png")
        self.pause_but.bind(on_release=self._read_pause)
        self.prev_pg_but = Button(text="",
                                size_hint=(None,None),
                                size=(52,56),
                                pos_hint={'center_x': .35, 'center_y': .15},
                                background_normal=
                                "doc/images/Reading_page/left_arrow.png",
                                background_down=
                                "doc/images/Reading_page/left_arrow_down.png")
        self.prev_pg_but.bind(on_release=partial(self._flip_page, direction="prev"))
        self.next_pg_but = Button(text="",
                                size_hint=(None,None),
                                size=(52,56),
                                pos_hint={'center_x': .65, 'center_y': .15},
                                background_normal=
                                "doc/images/Reading_page/right_arrow.png",
                                background_down=
                                "doc/images/Reading_page/right_arrow_down.png")
        self.next_pg_but.bind(on_release=partial(self._flip_page, direction="next"))
        self.book_layout.add_widget(self.book_panel)
        self.book_layout.add_widget(self.doc_text)
        self.book_layout.add_widget(self.book_title)
        self.book_layout.add_widget(self.doc_page)
        self.book_layout.add_widget(self.prev_pg_but)
        self.book_layout.add_widget(self.next_pg_but)
        self.book_mat_layout.add_widget(self.book_panel2)
        self.book_mat_layout.add_widget(self.doc_scroll)
        self.book_mat_layout.add_widget(self.book_timer)
        self.book_mat_layout.add_widget(self.refresh_but)
        self.book_layout.add_widget(self.book_mat_layout)
        self.add_widget(self.book_layout)
        #endregion
        #region Profile Layout
        self.user_details = self._get_details(self.user)
        self.profile_layout = FloatLayout(pos_hint={"center_x": 5, "center_y": .5},
                                      opacity=0)
        self.profile_panel = Image(source="app/doc/images/Register_shapes/Register_reg.png",
                                    size_hint=(None,None),
                                    size=(600,700),
                                    pos_hint={"center_x": .5, "center_y": .5})
        self.pfp_layout = FloatLayout(size=(75,75),
                                      size_hint=(None,None),
                                      pos_hint={'center_x': .32, 'center_y': .72})
        self.profile_border = Button(text="",
                                    size=(75,75),
                                    size_hint=(None,None),
                                    pos_hint={'center_x': 4.82, 'center_y': .72},
                                    background_normal=
                                    "doc/images/Profile_page/pfp_border.png",
                                    background_down=
                                    "doc/images/Profile_page/pfp_border_down.png")
        self.profile_border.bind(on_release=self._add_pfp)
        self.pfp = "doc/images/Profile_page/pfp_default.png"\
            if (self.user_details[4] == b'') else make_img(self.user_details[4],
                                                           "app/doc/images/Profile_page/profile_pic.jpg")
        self.profile_pic = Image(source=self.pfp,
                                    pos_hint={"center_x": .5, "center_y": .5})
        self.pfp_layout.add_widget(self.profile_pic)
        self.pfp_text_layout = FloatLayout(size=(275,75),
                                      size_hint=(None,None),
                                      pos_hint={'center_x': .65, 'center_y': .75})
        self.pfp_text = BoxLayout(orientation="vertical",
                                spacing=-30,
                                pos_hint={'center_x': 1, 'center_y': .5})
        self.profile_user = Label(text=self.user,
                                  font_name="Dosis",
                                  color=CYAN,
                                  font_size=22,
                                  halign='left',
                                  pos_hint={'right': 0})
        self.profile_user.bind(size=self.profile_user.setter('text_size'))
        self.badge_result, self.milestone = self._get_badge(self.user_details[3])
        self.profile_xp = Label(text="Total XP: {xp}/{m}".format(xp=self.user_details[3],
                                                                 m=self.milestone),
                                font_name="YaHei",
                                color=GRAY,
                                font_size=14,
                                halign='left',
                                pos_hint={'right': 0})
        self.profile_xp.bind(size=self.profile_xp.setter('text_size'))
        self.profile_badge = Image(source=f"doc/images/Profile_page/{self.badge_result}.png",
                                   pos_hint={"center_x": .68, "center_y": .7})
        self.pfp_text.add_widget(self.profile_user)
        self.pfp_text.add_widget(self.profile_xp)
        self.pfp_text_layout.add_widget(self.pfp_text)

        # Update Profile Details
        self.details_layout = GridLayout(rows=3,
                                orientation='tb-lr',
                                size_hint=(None,None),
                                size=(550,345),
                                spacing=-30,
                                row_default_height=115,
                                row_force_default=True,
                                pos_hint={'center_x': .5, 'center_y': .42},)
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
                                cursor_color=PURPLE,
                                font_size=13,
                                foreground_color=PURPLE,
                                write_tab=False,
                                padding=(10,10),
                                hint_text = "",
                                background_normal="doc/images/Register_shapes/TextBox.png",
                                background_active="doc/images/Register_shapes/TextBox_active.png",
                                pos_hint={'center_x': .5, 'center_y': .5})
        self.pass_layout.add_widget(self.pass_box)
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
                                cursor_color=PURPLE,
                                font_size=13,
                                foreground_color=PURPLE,
                                write_tab=False,
                                padding=(10,10),
                                hint_text = "",
                                background_normal="doc/images/Register_shapes/TextBox.png",
                                background_active="doc/images/Register_shapes/TextBox_active.png",
                                pos_hint={'center_x': .5, 'center_y': .5})
        self.conf_layout.add_widget(self.conf_box)
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
                                cursor_color=PURPLE,
                                font_size=13,
                                foreground_color=PURPLE,
                                write_tab=False,
                                padding=(10,10),
                                hint_text = self.user_details[0],
                                background_normal="doc/images/Register_shapes/TextBox.png",
                                background_active="doc/images/Register_shapes/TextBox_active.png",
                                pos_hint={'center_x': .5, 'center_y': .5})
        self.mail_layout.add_widget(self.mail_box)
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
                                cursor_color=PURPLE,
                                font_size=13,
                                foreground_color=PURPLE,
                                write_tab=False,
                                padding=(10,10),
                                hint_text = self.user_details[1],
                                background_normal="doc/images/Register_shapes/TextBox.png",
                                background_active="doc/images/Register_shapes/TextBox_active.png",
                                pos_hint={'center_x': .5, 'center_y': .5})
        self.city_layout.add_widget(self.city_box)
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
                                cursor_color=PURPLE,
                                font_size=13,
                                foreground_color=PURPLE,
                                write_tab=False,
                                padding=(10,10),
                                hint_text = self.user_details[2].strftime("%d"),
                                background_normal="doc/images/Register_shapes/SquareBtn.png",
                                background_active="doc/images/Register_shapes/SquareBtn_active.png")
        self.bd_month = DateTextInput(multiline=False,
                                font_name="YaHei",
                                input_filter='int',
                                cursor_color=PURPLE,
                                font_size=13,
                                foreground_color=PURPLE,
                                write_tab=False,
                                padding=(10,10),
                                hint_text = self.user_details[2].strftime("%m"),
                                background_normal="doc/images/Register_shapes/SquareBtn.png",
                                background_active="doc/images/Register_shapes/SquareBtn_active.png")
        self.bd_year = DateTextInput(multiline=False,
                                font_name="YaHei",
                                input_filter='int',
                                cursor_color=PURPLE,
                                font_size=13,
                                foreground_color=PURPLE,
                                write_tab=False,
                                padding=(10,10),
                                hint_text = self.user_details[2].strftime("%y"),
                                background_normal="doc/images/Register_shapes/SquareBtn.png",
                                background_active="doc/images/Register_shapes/SquareBtn_active.png")
        # Update Button
        self.update_but_layout = FloatLayout(size=(200,70))
        self.update_but = Button(text="UPDATE", color = "ffffff",
                                font_name="Dosis",
                                size_hint=(None,None),
                                size=(140,37),
                                pos_hint={'center_x': .5, 'center_y': .3},
                                font_size=16,
                                background_normal=
                                "doc/images/Register_shapes/Btn1.png",
                                background_down=
                                "doc/images/Register_shapes/Btn1_down.png")
        self.update_but.bind(on_release=self._update_details)
        self.update_but_layout.add_widget(self.update_but)
        self.bd_layout2.add_widget(self.bd_day)
        self.bd_layout2.add_widget(self.bd_month)
        self.bd_layout2.add_widget(self.bd_year)
        self.bd_layout.add_widget(self.bd_layout2)
        self.details_layout.add_widget(self.pass_layout)
        self.details_layout.add_widget(self.conf_layout)
        self.details_layout.add_widget(self.bd_layout)
        self.details_layout.add_widget(self.mail_layout)
        self.details_layout.add_widget(self.city_layout)
        self.details_layout.add_widget(self.update_but_layout)
        self.profile_layout.add_widget(self.profile_panel)
        self.profile_layout.add_widget(self.pfp_layout)
        self.profile_layout.add_widget(self.pfp_text_layout)
        self.profile_layout.add_widget(self.profile_badge)
        self.profile_layout.add_widget(self.details_layout)
        self.add_widget(self.profile_layout)
        self.add_widget(self.profile_border)
        #endregion
        for widget in ["home","add","book","profile"]:
            exec(f"self.{widget}_nav.add_widget(self.{widget}_but)")
            exec(f"self.{widget}_nav.add_widget(self.{widget}_icon)")
            exec(f"self.nav_bar.add_widget(self.{widget}_nav)")
        self.add_widget(self.nav_bar)
        #region Logout button
        self.logout_but = Button(text="",
                                size_hint=(None,None),
                                size=(52,56),
                                pos_hint={'center_x': .05, 'center_y': .1},
                                background_normal=
                                "doc/images/Home_page_shapes/logout_invis.png",
                                background_down=
                                "doc/images/Home_page_shapes/logout_shadow.png")
        self.logout_but.bind(on_release=self._logout_released)
        self.add_widget(self.logout_but)
        #endregion
        self.footer = Label(text="EGYPT-JAPAN UNIVERSITY OF SCIENCE AND TECHNOLOGY x BENHA UNIVERSITY HACKATHON - 2024",
                             color = PURPLE,
                             font_name="Dosis",
                             pos_hint={"center_x": .5, "center_y": .04},
                             font_size=11)
        self.add_widget(self.footer)