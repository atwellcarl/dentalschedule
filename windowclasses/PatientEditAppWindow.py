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
from windowclasses import WindowManager as mw
from kivy.uix.label import Label
from windowclasses import PatientLoginWindow as plw
import db_control as db

class PatientEditAppWindow(Screen):
    kv = Builder.load_file("stylefolders/peaw.kv")
    appointment = ObjectProperty(None)
    global buttons
    buttons = []

    def get_app(self):
        pos_x = .15
        pos_y = .65
        schedule = db.view_user_schedule(int(plw.user_info[0]), "Patient")
        if(len(schedule) != 0):
            self.appointment.text = ""
            for app in schedule:
                self.button = Button(text = "Date: {}\nTime:{}:00\nWith: Dr: {} {}".format(app[0],app[1],app[4],app[5]),
                    font_size = 16, size_hint = (.225, .125),
                    pos_hint = {"x": pos_x, "y": pos_y})
                self.add_widget(self.button)
                buttons.append(self.button)
                pos_y -= .15
                
                if (pos_y <= .1):
                    pos_x += .25
                    pos_y = .65
                #line1 = "Date: {}".format(app[0])
                #line2 = "Time: {}".format(app[1])
                #line3 = "Description: {}".format(app[3])
                #line4 = "With: Dr {} {} and Hygenist {} {}".format(app[4], app[5], app[6], app[7])
                #self.appointment.text += "{}\n {}:00\n {}\n {}\n\n".format(line1, line2, line3, line4)
        else:
            self.appointment.text = "No Appointments Scheduled"
    def remove_buttons(self):
        for item in buttons:
            self.remove_widget(item)