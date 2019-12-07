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
import db_control as db

text = "No wisdom here"
prev_window = "user"
class Help(Screen):
    kv = Builder.load_file("stylefolders/help.kv")
    words = ObjectProperty(None)

    def set_words(self):
        global text
        self.words.text = text

    def go_back(self):
        global text, prev_window
        text = "No Wisdom here"
        self.set_words()
        wm.screen_manager.current = prev_window
