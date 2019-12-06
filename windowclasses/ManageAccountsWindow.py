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

class ManageAccountsWindow(Screen):
    kv = Builder.load_file("stylefolders/maccw.kv")
    email = ObjectProperty(None)

    #Method for reactivating a previously deactivated user account
    def reactivate(self):
        if(self.email.text.find("@") == -1):
            self.pop_up("Bad Data", "Invalid Email")
        else:
            self.pop_up("Avtivated", "The selected account has been reactivated")
            print(self.email.text)
            self.email.text = ""

    #Method for deactivating an user acount. Soft delete in data base
    def deactivate(self):
        if(self.email.text.find("@") == -1):
            self.pop_up("Bad Data", "Invalid Email")
        else:
            self.pop_up("Deactivated", "The selected account has been deactivated")
            print(self.email.text)
            self.email.text = ""

    # This is a pop window that handles most system feedback to the user
    def pop_up(self, header, message):
        popup = Popup(title = header,
                      content = Label(text = message),
                      size_hint = (None, None), size = (400, 400))
        popup.open()
