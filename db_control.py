import sqlite3

con = sqlite3.connect("AppointmentTracker.db")
c = con.cursor()


# Commits changes to the database
def commit():
    con.commit()


# Closes the database
def close():
    con.close()


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
                              WHERE pat_email LIKE "%{}%" """ .format(email)
        c.execute(valid_query)
        output = c.fetchone()
        if output is not None:
            if output[0] == password:
                return True

    elif usr_type == "Employee":
        valid_query = """SELECT emp_password
                              FROM Employee
                              WHERE emp_email LIKE "%{}%" """.format(email)
        c.execute(valid_query)
        output = c.fetchone()
        if output is not None:
            if output[0] == password:
                return True

    return False


# Returns a patients ID given their email as the only parameter
def get_pat_id(email):
    print(email)
    id_query = """SELECT pat_id FROM Patient WHERE pat_email LIKE "%{}%" """.format(email)
    c.execute(id_query)
    id_num = c.fetchone()

    # Checks if the id value is None
    if id_num is None:
        print("No id found")
        return None

    return id_num[0]


# Returns an employees ID given their email as the only parameter
def get_emp_id(email):
    print(email)
    id_query = """SELECT emp_id FROM Employee WHERE emp_email LIKE "%{}%" """.format(email)
    c.execute(id_query)
    id_num = c.fetchone()

    # Checks if the id value is None
    if id_num is None:
        print("No id found")
        return None

    return id_num[0]


# Returns a patients email, given their ID
def get_pat_email(id_num):
    print(id_num)
    email_query = """SELECT pat_email FROM Patient WHERE pat_id LIKE "%{}%" """.format(id_num)
    c.execute(email_query)
    email = c.fetchone()

    # Checks if the id value is None
    if email is None:
        print("No id found")
        return None

    return email[0]


# Returns an employees email, given their ID
def get_emp_email(id_num):
    print(id_num)
    email_query = """SELECT emp_email FROM Employee WHERE emp_id LIKE "%{}%" """.format(id_num)
    c.execute(email_query)
    email = c.fetchone()

    # Checks if the id value is None
    if email is None:
        print("No id found")
        return None

    return email[0]


# Returns a list of output strings showing every appointment a user has in the database
def view_user_schedule(user_id, user_type):
    ls = []
    if user_type == "Patient":
        info_query = """SELECT date, start_time, end_time, description, emp_fn, emp_ln
                        FROM Requests NATURAL JOIN Appointment NATURAL JOIN Works NATURAL JOIN Employee
                        WHERE pat_id == {} """.format(user_id)
        appoinment = []
        for row in c.execute(info_query):
            appoinment.append(row[0])
            appoinment.append(row[1])
            appoinment.append(row[2])
            appoinment.append(row[3])
            appoinment.append(row[4])
            appoinment.append(row[5])
            ls.append(appoinment)
            for app in appoinment:
                print(app)
            appoinment = []
            # ls.append(s)

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
        insert = """INSERT INTO Employee (emp_fn, emp_ln, emp_password, emp_email, emp_phone, emp_type)
                        VALUES("{}", "{}", "{}", "{}", "{}", "{}")""".format(fn, ln, password, email, phone, emp_type)

    elif usr_type == "Patient":
        insert = """INSERT INTO Patient (pat_fn, pat_ln, pat_password, pat_email, pat_phone)
                            VALUES ("{}", "{}", "{}", "{}", "{}")""".format(fn, ln, password, email, phone)

    c.execute(insert)
    commit()


# Adds appointment info to the appointment table and relationship tables to relate patients, employees and appointments
def create_appointment(date, start, description, duration, pat_email, emp_email):
    # create appointment, need to figure out how to do math on times
    print(date)
    print(start)
    print(description)
    print(duration)
    print(pat_email)
    print(emp_email)

    end = start + duration
    print("Date: {}   Start: {} End: {}\n Description: {}\n".format(date, start, end, description))
    appt_query = """INSERT INTO Appointment(start_time, end_time, date, description, duration)
                            VALUES ("{}", "{}", "{}", "{}", {})""".format(start, end, date, description, duration)
    c.execute(appt_query)

    pat_id = get_pat_id(pat_email)
    emp_id = get_emp_id(emp_email)
    appt_id = c.lastrowid

    # create request relationship with most recent appointments id
    print(pat_id)
    print("dr {}".format(emp_id))
    create_request(pat_id, appt_id)

    # create works relationship
    create_work(emp_id, appt_id)
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
