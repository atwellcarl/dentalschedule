'''
 Allows a user to choose which kindo fo employee they are to
 be taken to their associated login pages.

 Author: Carl Atwell, Darian Boeck, and Andrew Valdez
 Date: 12/10/2019
'''
from windowclasses import WindowManager as wm
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

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


class StaffUserType(Screen):
    kv = Builder.load_file("stylefolders/sut.kv")

    # Takes a doctor to their login
    def doctor(self):
        wm.screen_manager.current = "st_login"

    # Takes a hygienist to their login
    def hygenist(self):
        wm.screen_manager.current = "st_login"

    # Takes the Admin to their login
    def admin(self):
        wm.screen_manager.current = "admin_login"

    # Sets the Help screen text to useful information about the page
    def find_help(self):
        help.prev_window = "staff_type"

        help.text = ("""
                      The page you were just on is meant to direct employees
                      to their corresponding logins based on job title. (for
                      example, if you are a Hygienist click the Hygienist button)

                                        For further asistance, please
                                           contact your supervisor
                      """)

        wm.screen_manager.current = "help"
