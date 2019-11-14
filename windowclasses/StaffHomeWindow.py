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
from windowclasses import StaffLoginWindow as slw
import db_control as db


class StaffHomeWindow(Screen):
    kv = Builder.load_file("stylefolders/shw.kv")
    appointment = ObjectProperty(None)

    def edit_schedule(self):
        print("Feature Unavailable")

    def get_app(self):
        schedule = db.view_user_schedule(int(slw.user_info[0]), "Employee")
        if(len(schedule) != 0):
            self.appointment.text = ""
            for app in schedule:
                line1 = "Date: {}".format(app[0])
                line2 = "Time: {}".format(app[1])
                line3 = "Description: {}".format(app[3])
                line4 = "With: {} {}".format(app[4], app[5])
                self.appointment.text += "{}\n {}:00\n {}\n {}\n\n".format(line1, line2,
                                                                    line3, line4)
        else:
            self.appointment.text = "No Current Appointments."

    def logout(self):
        for info in slw.user_info:
            print(info)
        for info in slw.user_info:
            info = None
