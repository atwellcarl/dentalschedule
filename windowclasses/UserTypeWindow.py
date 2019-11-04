from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

from windowclasses import WindowManager as wm

class UserTypeWindow(Screen):
    kv = Builder.load_file("stylefolders/utw.kv")
    def patient(self):
        wm.screen_manager.current = "pat_login"
    def staff(self):
        wm.screen_manager.current = "staff_type"
