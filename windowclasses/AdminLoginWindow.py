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

import db_control as db

user_info = [None] * 4

# A window for the admin to login
class AdminLoginWindow(Screen):
    kv = Builder.load_file("stylefolders/alw.kv")
    password = ObjectProperty(None)
    email = ObjectProperty(None)

    # Method handles login logic
    def login(self):
        # retrieve user entered data
        passw = self.password.text
        em = self.email.text

        # check if the credentials are correct
        if(db.is_user(em, passw, "Admin")):
            user_info[0] = db.get_emp_id(em)
            user_info[1] = "Admin"
            user_info[2] = em
            wm.screen_manager.current = "admin_action"

        # inform user that password or email was incorrect
        else:
            self.invalid_admin_login()

    # Pop up window to provide user with a message in
    # case of a failed login
    def invalid_admin_login(self):
        popup = Popup(title = "Login Failed",
                      content = Label(text = "Invalid email or passowrd."),
                      size_hint = (None, None), size = (400, 400))
        popup.open()

    # Set login text boxes to empty strings
    def reset_inputs(self):
        self.password.text = ""
        self.email.text = ""

    def find_help(self):
        help.prev_window = "admin_login"

        help.text = ("""
                      The previous page is meant only for the admin to login.
                      If you are not the admin, please click the back button
                      to return and choose a different user type.
                      """)

        wm.screen_manager.current = "help"
