'''
 This class handles program control as users checnge
 from one screen to another. It inherits all of its
 functions from ScreenManager, a Kivy class. To switch
 windows one must import this class and set the gloabal
 variable screen_manager to the their desired page.

 Author: Carl Atwell
 Date: 12/10/2019
'''
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
windows = []
screen_manager = None


class WindowManager(ScreenManager):
    pass
