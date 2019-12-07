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

# This class allows a patient user to register an account
class RegisterAccountWindow(Screen):
    kv = Builder.load_file("stylefolders/raw.kv")
    fr_name = ObjectProperty(None)
    lt_name = ObjectProperty(None)
    phone = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def reg_accout(self):
        passw = self.hash_password(self.password.text)

        if(self.email.text.find("@") == -1):
            self.pop_error("Invalid Email")
            print("invalid email")
        elif(len(self.phone.text) < 10 or len(self.phone.text) > 10):
            self.pop_error("Invalid Phone Number")
            print("invalid Phone")
        else:
            db.create_user(self.fr_name.text, self.lt_name.text, self.email.text, passw,
                        self.phone.text,"Not", "Patient")
            wm.screen_manager.current = "pat_login"

    def pop_error(self, message):
        popup = Popup(title = "Bad Data",
                      content = Label(text = message),
                      size_hint = (None, None), size = (400, 400))
        popup.open()

    def reset_inputs(self):
        self.fr_name.text = ""
        self.lt_name.text = ""
        self.phone.text = ""
        self.email.text = ""
        self.password.text = ""

    def hash_password(self, password):
        """Hash a password for storing."""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                    salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')

    def find_help(self):
        help.prev_window = "reg_acc_win"

        help.text = ("""
                      Enter words of wisdom here.
                      """)

        wm.screen_manager.current = "help"
