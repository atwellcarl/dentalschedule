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
import time
import calendar

class CalendarWindow(Screen):
    kv = Builder.load_file("stylefolders/cw.kv")
    time = time.localtime(time.time())
    year = time.tm_year
    month = time.tm_mon
    week_math = calendar.monthrange(year, month)
    week = 0
    # if(week_math[0] == 0 and time.tm_mday%7 == 0):
    #     week = int(time.tm_mday/7)
    # else:
    week = int(time.tm_mday/7)

    c = calendar.TextCalendar(calendar.SUNDAY)
    p = c.monthdatescalendar(year, month)

    def employee_scheduled(self, j, i, day):
        dr_id = db.get_emp_id(maw.dr_info[0])
        list = db.view_user_schedule(dr_id, "Employee")
        # build a string of format "2019-10-30-11" "yr-mon-day-strTime"
        cur_app = ("{}-{}-{}-{}".format(self.year, self.month, day, j + 8))

        print(cur_app)

    def valid_time(self, j, i):
        # Why is the first week of january Red? 1st-4th
        button_day = str(self.p[self.week][i]).split("-")[2]
        # if its the weekend
        if(i ==0 or i == 6):
            return False
        if(self.time.tm_year == self.year):
            # if the day already passed
            if(int(button_day) < self.time.tm_mday
            and self.month == self.time.tm_mon):
                return False
            elif(self.month < self.time.tm_mon
                 and self.year == self.time.tm_year):
                return False
            # if the hour has already passed on the current day
            elif(int(button_day) == self.time.tm_mday
                 and (j + 8) <= self.time.tm_hour):
                    return False
            self.employee_scheduled(j, i, button_day)
        return True

    def pop_cal(self):
        pos_x = .15
        pos_y = .65
        list = ["Sunday", "Monday", "Teusday", "Wednesday", "Thursday", "Friday", "Saturday"]

        for day in range(7):
            self.l = Button(text = str("{}\n{}".format(list[day],
                            self.p[self.week][day])),
                            size_hint = (.1, .05),
                            pos_hint = {"x": pos_x, "y":.7})
            self.add_widget(self.l)
            pos_x += .1

        pos_x = .15
        for j in range(8):
            for i in range(7):
                if(self.valid_time(j, i) == False):
                    # invalid time slots so painted red
                    self.button = Button(text = "{}:00".format(str(j + 8)),
                                    font_size = 20, size_hint = (.1, .05),
                                    pos_hint = {"x": pos_x, "y": pos_y})
                    self.button.color = (1, 0, 0, 1)
                    self.add_widget(self.button)
                else:
                    # id should be date
                    self.button = Button(id = ("{}".format(str(self.p[self.week][i]))),
                                    text = "{}:00".format(str(j + 8)), font_size = 20,
                                    size_hint = (.1, .05),
                                    pos_hint = {"x": pos_x, "y": pos_y})
                    self.button.bind(on_release = self.pressed)
                    self.button.color = (0, 1, 0, 1)
                    self.add_widget(self.button)
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
        elif(self.week >=4 and self.month == 12):
            self.week = 1
            self.month = 1
            self.year += 1
            self.p = self.c.monthdatescalendar(self.year, self.month)

        self.pop_cal()

    def prev_week(self):
        if(self.week == 1 and self.month > 1):
            self.week = 4
            self.month = self.month - 1
        elif(self.week > 1):
            self.week =self.week - 1
        elif(self.week ==1 and self.month == 1):
            self.week = 4
            self.month = 12
            self.year = self.year - 1
        self.p = self.c.monthdatescalendar(self.year, self.month)
        self.pop_cal()

    def pressed(self, instance):
        start = instance.text.split(":")[0]
        db.create_appointment(instance.id, int(start),
                              plw.user_info[3], 1, plw.user_info[2], maw.dr_info[0])
        wm.screen_manager.current = "pat_home"