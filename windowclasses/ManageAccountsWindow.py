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
from windowclasses import Help as help
from windowclasses import WindowManager as wm


import db_control as db

class ManageAccountsWindow(Screen):
    kv = Builder.load_file("stylefolders/maccw.kv")
    email = ObjectProperty(None)
    type = ObjectProperty(None)
    id = 1

    def view_schedule(self):
        print("hmmm... this is darian work")

    #Method for reactivating a previously deactivated user account
    def reactivate(self):
        if(self.type.text == "Employee"):
            print(db.get_emp_id(self.email.text))
            if(db.get_emp_id(self.email.text) != None):
                self.pop_up("Activated", "The selected account has been reactivated")
                print(self.email.text)
                self.email.text = ""
                self.type.text = ""
            else:
                self.pop_up("Bad Data", "The user email provided could not be found in the system")
        elif(self.type.text == "Patient"):
            if(db.get_pat_id(self.email.text) != None):
                self.pop_up("Activated", "The selected account has been reactivated")
                print(self.email.text)
                self.email.text = ""
                self.type.text = ""
            else:
                self.pop_up("Bad Data", "The user email provided could not be found in the system")
        else:
            self.pop_up("Bad Data", "Invalid User Type")

    #Method for deactivating an user acount. Soft delete in data base
    def deactivate(self):
        if(self.type.text == "Employee"):
            if(db.get_emp_id(self.email.text) != None):
                self.id = db.get_emp_id(self.email.text)
                self.del_apps("Employee")
                db.delete_user("Employee", self.id)
                self.pop_up("Deactivated", "The selected account has been deactivated")
                self.email.text = ""
                self.type.text = ""
            else:
                self.pop_up("Bad Data", "The user email provided could not be found in the system")
        elif(self.type.text == "Patient"):
            if(db.get_pat_id(self.email.text) != None):
                self.id = db.get_pat_id(self.email.text)
                self.del_apps("Patient")
                db.delete_user("Patient", self.id)
                self.pop_up("Deactivated", "The selected account has been deactivated")
                self.email.text = ""
                self.type.text = ""
            else:
                self.pop_up("Bad Data", "The user email provided could not be found in the system")
        else:
            self.pop_up("Bad Data", "Invalid User Type")

    def del_apps(self, type):
        schedule = db.view_user_schedule(self.id, type)
        for app in range(len(schedule)):
            db.delete_appt(app, self.id, type)
    # This is a pop window that handles most system feedback to the user
    def pop_up(self, header, message):
        popup = Popup(title = header,
                      content = Label(text = message),
                      size_hint = (None, None), size = (400, 400))
        popup.open()

    def find_help(self):
        help.prev_window = "manage_accounts"

        help.text = ("""
                      The previous page is a multi purpose user action window.
                      By entering a user email and their user type (must be
                      "Patient" or "Employee" exactly) you will be able to view
                      their schedule or reactivate or deactivate their account.
                      Deactivating will deny a user access to the account until
                      you reactivate it.  
                      """)

        wm.screen_manager.current = "help"
