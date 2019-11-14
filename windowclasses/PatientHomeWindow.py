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
import time


class PatientHomeWindow(Screen):
    kv = Builder.load_file("stylefolders/phw.kv")
    appointment = ObjectProperty(None)
    time = time.localtime(time.time())

    def logout(self):
        for info in plw.user_info:
            print (info)
        for info in plw.user_info:
            info = None

    def get_app(self):
        schedule = db.view_user_schedule(int(plw.user_info[0]), "Patient")
        cur_time = ("{}{}{}{}".format(self.time.tm_year, self.time.tm_mon,
                    self.time.tm_mday, self.time.tm_hour))
        if(len(schedule) != 0):
            self.appointment.text = ""
            for app in schedule:
                # run a check to see if app has passed
                temp = app[0].split("-")
                temp2 = app[1].split(":")
                app_time = 0
                if(int(temp2[0]) < 10):
                    app_time = "{}{}{}{}0".format(temp[0], temp[1], temp[2], temp2[0])
                else:
                    app_time = "{}{}{}{}".format(temp[0], temp[1], temp[2], temp2[0])

                if(int(app_time) >= int(cur_time)):
                    line1 = "Date: {}".format(app[0])
                    line2 = "Time: {}".format(app[1])
                    line3 = "Description: {}".format(app[3])
                    line4 = "With: Dr. {} {} and Hygenist {} {}".format(app[4], app[5], app[6], app[7])
                    self.appointment.text += "{}\n {}:00\n {}\n {}\n\n".format(line1, line2, line3, line4)
        else:
            self.appointment.text = "No Appointments Scheduled"

    def make_appointment(self):
        mw.screen_manager.current = "make_appointment"
