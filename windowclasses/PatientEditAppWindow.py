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
from windowclasses import WindowManager as wm
from kivy.uix.label import Label
from windowclasses import PatientLoginWindow as plw
from windowclasses import Help as help


import db_control as db

class PatientEditAppWindow(Screen):
    kv = Builder.load_file("stylefolders/peaw.kv")
    appointment = ObjectProperty(None)
    # global buttons
    buttons = []

    def get_app(self):
        pos_x = .15
        pos_y = .65
        schedule = db.view_user_schedule(int(plw.user_info[0]), "Patient")
        row = 0
        if(len(schedule) != 0):
            self.appointment.text = ""
            for app in schedule:
                self.button = Button(id = str(row), text = "Date: {}\nTime:{}:00\nFor A: {}".format(app[0],app[1],app[3]),
                    font_size = 16, size_hint = (.225, .125),
                    pos_hint = {"x": pos_x, "y": pos_y})
                self.button.bind(on_release = self.delete_app)
                self.add_widget(self.button)
                self.buttons.append(self.button)
                pos_y -= .15
                row += 1

                if (pos_y <= .1):
                    pos_x += .25
                    pos_y = .65
        else:
            self.appointment.text = "No Appointments Scheduled"

    def remove_buttons(self):
        for item in self.buttons:
            self.remove_widget(item)

    def delete_app(self, instance):
        print("{} {} {}".format(int(instance.id), plw.user_info[0], "Patient"))

        db.delete_appt(int(instance.id), plw.user_info[0], "Patient")
        self.remove_buttons()
        self.pop("The appointment you selected has been deleted.")
        wm.screen_manager.current = "pat_post_del"

    def pop(self, message):
        popup = Popup(title = "Appointment Deleted",
                      content = Label(text = message),
                      size_hint = (None, None), size = (400, 400))
        popup.open()

    def find_help(self):
        help.prev_window = "pat_edit_app"

        help.text = ("""
                      The previous page is meant for delting a current
                      appointment. To delete an appointment simply click
                      the button corresponding to it. You will be notified
                      immediatly of it's deletion and taken to a new page
                      to either schedule a new appointment or return to your
                      homepage. If no buttons appear, then you do not have
                      any future appointments and you should click the back
                      button to return back to your homepage.

                                    For further assitance feel free
                                      to call our office directly
                                             608-444-1212
                      """)

        wm.screen_manager.current = "help"
