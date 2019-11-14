from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from windowclasses import WindowManager as wm
import db_control as db

user_info = [None] * 4

# A window used for patient logins or registration
class PatientLoginWindow(Screen):
    kv = Builder.load_file("stylefolders/plw.kv")
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def login(self):
        em = self.email.text
        passw = self.password.text
        if(db.is_user(em, passw, "Patient")):
            user_info[0] = db.get_pat_id(em)
            user_info[1] = "Patient"
            user_info[2] = em
            wm.screen_manager.current = "pat_home"
        else:
            self.invalid_pat_login()

    def invalid_pat_login(self):
        popup = Popup(title = "Login Failed",
                      content = Label(text = "Invalid email name or passowrd.\n New Patient? Register an account."),
                      size_hint = (None, None), size = (400, 400))
        popup.open()

    def register(self):
        wm.screen_manager.current = "reg_acc_win"
    def reset_inputs(self):
        self.email.text = ""
        self.password.text = ""
