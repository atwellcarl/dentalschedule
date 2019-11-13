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

class PatientEditAppWindow(Screen):
    kv = Builder.load_file("stylefolders/peaw.kv")
