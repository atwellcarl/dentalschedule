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

# A window allowing doctor or hygenist to login
class StaffLoginWindow(Screen):
    kv = Builder.load_file("stylefolders/slw.kv")
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def login(self):

        em = self.email.text
        passw = self.password.text
        # need database validation

        if(db.is_user(em, passw, "Employee")):
            self.reset_inputs()
            user_info[0] = db.get_emp_id(em)
            user_info[1] = "Employee"
            user_info[2] = em
            wm.screen_manager.current = "st_home"
        else:
            self.invalid_staff_login()

    def invalid_staff_login(self):
        popup = Popup(title = "Login Failed",
                      content = Label(text = "Invalid email or passowrd."),
                      size_hint = (None, None), size = (400, 400))
        popup.open()
        
    # def logout(self):
    #     for info in user_info:
    #         print (info)
    #     for info in user_info:
    #         info = None
    def reset_inputs(self):
        self.email.text = ""
        self.password.text = ""
