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
from windowclasses import AdminLoginWindow as alw

# Inquires about what administrative actions the Admin
# would like to perform
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
            print (info)
        for info in alw.user_info:
            info = None
