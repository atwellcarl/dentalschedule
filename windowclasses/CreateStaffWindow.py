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

import db_control as db

class CreateStaffWindow(Screen):
    kv = Builder.load_file("stylefolders/csw.kv")
    fr_name = ObjectProperty(None)
    lt_name = ObjectProperty(None)
    phone = ObjectProperty(None)
    email = ObjectProperty(None)
    passowrd = ObjectProperty(None)
    emp_type = ObjectProperty(None)

    def creat_acc(self):
        db.create_user(self.fr_name.text, self.lt_name.text, self.email.text,
                        self.password.text, self.phone.text, self.emp_type.text,
                        "Employee")

    def reset_inputs(self):
        self.fr_name.text = ""
        self.lt_name.text = ""
        self.phone.text = ""
        self.email.text = ""
        self.password.text = ""
        self.emp_type.text = ""
