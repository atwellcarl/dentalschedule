'''
 A window allowing doctor or hygenist to login. If someone
 has edited their schedule a popup will be displayed upon
 successful login.

 Author: Carl Atwell
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
import db_control as db

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
user_info = [None] * 4


class StaffLoginWindow(Screen):
    kv = Builder.load_file("stylefolders/slw.kv")
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    # Validates user credentials by grabbing user inputs
    # and checking the database.
    def login(self):
        em = self.email.text
        passw = self.password.text

        if(db.is_user(em, passw, "Employee")):
            self.reset_inputs()
            user_info[0] = db.get_emp_id(em)
            user_info[1] = "Employee"
            user_info[2] = em

            # Check is the users schedule has been edited
            if(db.has_notification("Employee", user_info[0]) == 1):
                self.pop_up("Schedule Change", "Your Schedule has changed since you last \nloged in. Please review your new schedule\ndisplayed on the homepage.")
            wm.screen_manager.current = "st_home"
        else:
            self.pop_up("Login Failed", "The email or password provided was not correct.")

    # Pop up window for giving the user feedback
    # handles errors or successful operations
    def pop_up(self, header, info):
        popup = Popup(title = header,
                      content = Label(text = info),
                      size_hint = (None, None), size = (400, 400))
        popup.open()

    # Sets all input fields to the empty string
    def reset_inputs(self):
        self.email.text = ""
        self.password.text = ""

    # Sets the Help screen text to helpful information about the page.
    def find_help(self):
        help.prev_window = "st_login"

        help.text = ("""
                      To login you will need your personal email and
                      the password for your account. If it is your first
                      time loging in as an employee, please contact the
                      admin for your login credentials. If you have
                      forgotten your credentials you will again need to
                      speak with the admin.
                      """)

        wm.screen_manager.current = "help"
