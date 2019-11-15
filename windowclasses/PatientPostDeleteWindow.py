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

class PatientPostDeleteWindow(Screen):
    kv = Builder.load_file("stylefolders/ppdw.kv")
