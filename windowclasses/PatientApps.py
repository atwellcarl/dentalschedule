'''
 This class sets the window text to the schedule of the user
 associated with the global variables.

 Author: Darian Boeck
 Date: 12/10/2019
'''
from windowclasses import Help as help
from windowclasses import PatientLoginWindow as plw
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
email = ""
type = ""


class PatientApps(Screen):

    kv = Builder.load_file("stylefolders/pa.kv")
    appointment = ObjectProperty(None)
    time = time.localtime(time.time())
    labels = []

    # Gets the users schedule and displays it on the window
    def get_app(self):
        global email, type

        for item in self.labels:
            self.remove_widget(item)
        pos_x = .035
        pos_y = .75
        schedule = []
        if type == "Patient":
                schedule = db.view_user_schedule(int(db.get_pat_id(email)), "Patient")

                cur_time = ("{}{}{}{}".format(self.time.tm_year, self.time.tm_mon,
                            self.time.tm_mday, self.time.tm_hour))
                if(len(schedule) != 0):
                    self.appointment.text = ""
                    for app in schedule:
                        temp = app[0].split("-")
                        temp2 = app[1].split(":")
                        app_time = 0
                        if(int(temp2[0]) < 10):
                            app_time = "{}{}{}0{}".format(temp[0], temp[1], temp[2], temp2[0])
                        else:
                            app_time = "{}{}{}{}".format(temp[0], temp[1], temp[2], temp2[0])
                        if(int(app_time) >= int(cur_time)):
                            line1 = "Date: {}".format(app[0])
                            line2 = "Time: {}".format(app[1])
                            line3 = "Description: {}".format(app[3])
                            line4 = "Dr: {} {}\nHygienist: {} {}".format(app[4], app[5], app[6], app[7])
                            line5 = "{}\n{}:00\n{}\n{}\n\n".format(line1, line2, line3, line4)

                            lbl = Label(text = line5, font_size=15, pos_hint = {"x": pos_x, "y": pos_y}, size_hint = (.225, .125), color=[255,255,255,1])
                            self.labels.append(lbl)

                            self.add_widget(lbl)
                            pos_y -= .185
                            if ((len(self.labels)) % 3 == 0):
                                pos_x += .225
                                pos_y = .75
                else:
                    self.appointment.text = "No Appointments Scheduled"
        else:
            schedule = db.view_user_schedule(int(db.get_emp_id(email)), "Employee")
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

    # Sets the Help screen to useful information about the page
    def find_help(self):
        help.prev_window = "manage_accounts"

        help.text = ("""
                      The previous page is used soley to view a users schedule.
                      No actons can be performed.
                      """)

        wm.screen_manager.current = "help"
