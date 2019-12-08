import sqlite3
import hashlib, binascii, os

con = sqlite3.connect("AppointmentTracker.db")
c = con.cursor()


# Commits changes to the database
def commit():
    con.commit()


# Closes the database
def close():
    con.close()

def is_valid(email, usr_type):
    valid_bit = None
    if usr_type == "Patient":
        valid_bit = """SELECT pat_valid
                        FROM Patient
                        WHERE pat_email LIKE "{}" """.format(email)

    elif usr_type == "Employee":
        valid_bit = """SELECT emp_valid
                                FROM Employee
                                WHERE emp_email LIKE "{}" """.format(email)
    c.execute(valid_bit)
    output = c.fetchone()
    return output[0] == "true"


def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

# Returns a boolean true or false if any users login info is valid
# @Param email, password, type of user
def is_user(email, password, usr_type):
    print("{} {} {}".format(email, password, usr_type))
    if email == "Admin":
        if password == "Admin":
            return True

    elif usr_type == "Patient":
        valid_query = """SELECT pat_password
                              FROM Patient
                              WHERE pat_email LIKE "{}" """.format(email)
        c.execute(valid_query)
        output = c.fetchone()
        if output is not None:
            return verify_password(output[0], password) and is_valid(email, usr_type)

    elif usr_type == "Employee":
        valid_query = """SELECT emp_password
                              FROM Employee
                              WHERE emp_email LIKE "{}" """.format(email)
        c.execute(valid_query)
        output = c.fetchone()
        if output is not None:
            return verify_password(output[0], password) and is_valid(email, usr_type)
            # if output[0] == password:
            #     return True

    return False


# Returns a patients ID given their email as the only parameter
def get_pat_id(email):
    id_query = """SELECT pat_id FROM Patient WHERE pat_email LIKE "{}" """.format(email)
    c.execute(id_query)
    id_num = c.fetchone()

    # Checks if the id value is None
    if id_num is None:
        print("No id found")
        return None

    return id_num[0]


# Returns an employees ID given their email as the only parameter
def get_emp_id(email):
    id_query = """SELECT emp_id FROM Employee WHERE emp_email LIKE "{}" """.format(email)
    c.execute(id_query)
    id_num = c.fetchone()

    # Checks if the id value is None
    if id_num is None:
        print("No id found")
        return None

    return id_num[0]


# Returns a patients email, given their ID
def get_pat_email(id_num):
    email_query = """SELECT pat_email FROM Patient WHERE pat_id LIKE "{}" """.format(id_num)
    c.execute(email_query)
    email = c.fetchone()

    # Checks if the id value is None
    if email is None:
        print("No id found")
        return None

    return email[0]


# Returns an employees email, given their ID
def get_emp_email(id_num):
    email_query = """SELECT emp_email FROM Employee WHERE emp_id LIKE "{}" """.format(id_num)
    c.execute(email_query)
    email = c.fetchone()

    # Checks if the id value is None
    if email is None:
        print("No id found")
        return None

    return email[0]

def get_hygen(temp, query, appointment):
    for row in query:
        # print(tow)
        temp1 = "{} {}".format(row[0], row[1])
        if(temp == temp1):
            print("MAtch")
            appointment.append(row[4])
            appointment.append(row[5])

