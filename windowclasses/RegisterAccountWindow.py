'''
 This class allows a patient user to register an account

 Author: Carl Atwell and Darian Boeck
 Date: 12/10/2019
'''
from windowclasses import WindowManager as wm
from windowclasses import Help as help
from kivy.config import Config
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
import hashlib, binascii, os
import db_control as db

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


class RegisterAccountWindow(Screen):
    kv = Builder.load_file("stylefolders/raw.kv")
    fr_name = ObjectProperty(None)
    lt_name = ObjectProperty(None)
    phone = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    # grabs user input from the page, validates input,
    # and creates the new user
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

    # A pop up used to inform the user that their input was invalid
    def pop_error(self, message):
        popup = Popup(title = "Bad Data",
                      content = Label(text = message),
                      size_hint = (None, None), size = (400, 400))
        popup.open()

    # sets all user input fields to the empty string
    def reset_inputs(self):
        self.fr_name.text = ""
        self.lt_name.text = ""
        self.phone.text = ""
        self.email.text = ""
        self.password.text = ""

    # salts and hashes the user password
    def hash_password(self, password):
        """Hash a password for storing."""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                    salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')

    # Sets the Help screen text to useful information about the page.
    def find_help(self):
        help.prev_window = "reg_acc_win"

        help.text = ("""
                      To register a new account please fill in every field.
                      After register account is clicked you will be able taken
                      back to the patient login page where you can immediatly
                      enter your email and password to be taken to your brand
                      new personal homepage.

                                    For further assitance feel free
                                      to call our office directly
                                             608-444-1212
                      """)

        wm.screen_manager.current = "help"
