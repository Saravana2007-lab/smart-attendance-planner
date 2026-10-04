import sqlite3
import math


# =========================================================
# DATABASE CONNECTION
# =========================================================

def connect_database():
    return sqlite3.connect("smart_attendance.db")


# =========================================================
# NAME VALIDATION AND NORMALIZATION
# =========================================================

def validate_name():

    while True:

        student_name = input("Enter Student Name: ")

        # Remove extra spaces from beginning/end
        student_name = student_name.strip()

        if student_name == "":
            print("Name cannot be empty.")

        elif len(student_name) < 2:
            print("Name must have at least 2 characters.")

        elif student_name.replace(" ", "").isalpha() == False:
            print("Name can only contain letters and spaces.")

        else:
            # Remove extra spaces between words
            student_name = " ".join(student_name.split())

            # Make name case-insensitive
            # harshita -> Harshita
            # HARSHITA -> Harshita
            # hArShItA -> Harshita
            # harshita   gupta -> Harshita Gupta
            student_name = student_name.lower().title()

            return student_name


# =========================================================
# ROLL NUMBER
# =========================================================

def validate_roll_number():

    while True:

        try:

            roll_no = int(input("Enter Roll Number: "))

            if roll_no <= 0:
                print("Roll number must be greater than 0.")

            else:
                return roll_no

        except ValueError:

            print("Roll number must contain numbers only.")


# =========================================================
# SUBJECT
# =========================================================

def get_subject():

    subjects = {
        "python": "Python",
        "operating system": "Operating System",
        "computer network": "Computer Network",
        "dbms": "DBMS",
        "web programming": "Web Programming"
    }


    while True:

        subject = input("Enter Subject: ")

        # Remove extra spaces and convert to lowercase
        subject = " ".join(subject.strip().split()).lower()


        if subject in subjects:

            return subjects[subject]

        else:

            print("\nInvalid subject.")
            print("Available subjects:")
            print("1. Python")
            print("2. Operating System")
            print("3. Computer Network")
            print("4. DBMS")
            print("5. Web Programming")


# =========================================================
# GET STUDENT + SUBJECT
# =========================================================

def get_student_record():

    student_name = validate_name()

    roll_no = validate_roll_number()

    subject = get_subject()


    connection = connect_database()
    cursor = connection.cursor()


    cursor.execute("""
        SELECT student_name,
               roll_no,
               subject,
               total_classes,
               attended_classes
        FROM attendance
        WHERE LOWER(student_name) = LOWER(?)
        AND roll_no = ?
        AND LOWER(subject) = LOWER(?)
    """, (
        student_name,
        roll_no,
        subject
    ))


    record = cursor.fetchone()

    connection.close()


    if record is None:

        print("\n----------------------------------------")
        print("No record found.")
        print("----------------------------------------")
        print("Please check the student name,")
        print("roll number and subject.")

        return None


    return record


# =========================================================
# OPTION 1
# ADD ATTENDANCE
# =========================================================

def add_student_attendance():

    print("\n==========================================")
    print("          ADD ATTENDANCE")
    print("==========================================")


    student_name = validate_name()

    roll_no = validate_roll_number()

    subject = get_subject()


    # Check whether student/subject already exists
    connection = connect_database()
    cursor = connection.cursor()


    cursor.execute("""
        SELECT total_classes,
               attended_classes
        FROM attendance
        WHERE LOWER(student_name) = LOWER(?)
        AND roll_no = ?
        AND LOWER(subject) = LOWER(?)
    """, (
        student_name,
        roll_no,
        subject
    ))


    record = cursor.fetchone()


    if record is None:

        connection.close()

        print("\nNo record found for this student and subject.")
        print("Please check the details and try again.")

        return


    old_total = record[0]
    old_attended = record[1]


    # Ask only how many new classes were attended
    while True:

        try:

            new_attendance = int(
                input("How many classes do you want to add? ")
            )


            if new_attendance <= 0:

                print(
                    "Number of classes must be greater than 0."
                )

            else:

                break

        except ValueError:

            print("Please enter a number.")


    # Update both total and attended classes
    new_total = old_total + new_attendance

    new_attended = old_attended + new_attendance


    cursor.execute("""
        UPDATE attendance
        SET total_classes = ?,
            attended_classes = ?
        WHERE LOWER(student_name) = LOWER(?)
        AND roll_no = ?
        AND LOWER(subject) = LOWER(?)
    """, (
        new_total,
        new_attended,
        student_name,
        roll_no,
        subject
    ))


    connection.commit()
    connection.close()


    attendance = calculate_attendance(
        new_total,
        new_attended
    )


    print("\n==========================================")
    print("       ATTENDANCE UPDATED SUCCESSFULLY")
    print("==========================================")

    print("Student Name       :", student_name)
    print("Roll Number        :", roll_no)
    print("Subject            :", subject)

    print("\nPrevious Total     :", old_total)
    print("Classes Added      :", new_attendance)
    print("New Total          :", new_total)

    print("\nPrevious Attended  :", old_attended)
    print("New Attended       :", new_attended)

    print(
        "\nCurrent Attendance :",
        round(attendance, 2),
        "%"
    )

    print("==========================================")