# Returns a list of output strings showing every appointment a user has in the database
def view_user_schedule(user_id, user_type):
    ls = []
    if user_type == "Patient":
        info_query = """SELECT date, start_time, end_time, description, emp_fn, emp_ln
                            FROM Requests NATURAL JOIN Appointment NATURAL JOIN Works NATURAL JOIN Employee
                            WHERE pat_id == {} AND emp_type LIKE "%Doctor%" """.format(user_id)

        hygenist_query = """SELECT date, start_time, end_time, description, emp_fn, emp_ln
                            FROM Requests NATURAL JOIN Appointment NATURAL JOIN Works NATURAL JOIN Employee
                            WHERE pat_id == {} AND emp_type LIKE "%Hygenist%" """.format(user_id)

        # hygenist_query = """SELECT emp_fn, emp_ln
        #                      FROM Requests NATURAL JOIN Appointment NATURAL JOIN Works NATURAL JOIN Employee
        #                      WHERE pat_id == {} AND emp_type LIKE "%Hygenist%" """.format(user_id)

        appointment = []
        for row in c.execute(info_query):
            temp = "{} {}".format(row[0], row[1])
            appointment.append(row[0])
            appointment.append(row[1])
            appointment.append(row[2])
            appointment.append(row[3])
            appointment.append(row[4])
            appointment.append(row[5])
            appointment.append("No")
            appointment.append("Hygenist")
            ls.append(appointment)
            appointment = []
        for row in c.execute(hygenist_query):
            temp1 = "{} {}".format(row[0], row[1])
            for item in ls:
                temp = "{} {}".format(item[0], item[1])
                if(temp == temp1):
                    item[6] = row[4]
                    item[7] = row[5]

    elif user_type == "Employee":
        info_query = """SELECT date, start_time, end_time, description, pat_fn, pat_ln
                                FROM Patient NATURAL JOIN Requests NATURAL JOIN Appointment NATURAL JOIN Works
                                WHERE emp_id == {} """.format(user_id)

        # for row in c.execute(info_query):
        #     s = "{}: Start: {}  Finish: {}  Description: {} for {} {}".format(row[0], row[1], row[2], row[3], row[4],
        #                                                                       row[5])
        #     ls.append(s)

        appoinment = []
        for row in c.execute(info_query):
            # s = "{}: Start: {}  Finish: {}  Description: {} with Dr. {} {}".format(row[0], row[1], row[2], row[3],
            #                                                                        row[4], row[5])
            appoinment.append(row[0])
            appoinment.append(row[1])
            appoinment.append(row[2])
            appoinment.append(row[3])
            appoinment.append(row[4])
            appoinment.append(row[5])
            ls.append(appoinment)
            appoinment = []

    return ls


# Returns a list strings, showing all employees in the database
def list_employees():
    ls = []

    emp_query = """SELECT emp_type, emp_fn, emp_ln, emp_email FROM EMPLOYEE"""

    emp = []
    for row in c.execute(emp_query):
        emp.append(row[0])
        emp.append(row[1])
        emp.append(row[2])
        emp.append(row[3])
        ls.append(emp)
        emp = []
        # s = "{}: {} {} {}".format(row[0], row[1], row[2], row[3])
        # ls.append(s)

    return ls


# Creates a user and adds them to a database, takes in personal info as parameters along with an
# employee type to use if the user being created is an employee
def create_user(fn, ln, email, password, phone, emp_type, usr_type):
    print("{} {} {} {} {} {}".format(fn, ln, email, password, phone, usr_type, emp_type))

    insert = ""
    if usr_type == "Employee":
        insert = """INSERT INTO Employee (emp_fn, emp_ln, emp_password, emp_email, emp_phone, emp_type, emp_valid)
                        VALUES("{}", "{}", "{}", "{}", "{}", "{}", "{}")""".format(fn, ln, password, email, phone, emp_type, 1)

    elif usr_type == "Patient":
        insert = """INSERT INTO Patient (pat_fn, pat_ln, pat_password, pat_email, pat_phone, pat_valid)
                            VALUES ("{}", "{}", "{}", "{}", "{}", "{}")""".format(fn, ln, password, email, phone, 1)

    c.execute(insert)
    commit()


# Adds appointment info to the appointment table and relationship tables to relate patients, employees and appointments
def create_appointment(date, start, description, duration, pat_email, dr_email, hyg_email):
    # create appointment, need to figure out how to do math on times
    print(date)
    print(start)
    print(description)
    print(duration)
    print(pat_email)
    print(hyg_email)
    print(dr_email)

    end = start + duration
    print("Date: {}   Start: {} End: {}\n Description: {}\n".format(date, start, end, description))
    appt_query = """INSERT INTO Appointment(start_time, end_time, date, description, duration)
                            VALUES ("{}", "{}", "{}", "{}", {})""".format(start, end, date, description, duration)
    c.execute(appt_query)

    pat_id = get_pat_id(pat_email)
    dr_id = get_emp_id(dr_email)
    hyg_id = get_emp_id(hyg_email)
    appt_id = c.lastrowid

    # create request relationship with most recent appointments id
    print(pat_id)
    print("dr {}".format(dr_id))
    print("hygenist {}".format(hyg_id))
    create_request(pat_id, appt_id)

    # create works relationship
    create_work(hyg_id, appt_id)
    create_work(dr_id, appt_id)
    commit()


# Called by the create_appointment method to add to the relationship table relating patients and appointments
def create_request(user_id, appt_id):
    print("{} {}".format(user_id, appt_id))
    req_query = """INSERT INTO Requests(pat_id, appt_id) VALUES ({}, {})""".format(user_id, appt_id)
    c.execute(req_query)


