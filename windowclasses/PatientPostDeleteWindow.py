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

class PatientPostDeleteWindow(Screen):
    kv = Builder.load_file("stylefolders/ppdw.kv")

    def find_help(self):
        help.prev_window = "pat_post_del"

        help.text = ("""
                      The page you were just on is meant for choosing
                      whether to create a new appointment in place of
                      the one you deleted or return to your personalized
                      homepage. If you choose to return to the homepage
                      you can still create a new appointment by clicking
                      the appropriate button.

                                    For further assitance feel free
                                      to call our office directly
                                             608-444-1212
                      """)

        wm.screen_manager.current = "help"
