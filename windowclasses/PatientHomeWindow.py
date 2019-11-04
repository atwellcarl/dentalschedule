from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from windowclasses import WindowManager as mw
from windowclasses import PatientLoginWindow as plw
import db_control as db


class PatientHomeWindow(Screen):
    kv = Builder.load_file("stylefolders/phw.kv")
    appointment = ObjectProperty(None)

    def logout(self):
        for info in plw.user_info:
            print (info)
        for info in plw.user_info:
            info = None

    def get_app(self):
        schedule = db.view_user_schedule(int(plw.user_info[0]), "Patient")
        if(len(schedule) != 0):
            self.appointment.text = ""
            for app in schedule:
                line1 = "Date: {}".format(app[0])
                line2 = "Time: {}".format(app[1])
                line3 = "Description: {}".format(app[3])
                line4 = "With: Dr {} {}".format(app[4], app[5])
                self.appointment.text += "{}\n {}:00\n {}\n {}\n\n".format(line1, line2, line3, line4)
        else:
            self.appointment.text = "No Appointments Scheduled"

    def make_appointment(self):
        mw.screen_manager.current = "make_appointment"