# Called by the create_appointment method to add to the relationship table to relate doctors and appointments
def create_work(user_id, appt_id):
    print("{} {} ", user_id, appt_id)
    work_query = """INSERT INTO Works(appt_id, emp_id) VALUES ({}, {})""".format(appt_id, user_id)
    c.execute(work_query)


def get_appt_id(row, user_id, user_type):
    if user_type == "Patient":
        appt_id_q = """SELECT appt_id
                        FROM Patient NATURAL JOIN Requests NATURAL JOIN Appointment NATURAL JOIN Works NATURAL JOIN Employee
                        WHERE pat_id = {}
                        LIMIT 1 OFFSET {}""".format(user_id, row)
        c.execute(appt_id_q)
        if appt_id_q is None:
            print("No id found")
            return None

            return appt_id_q[0]

    elif user_type == "Employee":
        appt_id_q = """SELECT appt_id
                         FROM Patient NATURAL JOIN Requests NATURAL JOIN Appointment NATURAL JOIN Works NATURAL JOIN Employee
                         WHERE emp_id = {}
                         LIMIT 1 OFFSET {}""".format(user_id, row)
        c.execute(appt_id_q)
        if appt_id_q is None:
            print("No id found")
            return None

        return appt_id_q[0]


# Deletes an appointment given what row it is in the database (zero indexed)
def delete_appt(row, user_id, user_type):
    appt_id = get_appt_id(row, user_id, user_type)
    set_notification(appt_id)

    del_request = """DELETE FROM Requests
                        WHERE appt_id = {}""".format(appt_id)

    del_works = """DELETE FROM Works
                            WHERE appt_id = {}""".format(appt_id)

    del_appt = """DELETE FROM Appointment
                            WHERE appt_id = {}""".format(appt_id)

    c.execute(del_request)
    c.execute(del_works)
    c.execute(del_appt)

    commit()


def delete_user(usr_type, usr_id):
    update_stmt = ""
    if usr_type == "Employee":
        update_stmt = """UPDATE Employee
                        SET emp_valid = 1
                        WHERE emp_id = {}""".format(usr_id)

    elif usr_type == "Patient":
        update_stmt = """UPDATE Patient
                            SET pat_valid = 1
                            WHERE pat_id = {}""".format(usr_id)

    c.execute(update_stmt)
    commit()


def set_notification(appt_id):
    pat_update = """UPDATE Patient
                        SET pat_notification = {}
                        WHERE pat_id = (SELECT pat_id
                            FROM Patient NATURAL JOIN Requests NATURAL JOIN Appointment NATURAL JOIN Appointment
                            WHERE appt_id = {})""".format(1, appt_id)

    dr_update = """UPDATE Employee
                            SET emp_notification = {}
                            WHERE emp_id = (SELECT emp_id
                                FROM Employee NATURAL JOIN Works NATURAL JOIN Appointment NATURAL JOIN Appointment
                                WHERE appt_id = {} AND emp_type = "Doctor")""".format(1, appt_id)

    hyg_update = """UPDATE Employee
                            SET emp_notification = {}
                            WHERE emp_id = (SELECT emp_id
                                FROM Employee NATURAL JOIN Works NATURAL JOIN Appointment NATURAL JOIN Appointment
                                WHERE appt_id = {} AND emp_type = "Hygenist")""".format(1, appt_id)

    c.execute(dr_update)
    c.execute(pat_update)
    c.execute(hyg_update)
    commit()


def has_notification(usr_type, usr_id):
    notification_q = ""
    if usr_type == "Employee":
        notification_q = """SELECT emp_notification
                                FROM Employee
                                WHERE emp_id = {}""".format(usr_id)

    elif usr_type == "Patient":
        notification_q = """SELECT pat_notification
                                FROM Patient
                                WHERE pat_id = {}""".format(usr_id)

    c.execute(notification_q)
    output = c.fetchone()
    if output[0] == 1:
        remove_notification(usr_type, usr_id)
        return 1
    else:
        return 0


def remove_notification(usr_type, usr_id):
    remove_q = ""
    if usr_type == "Employee":
        remove_q = """UPDATE Employee
                        SET emp_notification = 0
                        WHERE emp_id = {}""".format(usr_id)

    elif usr_type == "Patient":
        remove_q = """UPDATE Patient
                        SET pat_notification = 0
                        WHERE pat_id = {}""".format(usr_id)

    c.execute(remove_q)
    commit()