# =========================================================
# OPTION 2
# VIEW STUDENT ATTENDANCE
# =========================================================

def view_student_attendance():

    print("\n==========================================")
    print("        VIEW STUDENT ATTENDANCE")
    print("==========================================")


    record = get_student_record()


    if record is None:
        return


    student_name = record[0]
    roll_no = record[1]
    subject = record[2]
    total_classes = record[3]
    attended_classes = record[4]


    attendance = calculate_attendance(
        total_classes,
        attended_classes
    )


    print("\n==========================================")
    print("        STUDENT ATTENDANCE")
    print("==========================================")

    print("Student Name       :", student_name)
    print("Roll Number        :", roll_no)
    print("Subject            :", subject)

    print("Total Classes      :", total_classes)
    print("Attended Classes   :", attended_classes)

    print(
        "Attendance         :",
        round(attendance, 2),
        "%"
    )

    print("==========================================")


# =========================================================
# CALCULATE ATTENDANCE
# =========================================================

def calculate_attendance(total_classes, attended_classes):

    attendance = (
        attended_classes / total_classes
    ) * 100

    return attendance


# =========================================================
# OPTION 3
# CALCULATE ATTENDANCE FROM DATABASE
# =========================================================

def calculate_student_attendance():

    print("\n==========================================")
    print("          CALCULATE ATTENDANCE")
    print("==========================================")


    record = get_student_record()


    if record is None:
        return


    total_classes = record[3]
    attended_classes = record[4]


    attendance = calculate_attendance(
        total_classes,
        attended_classes
    )


    print("\n==========================================")
    print("        ATTENDANCE CALCULATION")
    print("==========================================")

    print("Student Name     :", record[0])
    print("Roll Number      :", record[1])
    print("Subject          :", record[2])

    print("Total Classes    :", total_classes)
    print("Attended Classes :", attended_classes)

    print(
        "Attendance       :",
        round(attendance, 2),
        "%"
    )

    print("==========================================")


# =========================================================
# CALCULATE CLASSES REQUIRED
# =========================================================

def classes_required(total_classes, attended_classes):

    required = 0.75

    attendance = calculate_attendance(
        total_classes,
        attended_classes
    )


    if attendance >= 75:

        return 0


    classes = math.ceil(
        (
            required * total_classes
            - attended_classes
        )
        / (1 - required)
    )


    return classes


# =========================================================
# OPTION 4
# CLASSES REQUIRED FOR 75%
# =========================================================

def calculate_classes_required():

    print("\n==========================================")
    print("       CLASSES REQUIRED FOR 75%")
    print("==========================================")


    record = get_student_record()


    if record is None:
        return


    total_classes = record[3]
    attended_classes = record[4]


    attendance = calculate_attendance(
        total_classes,
        attended_classes
    )


    required = classes_required(
        total_classes,
        attended_classes
    )


    print("\n==========================================")
    print("        75% ATTENDANCE PLANNER")
    print("==========================================")

    print("Student Name       :", record[0])
    print("Roll Number        :", record[1])
    print("Subject            :", record[2])

    print(
        "Current Attendance :",
        round(attendance, 2),
        "%"
    )


    if required == 0:

        print(
            "\nYou already have 75% or more attendance."
        )

    else:

        print(
            "\nClasses you need to attend:",
            required
        )

        print("to reach 75% attendance.")


    print("==========================================")


# =========================================================
# CALCULATE CLASSES THAT CAN BE MISSED
# =========================================================

def classes_can_miss(total_classes, attended_classes):

    required = 0.75

    attendance = calculate_attendance(
        total_classes,
        attended_classes
    )


    if attendance < 75:

        return 0


    classes = math.floor(
        attended_classes / required
        - total_classes
    )


    return classes


