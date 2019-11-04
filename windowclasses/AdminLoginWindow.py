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
# A window for the admin to login
class AdminLoginWindow(Screen):
    kv = Builder.load_file("stylefolders/alw.kv")
    password = ObjectProperty(None)
    email = ObjectProperty(None)

    def login(self):

        passw = self.password.text
        em = self.email.text
        if(db.is_user(em, passw, "Admin")):
            user_info[0] = db.get_emp_id(em)
            user_info[1] = "Admin"
            user_info[2] = em
            wm.screen_manager.current = "admin_action"
        else:
            self.invalid_admin_login()

    def invalid_admin_login(self):
        popup = Popup(title = "Login Failed",
                      content = Label(text = "Invalid email or passowrd."),
                      size_hint = (None, None), size = (400, 400))
        popup.open()

    def reset_inputs(self):
        self.password.text = ""
        self.email.text = ""
