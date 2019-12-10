'''
 This is the class that allows patient users to naviage their home page.
 They can view their schedule uppon entry and make or edit appointments.

 Author: Carl Atwell, Darian Boeck
 Date: 12/10/2019
'''
from windowclasses import WindowManager as wm
from windowclasses import PatientLoginWindow as plw
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
import time

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


class PatientHomeWindow(Screen):
    kv = Builder.load_file("stylefolders/phw.kv")
    appointment = ObjectProperty(None)
    time = time.localtime(time.time())
    labels = []

    # helper method for changing schedule labels
    def clean_labels (self):
        for item in self.labels:
            self.remove_widget(item)
        self.labels = []

    # performs the user logout. Sets globals to none
    def logout(self):
        for info in plw.user_info:
            print (info)
        for info in plw.user_info:
            info = None
        self.clean_labels()

    # helper method to remove labels from the screen
    def remove_labels(self):
        for item in self.labels:
            self.remove_widget(item)

    # This method is called upon login to display
    # the users schedule
    def get_app(self):
        for item in self.labels:
            self.remove_widget(item)

        pos_x = .035
        pos_y = .75
        schedule = db.view_user_schedule(int(plw.user_info[0]), "Patient")
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
                    if ( (len(self.labels)) % 3 == 0):
                        pos_x += .225
                        pos_y = .75
        else:
            self.appointment.text = "No Appointments Scheduled"

    # helper method for changing to the make appointment window
    def make_appointment(self):
        wm.screen_manager.current = "make_appointment"

    # Sets the Help screen text to useful information about a
    # user's personal home page.
    def find_help(self):
        help.prev_window = "pat_home"

        help.text = ("""
                      The previous page is your personalized homepage. It
                      displays any appointments you scheduled in the future.
                      From there you can perform actions such as scheduling
                      a new appointment or deleting a current one.

                                    For further assitance feel free
                                      to call our office directly
                                             608-444-1212
                      """)

        wm.screen_manager.current = "help"
