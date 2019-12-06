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
from windowclasses import PatientLoginWindow as plw
import db_control as db

dr_info = [None] * 4
# This class handles the logic for the make appointment window
class MakeAppointmentWindow(Screen):
    kv = Builder.load_file("stylefolders/maw.kv")
    description = ObjectProperty(None)
    choose_button = ObjectProperty(None)
    dr_list = []
    list_filled = False
    dr_button = []
    hygen_button = []

    # Changes the choose button text
    def no_func(self, button_text):
        # self.remove_widget(self.choose_button)
        self.button = Button(text = button_text, size_hint = (.25, .1),
                        pos_hint = {"center_x": .5, "center_y": .7})
        self.add_widget(self.button)

    # populates the page with buttons coreesponding to drs
    def choose_dr(self):
        button = Button(text = "Choose a Doctor", size_hint = (.25, .1),
                        pos_hint = {"center_x": .5, "center_y": .7})
        self.add_widget(button)
        if(self.list_filled == False):
            emp_list = db.list_employees()
            for employee in emp_list:
                if(employee[0] == "Doctor"):
                    self.dr_list.append(employee)
            self.list_filled = True
        y_pos = .6
        for doctor in self.dr_list:
            self.b = Button(text = ("{} {}".format(doctor[1], doctor[2])), size_hint = (.25, .1),
            pos_hint = {"center_x": .5, "center_y": y_pos })
            self.b.bind(on_release = self.dr_pressed)
            self.add_widget(self.b)
            self.dr_button.append(self.b)
            y_pos -= .1

    # populates the page with buttons corresponding to hygienists
    def choose_hygen(self):
        emp_list = db.list_employees()
        for employee in emp_list:
            if(employee[0] == "Hygenist"):
                self.dr_list.append(employee)
        y_pos = .6
        for doctor in self.dr_list:
            self.b = Button(text = ("{} {}".format(doctor[1], doctor[2])), size_hint = (.25, .1),
            pos_hint = {"center_x": .5, "center_y": y_pos })
            self.b.bind(on_release = self.hygen_pressed)
            self.add_widget(self.b)
            self.hygen_button.append(self.b)
            y_pos -= .1
        self.list_filled = False

    # The doctor has been choosen so save the email and prompt
    # for a hygienists
    def dr_pressed(self, instance):
        for doctor in self.dr_list:
            dr = "{} {}".format(doctor[1], doctor[2])
            if(instance.text == dr):
                dr_info[0] = doctor[3]
        self.dr_list = []
        for button in self.dr_button:
            self.remove_widget(button)
        self.no_func("Choose a hygenist")
        self.choose_hygen()

    def hygen_pressed(self, instance):
        for doctor in self.dr_list:
            dr = "{} {}".format(doctor[1], doctor[2])
            if(instance.text == dr):
                dr_info[1] = doctor[3]
        for button in self.hygen_button:
            self.remove_widget(button)
        # self.no_func("Choose a Doctor")
        self.dr_list = []
        # self.choose_dr()
        plw.user_info[3] = self.description.text
        mw.screen_manager.current = "calendar"
        self.description.text = ""
