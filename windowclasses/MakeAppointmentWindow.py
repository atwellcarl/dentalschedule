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
class MakeAppointmentWindow(Screen):
    kv = Builder.load_file("stylefolders/maw.kv")
    description = ObjectProperty(None)
    dr_list = []

    def choose(self):
        emp_list = db.list_employees()
        for employee in emp_list:
            if(employee[0] == "Doctor"):
                self.dr_list.append(employee)
        y_pos = .6

        for doctor in self.dr_list:
            self.b = Button(text = ("{} {}".format(doctor[1], doctor[2])), size_hint = (.25, .1),
            pos_hint = {"center_x": .5, "center_y": y_pos })
            self.b.bind(on_release = self.pressed)
            self.add_widget(self.b)
            y_pos -= .1

    def pressed(self, instance):
        for doctor in self.dr_list:
            dr = "{} {}".format(doctor[1], doctor[2])
            if(instance.text == dr):
                dr_info[0] = doctor[3]
        plw.user_info[3] = self.description.text
        mw.screen_manager.current = "calendar"
        self.description.text = ""
