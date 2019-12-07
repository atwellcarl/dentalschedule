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
from windowclasses import Help as help
from windowclasses import WindowManager as wm



class SetupCalendarWindow(Screen):
    kv = Builder.load_file("stylefolders/scw.kv")
    def find_help(self):
        help.prev_window = "setup_calendar"

        help.text = ("""
                      Enter words of wisdom here.
                      """)

        wm.screen_manager.current = "help"
