'''
 Inquires about what administrative actions the Admin
 would like to perform.

 Author: Carl Atwell
 Date: 12/10/2019
'''

from windowclasses import WindowManager as wm
from windowclasses import AdminLoginWindow as alw
from windowclasses import Help as help
from kivy.config import Config
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


class AdminActionWindow(Screen):
    kv = Builder.load_file("stylefolders/aaw.kv")

    def create_staff(self):
        wm.screen_manager.current = "create_staff"

    def setup_calendar(self):
        wm.screen_manager.current = "setup_calendar"

    def manage_accounts(self):
        wm.screen_manager.current = "manage_accounts"

    def logout(self):
        for info in alw.user_info:
            info = None
        wm.screen_manager.current = "user"

    def find_help(self):
        help.prev_window = "admin_action"

        help.text = ("""
                      This the main page for the admin to perform administrative
                      actions. The main actions are creating new employee users
                      and managing new user accounts.""")

        wm.screen_manager.current = "help"
