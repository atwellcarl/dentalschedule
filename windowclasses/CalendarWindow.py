from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

from windowclasses import WindowManager as wm
from windowclasses import PatientLoginWindow as plw
from windowclasses import MakeAppointmentWindow as maw
import db_control as db


import calendar

class CalendarWindow(Screen):
    kv = Builder.load_file("stylefolders/cw.kv")
    year = 2019
    month = 10
    week = 4

    c = calendar.TextCalendar(calendar.SUNDAY)
    p = c.monthdatescalendar(year, month)
    def pop_cal(self):
        pos_x = .15
        pos_y = .65
        list = ["Sunday", "Monday", "Teusday", "Wednesday", "Thursday", "Friday", "Saturday"]

        for day in range(7):
            self.l = Button(text = str("{}\n{}".format(list[day], self.p[self.week][day])),
                            size_hint = (.1, .05),
                            pos_hint = {"x": pos_x, "y":.7})
            self.add_widget(self.l)
            pos_x += .1

        pos_x = .15
        for j in range(8):
            for i in range(7):
                if(i == 0 or i == 6):
                    self.b = Button(text = "{}:00".format(str(j + 8)), font_size = 20, size_hint = (.1, .05),
                                pos_hint = {"x": pos_x, "y": pos_y})
                    self.b.color = (1, 0, 0, 1)
                    self.add_widget(self.b)
                else:
                    # id should be date
                    self.b = Button(id = ("{}".format(str(self.p[self.week][i]))),
                                    text = "{}:00".format(str(j + 8)), font_size = 20,
                                    size_hint = (.1, .05),
                                    pos_hint = {"x": pos_x, "y": pos_y})
                    self.b.bind(on_release = self.pressed)
                    self.add_widget(self.b)
                pos_x += .1
            pos_y -= .05
            pos_x = .15

    def next_week(self):
        if(self.week < 4):
            self.week += 1
        elif(self.week >= 4 and self.month < 12):
            self.week = 1
            self.month += 1
            self.p = self.c.monthdatescalendar(self.year, self.month)

        self.pop_cal()

    def prev_week(self):
        if(self.week >= 4):
            self.week -= 1
        elif(self.week <= 4 and self.month > 1):
            self.week = 52
            self.month = 12
            self.p = self.c.monthdatescalendar(self.year, self.month)

        self.pop_cal()

    def pressed(self, instance):

        start = instance.text.split(":")[0]
        db.create_appointment(instance.id, int(start),
                              plw.user_info[3], 1, plw.user_info[2], maw.dr_info[0])
        wm.screen_manager.current = "pat_home"
