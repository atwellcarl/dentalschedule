'''
 This class allows a staff member to delete appointments from their
 schedule. Populates a page with buttons that when clicked
 delete the associated appointment from the database.

 Author: Carl Atwell
 Date: 12/10/2019
'''
from windowclasses import WindowManager as wm
from windowclasses import StaffLoginWindow as slw
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

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


class StaffEditAppWindow(Screen):
    kv = Builder.load_file("stylefolders/seaw.kv")
    appointment = ObjectProperty(None)
    global buttons
    buttons = []

    # gets the users schedule an displays it in buttons that will
    # delete the appointment upon clicking
    def get_app(self):
        pos_x = .15
        pos_y = .65
        schedule = db.view_user_schedule(int(slw.user_info[0]), "Employee")
        row = 0
        if(len(schedule) != 0):
            self.appointment.text = ""
            for app in schedule:
                self.button = Button(id = str(row), text = "Date: {}\nTime:{}:00\nFor A: {}".format(app[0],app[1],app[3]),
                    font_size = 16, size_hint = (.225, .125),
                    pos_hint = {"x": pos_x, "y": pos_y})
                self.button.bind(on_release = self.delete_app)
                self.add_widget(self.button)
                buttons.append(self.button)
                pos_y -= .15
                row += 1

                if (pos_y <= .1):
                    pos_x += .25
                    pos_y = .65
        else:
            self.appointment.text = "No Appointments Scheduled"

    # A helper method for removing buttons from the screen
    def remove_buttons(self):
        for item in buttons:
            self.remove_widget(item)

    # Calls the database delete method for an appoinment
    # associated with the button
    def delete_app(self, instance):
        db.delete_appt(int(instance.id), slw.user_info[0], "Employee")
        self.pop("The appointment you selected has been deleted.")
        wm.screen_manager.current = "st_home"

    # Displays to the user that the appointment was deleted
    def pop(self, message):
        popup = Popup(title = "Appointment Deleted",
                      content = Label(text = message),
                      size_hint = (None, None), size = (400, 400))
        popup.open()

    # Sets the Help screen text to useful information about the page
    def find_help(self):
        help.prev_window = "staff_edit_app"

        help.text = ("""
                      The page you were just on is for removing an
                      appointment from your schedule. To do this,
                      simply click the button corresponding to the
                      appointment you would like to change. If no
                      appointments appear, then your schedule is
                      free. PLease note, that deleting an appointment
                      will change other users' schedules.

                            For further assitance, contact
                               your supervisor or admin
                      """)

        wm.screen_manager.current = "help"
