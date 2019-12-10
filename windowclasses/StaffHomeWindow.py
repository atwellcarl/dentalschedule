'''
 This handels the staff user home page. Allows the user to see their
 schedule and choose to edit it. 

 Author: Carl Atwell and Darian Boeck
 Date: 12/10/2019
'''
from windowclasses import StaffLoginWindow as slw
from windowclasses import Help as help
from windowclasses import WindowManager as wm
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
import time

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


class StaffHomeWindow(Screen):
    kv = Builder.load_file("stylefolders/shw.kv")
    appointment = ObjectProperty(None)
    time = time.localtime(time.time())
    def edit_schedule(self):
        print("Feature Unavailable")

    # populates the staff home page with the user's schedule
    # called on page open
    def get_app(self):
        schedule = db.view_user_schedule(int(slw.user_info[0]), "Employee")
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
                if(int(cur_time) < int(app_time)):
                    line1 = "Date: {}".format(app[0])
                    line2 = "Time: {}".format(app[1])
                    line3 = "Description: {}".format(app[3])
                    line4 = "With: {} {}".format(app[4], app[5])
                    self.appointment.text += "{}\n {}:00\n {}\n {}\n\n".format(line1, line2,
                                                                        line3, line4)
        else:
            self.appointment.text = "No Current Appointments."

    # Sets globals to none to secure logout
    def logout(self):
        for info in slw.user_info:
            print(info)
        for info in slw.user_info:
            info = None

    # Sets Help screen text to useful information about the page
    def find_help(self):
        help.prev_window = "st_home"

        help.text = ("""
                      The page were just on is your personalized home page.
                      There, you cen view your schedule and make changes to
                      it by clicking buttons such as delete an appointment

                                        for futher assitance please
                                      contact your admin or supervisor.
                      """)

        wm.screen_manager.current = "help"