# =========================================================
# OPTION 5
# CLASSES YOU CAN MISS
# =========================================================

def calculate_classes_can_miss():

    print("\n==========================================")
    print("         CLASSES YOU CAN MISS")
    print("==========================================")


    record = get_student_record()


    if record is None:
        return


    total_classes = record[3]
    attended_classes = record[4]


    attendance = calculate_attendance(
        total_classes,
        attended_classes
    )


    print("\n==========================================")
    print("          ATTENDANCE PLANNER")
    print("==========================================")

    print("Student Name       :", record[0])
    print("Roll Number        :", record[1])
    print("Subject            :", record[2])

    print(
        "Current Attendance :",
        round(attendance, 2),
        "%"
    )


    if attendance < 75:

        required = classes_required(
            total_classes,
            attended_classes
        )


        print("\nYour attendance is below 75%.")

        print(
            "You need to attend",
            required,
            "more classes to reach 75%."
        )


    else:

        can_miss = classes_can_miss(
            total_classes,
            attended_classes
        )


        print(
            "\nYou can miss",
            can_miss,
            "classes and still maintain 75%."
        )


    print("==========================================")


# =========================================================
# OPTION 6
# ATTENDANCE REPORT
# =========================================================

def attendance_report():

    connection = connect_database()
    cursor = connection.cursor()


    cursor.execute("""
        SELECT student_name,
               roll_no,
               subject,
               total_classes,
               attended_classes
        FROM attendance
        ORDER BY roll_no, subject
    """)


    records = cursor.fetchall()

    connection.close()


    if len(records) == 0:

        print("\nNo attendance records found.")

        return


    print("\n")
    print("==============================================================")
    print("                  ATTENDANCE REPORT")
    print("==============================================================")


    current_roll = None


    for record in records:

        student_name = record[0]
        roll_no = record[1]
        subject = record[2]
        total_classes = record[3]
        attended_classes = record[4]


        attendance = calculate_attendance(
            total_classes,
            attended_classes
        )


        required = classes_required(
            total_classes,
            attended_classes
        )


        can_miss = classes_can_miss(
            total_classes,
            attended_classes
        )


        if current_roll != roll_no:

            print("\n")
            print("--------------------------------------------------------------")
            print("Student :", student_name)
            print("Roll No. :", roll_no)
            print("--------------------------------------------------------------")

            current_roll = roll_no


        print("\nSubject          :", subject)
        print("Total Classes    :", total_classes)
        print("Attended Classes :", attended_classes)

        print(
            "Attendance       :",
            round(attendance, 2),
            "%"
        )


        if attendance >= 75:

            print("Status            : SAFE")

            print(
                "Classes Can Miss  :",
                can_miss
            )

        else:

            print("Status            : BELOW 75%")

            print(
                "Classes Required  :",
                required
            )


        print("--------------------------------------------------------------")


# =========================================================
# MAIN MENU
# =========================================================

while True:

    print("\n")
    print("==========================================")
    print("       SMART ATTENDANCE PLANNER")
    print("==========================================")

    print("1. Add Student Attendance")
    print("2. View Student Attendance")
    print("3. Calculate Attendance")
    print("4. Classes Required for 75%")
    print("5. Classes You Can Miss")
    print("6. Attendance Report")
    print("7. Exit")

    print("==========================================")


    choice = input("Enter your choice: ")


    # -----------------------------------------------------
    # OPTION 1
    # -----------------------------------------------------

    if choice == "1":

        add_student_attendance()


    # -----------------------------------------------------
    # OPTION 2
    # -----------------------------------------------------

    elif choice == "2":

        view_student_attendance()


    # -----------------------------------------------------
    # OPTION 3
    # -----------------------------------------------------

    elif choice == "3":

        calculate_student_attendance()


    # -----------------------------------------------------
    # OPTION 4
    # -----------------------------------------------------

    elif choice == "4":

        calculate_classes_required()


    # -----------------------------------------------------
    # OPTION 5
    # -----------------------------------------------------

    elif choice == "5":

        calculate_classes_can_miss()


    # -----------------------------------------------------
    # OPTION 6
    # -----------------------------------------------------

    elif choice == "6":

        attendance_report()


    # -----------------------------------------------------
    # OPTION 7
    # -----------------------------------------------------

    elif choice == "7":

        print("\nThank you for using Smart Attendance Planner!")

        break


    # -----------------------------------------------------
    # INVALID CHOICE
    # -----------------------------------------------------

    else:

        print("\nInvalid choice. Please enter 1 to 7.")        



