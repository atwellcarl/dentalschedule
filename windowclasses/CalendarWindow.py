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
from windowclasses import PatientLoginWindow as plw
from windowclasses import MakeAppointmentWindow as maw
import db_control as db
import time
import calendar

window = "pat_home"
# Class is used for scheduling appointments. This will display one
# week at a time (x-axis is days of the week, y-axis is time of day)
class CalendarWindow(Screen):
    kv = Builder.load_file("stylefolders/cw.kv")

    time = time.localtime(time.time())
    year = time.tm_year
    month = time.tm_mon
    week_math = calendar.monthrange(year, month)


    #logic to decide which week of the month the current day is in.
    week = 0
    temp = time.tm_mday/7
    if(temp <= 1):
        week = 0
    elif(temp <= 2):
        week = 1
    elif(temp <= 3):
        week = 2
    elif(temp <= 4):
        week = 3
    else:
        week = 4

    # Python calendar objects
    c = calendar.TextCalendar(calendar.SUNDAY)
    p = c.monthdatescalendar(year, month)

    # Takes a day, hour,day of week, email
    # and determins if the employee already has
    # an appointment
    def employee_scheduled(self, j, i, day, emp):
        dr_id = db.get_emp_id(emp)
        list = db.view_user_schedule(dr_id, "Employee")
        # build a string of format "2019-10-30-11" "yr-mon-day-strTime"
        cur_app = ("{}-{}-{}-{}".format(self.year, self.month, day, j + 8))
        # if the employee is busy
        for app in list:
            dr_schedule = ("{}-{}".format(app[0], app[1]))
            if(dr_schedule == cur_app):
                return False
        return True
    # Takes a day, hour,day of week, email
    # and determins if the patient already has
    # an appointment
    def patient_scheduled(self, j, i, day):
        # dr_id = db.get_pat_id(pwl.user_info[0])
        list = db.view_user_schedule(plw.user_info[0], "Patient")
        # build a string of format "2019-10-30-11" "yr-mon-day-startTime"
        cur_app = ("{}-{}-{}-{}".format(self.year, self.month, day, j + 8))
        i = 0
        for app in list:
            pat_schedule = ("{}-{}".format(app[0], app[1]))
            i += 1
            if(pat_schedule == cur_app):
                return False
        return True

    # Takes day and time arguments from the calendar set up
    # and checks for possible conflicts
    def valid_time(self, j, i):
        button_day = str(self.p[self.week][i]).split("-")[2]
        temp = True
        # if its the weekend
        if(i ==0 or i == 6):
            temp = False
        if(self.time.tm_year == self.year):
            # if the day already passed
            if(int(button_day) < self.time.tm_mday
            and self.month == self.time.tm_mon):
                temp = False
            elif(self.month < self.time.tm_mon
                 and self.year == self.time.tm_year):
                temp = False
            # if the hour has already passed on the current day
            elif(int(button_day) == self.time.tm_mday
                 and (j + 8) <= self.time.tm_hour):
                temp = False
            # check if the selected dr is busy this hour
            elif(self.employee_scheduled(j, i, button_day, maw.dr_info[0]) == False):
                temp = False
            # check if the selected hygenist is busy this hour
            elif(self.employee_scheduled(j, i, button_day, maw.dr_info[1]) == False):
                temp = False
            # check if the patient already has an appointment this hour
            elif(self.patient_scheduled(j, i, button_day) == False):
                temp = False
        return temp

    # Populates the window with the valid calendar for the week
    def pop_cal(self):
        pos_x = .15
        pos_y = .65
        list = ["Sunday", "Monday", "Teusday", "Wednesday", "Thursday", "Friday", "Saturday"]

        # populate day of the week buttons
        for day in range(7):
            self.l = Button(text = str("{}\n{}".format(list[day],
                            self.p[self.week][day])),
                            size_hint = (.1, .05),
                            pos_hint = {"x": pos_x, "y":.7})
            self.add_widget(self.l)
            pos_x += .1

        # populate hour buttons by appropriately marking available and
        # unavailable times (decide between green and red)
        pos_x = .15
        for j in range(10):
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

    #logic for what the next week should look like
    def next_week(self):
        # if month doesnt change
        if(self.week < 4):
            self.week += 1
        # if the month should change but not the year
        elif(self.week >= 4 and self.month < 12):
            self.week = 0
            self.month += 1
        # if the month and year should change
        elif(self.week >=4 and self.month == 12):
            self.week = 0
            self.month = 1
            self.year += 1

        self.p = self.c.monthdatescalendar(self.year, self.month)
        self.pop_cal()

    # logic for what the previous week should look like
    def prev_week(self):
        # if the month should change but not the year
        if(self.week == 1 and self.month > 1):
            self.week = 4
            self.month = self.month - 1

        # if month doesnt change
        elif(self.week > 1):
            self.week =self.week - 1

        # if the month and year should change
        elif(self.week ==1 and self.month == 1):
            self.week = 4
            self.month = 12
            self.year = self.year - 1
        self.p = self.c.monthdatescalendar(self.year, self.month)
        self.pop_cal()

    # Pop up to inform the user that they have made an appointment
    def sucessful_app(self, instance):
        popup = Popup(title = "Appointment Made!",
                  content = Label(text = "Your appointment has been successfully scheduled."),
                  size_hint = (None, None), size = (400, 400))
        popup.open()

    # schedules the appointment
    def pressed(self, instance):
        start = instance.text.split(":")[0]
        db.create_appointment(instance.id, int(start),
                              plw.user_info[3], 1, plw.user_info[2], maw.dr_info[0], maw.dr_info[1])
        # print("creating an app with {} and {}".format(maw.dr_info[0], maw.dr_info[1]))
        wm.screen_manager.current = window
        self.sucessful_app(instance)
