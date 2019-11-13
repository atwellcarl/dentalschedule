#!python3.6
import calendar

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
import db_control as db

from windowclasses import WindowManager as wm
from windowclasses import AdminActionWindow as aaw
from windowclasses import AdminLoginWindow as alw
from windowclasses import CalendarWindow as cw
from windowclasses import CreateStaffWindow as csw
from windowclasses import MakeAppointmentWindow as maw
from windowclasses import ManageAccountsWindow as maccw
from windowclasses import PatientHomeWindow as phw
from windowclasses import PatientLoginWindow as plw
from windowclasses import RegisterAccountWindow as raw
from windowclasses import SetupCalendarWindow as scw
from windowclasses import StaffHomeWindow as shw
from windowclasses import StaffLoginWindow as slw
from windowclasses import StaffUserType as sut
from windowclasses import UserTypeWindow as utw
from windowclasses import PatientEditAppWindow as peaw

user_info = [None] * 4
dr_info = [None] * 4

# kv = Builder.load_file("win.kv")
screen_manager = wm.WindowManager()
wm.screen_manager = screen_manager

# A list of all windows
wm.windows.append(utw.UserTypeWindow(name = "user"))
wm.windows.append(sut.StaffUserType(name = "staff_type"))
wm.windows.append(plw.PatientLoginWindow(name = "pat_login"))
wm.windows.append(raw.RegisterAccountWindow(name = "reg_acc_win"))
wm.windows.append(phw.PatientHomeWindow(name = "pat_home"))
wm.windows.append(maw.MakeAppointmentWindow(name = "make_appointment"))
wm.windows.append(slw.StaffLoginWindow(name = "st_login"))
wm.windows.append(alw.AdminLoginWindow(name = "admin_login"))
wm.windows.append(aaw.AdminActionWindow(name = "admin_action"))
wm.windows.append(csw.CreateStaffWindow(name = "create_staff"))
wm.windows.append(scw.SetupCalendarWindow(name = "setup_calendar"))
wm.windows.append(maccw.ManageAccountsWindow(name = "manage_accounts"))
wm.windows.append(cw.CalendarWindow(name = "calendar"))
wm.windows.append(shw.StaffHomeWindow(name = "st_home"))
wm.windows.append(peaw.PatientEditAppWindow(name = "pat_edit_app"))

for window in wm.windows:
    screen_manager.add_widget(window)

screen_manager.current = "user"

class MyDentalApp(App):
    def build(self):
        return screen_manager

if __name__ == "__main__":
    MyDentalApp().run()
