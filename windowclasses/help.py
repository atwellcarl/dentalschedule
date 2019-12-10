'''
 This window is for providing the user with some useful information
 about the page they were on and who they can contact for further
 information. Before a screen class switches to the help screen it
 should set the global text variable to the desired information and
 set prev_window equal to the string name of their current window.

 Author: Carl Atwell
 Date: 12/10/2019
'''
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
import db_control as db

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
text = "No wisdom here"
prev_window = "user"


class Help(Screen):
    kv = Builder.load_file("stylefolders/help.kv")
    words = ObjectProperty(None)

    # Sets the text box on the window equal to the global
    # variable text. Called immediately upon opening the
    # window
    def set_words(self):
        global text
        self.words.text = text

    # Sets the return page for the back button.
    def go_back(self):
        global text, prev_window
        text = "No Wisdom here"
        self.set_words()
        wm.screen_manager.current = prev_window
