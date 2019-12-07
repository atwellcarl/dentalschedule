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

import hashlib, binascii, os
import db_control as db

# This class handles the logic for when the Admin creates a new
# employee account
class CreateStaffWindow(Screen):
    kv = Builder.load_file("stylefolders/csw.kv")
    fr_name = ObjectProperty(None)
    lt_name = ObjectProperty(None)
    phone = ObjectProperty(None)
    email = ObjectProperty(None)
    passowrd = ObjectProperty(None)
    emp_type = ObjectProperty(None)

    # validates inputs and creates and account
    def creat_acc(self):
        passw = self.hash_password(self.password.text)
        if(self.email.text.find("@") == -1):
            self.pop_up("Bad Data", "Invalid Email")
        elif(len(self.phone.text) < 10 or len(self.phone.text) > 10):
            self.pop_up("Bad Data", "Invalid Phone Number")
        elif(self.emp_type.text == "Doctor"):
            db.create_user(self.fr_name.text, self.lt_name.text, self.email.text,
                            passw, self.phone.text, self.emp_type.text,
                            "Employee")
            self.pop_up("Account Created", "{} {}'s account created".format(self.fr_name.text, self.lt_name.text))
            self.reset_inputs()
        elif(self.emp_type.text == "Hygienist"):
            db.create_user(self.fr_name.text, self.lt_name.text, self.email.text,
                            passw, self.phone.text, self.emp_type.text,
                            "Employee")
            self.pop_up("Account Created", "{} {}'s account created".format(self.fr_name.text, self.lt_name.text))
            self.reset_inputs()
        # data inputs are good, so create the account
        else:
            self.pop_up("Bad Data", "Invalid employee type\n (Must be Doctor or Hygienist)")


    # Pop up window for giving the user feedback
    # handles errors or successful operations
    def pop_up(self,header, message):
        popup = Popup(title = header,
                      content = Label(text = message),
                      size_hint = (None, None), size = (400, 400))
        popup.open()

    #Sets all user intput feilds to the empty string
    def reset_inputs(self):
        self.fr_name.text = ""
        self.lt_name.text = ""
        self.phone.text = ""
        self.email.text = ""
        self.password.text = ""
        self.emp_type.text = ""

    # salts and hashes a given string. Returns the hash
    def hash_password(self, password):
        """Hash a password for storing."""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                    salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')
