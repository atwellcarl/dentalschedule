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
from windowclasses import Help as help


import hashlib, binascii, os
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
            if(db.has_notification("Patient", user_info[0]) == 1):
                self.pop_up("Schedule Change", "Your Schedule has changed since you last \nloged in. Please review your new schedule\ndisplayed on the homepage.")
            wm.screen_manager.current = "pat_home"
        else:
            self.invalid_pat_login()

    # Pop up window for giving the user feedback
    # handles errors or successful operations
    def pop_up(self,header, message):
        popup = Popup(title = header,
                      content = Label(text = message),
                      size_hint = (None, None), size = (400, 400))
        popup.open()

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

    def find_help(self):
        help.prev_window = "pat_login"

        help.text = ("""
                      The previous page is meant for a patient to login
                      or register an account. If you have never scheduled
                      an appointment online, please register a new account.
                      For returning users, enter your personal email and
                      password. If you have forgotten either your email or
                      password please contact our office to reset them.

                                    For further assitance feel free
                                      to call our office directly
                                             608-444-1212
                      """)

        wm.screen_manager.current = "help"
