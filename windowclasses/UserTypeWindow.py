'''
 Inquires users as to which type of user they are, patient or staff.

 Author: Carl Atwell, Darian Boeck, and Andrew Valdez
 Date: 12/10/2019
'''
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


Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


class UserTypeWindow(Screen):
    kv = Builder.load_file("stylefolders/utw.kv")

    # Takes a patient to their login page
    def patient(self):
        wm.screen_manager.current = "pat_login"

    # Takes a staff member to the choose staff type page
    def staff(self):
        wm.screen_manager.current = "staff_type"

    # Sets the Help text to usefule information about the page
    def find_help(self):
        help.prev_window = "user"

        help.text = ("""
                      Hello,
                      The page you were just on is meant to direct patients
                      and dental office employees to the appropriate login
                      page. If you do not work for the office and would like
                      to sign up or sign into an account, please choose the
                      patient button.

                                      For further assitance feel free
                                        to call our office directly
                                               608-444-1212
                      """)

        wm.screen_manager.current = "help"
