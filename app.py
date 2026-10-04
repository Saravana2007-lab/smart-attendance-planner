from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import math


# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__, static_folder=".", static_url_path="")


# =========================================================
# DATABASE CONNECTION
# =========================================================
def connect_database():

   return sqlite3.connect("smart_attendance.db")



def initialize_database():

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT NOT NULL,
        roll_no INTEGER NOT NULL,
        subject TEXT NOT NULL,
        total_classes INTEGER NOT NULL,
        attended_classes INTEGER NOT NULL
    )
    """)

    cursor.execute("SELECT COUNT(*) FROM attendance")
    count = cursor.fetchone()[0]

    if count == 0:
        students = [
            ("Harshita", 101, "Python", 50, 42),
            ("Harshita", 101, "Operating System", 45, 36),
            ("Harshita", 101, "Computer Network", 40, 31),
            ("Harshita", 101, "DBMS", 48, 34),
            ("Spoorthi", 102, "Python", 50, 44),
            ("Spoorthi", 102, "Operating System", 45, 35),
            ("Spoorthi", 102, "Computer Network", 40, 34),
            ("Spoorthi", 102, "DBMS", 50, 40),
            ("Reetesh", 103, "Python", 48, 38),
            ("Reetesh", 103, "Operating System", 50, 39),
            ("Reetesh", 103, "Computer Network", 42, 30),
            ("Reetesh", 103, "DBMS", 45, 32),
            ("Ravi", 104, "Python", 55, 45),
            ("Ravi", 104, "Operating System", 55, 44),
            ("Ravi", 104, "Computer Network", 45, 36),
            ("Ravi", 104, "DBMS", 60, 48),
            ("Preetam", 105, "Python", 50, 38),
            ("Preetam", 105, "Operating System", 50, 34),
            ("Preetam", 105, "Computer Network", 40, 27),
            ("Preetam", 105, "DBMS", 55, 41)
        ]
        cursor.executemany("""
        INSERT INTO attendance
        (student_name, roll_no, subject, total_classes, attended_classes)
        VALUES (?, ?, ?, ?, ?)
        """, students)

    connection.commit()
    connection.close()


initialize_database()


# =========================================================
# CALCULATE ATTENDANCE
# =========================================================

def calculate_attendance(total_classes, attended_classes):

    return (
        attended_classes / total_classes
    ) * 100


# =========================================================
# CLASSES REQUIRED FOR 75%
# =========================================================

def classes_required(total_classes, attended_classes):

    attendance = calculate_attendance(
        total_classes,
        attended_classes
    )

    if attendance >= 75:

        return 0

    required = 0.75

    classes = math.ceil(
        (
            required * total_classes
            - attended_classes
        )
        / (1 - required)
    )

    return classes


# =========================================================
# CLASSES THAT CAN BE MISSED
# =========================================================

def classes_can_miss(total_classes, attended_classes):

    attendance = calculate_attendance(
        total_classes,
        attended_classes
    )

    if attendance < 75:

        return 0

    required = 0.75

    classes = math.floor(
        attended_classes / required
        - total_classes
    )

    return classes


# =========================================================
# SUBJECT NORMALIZATION
# =========================================================

def normalize_subject(subject):

    subjects = {

        "python": "Python",

        "operating system": "Operating System",

        "computer network": "Computer Network",

        "dbms": "DBMS",

        "web programming": "Web Programming"

    }

    subject = " ".join(
        subject.strip().split()
    ).lower()

    return subjects.get(subject)


# =========================================================
# HOME PAGE
# =========================================================
@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/style.css")
def style():
    return send_from_directory(".", "style.css")


@app.route("/script.js")
def script():
    return send_from_directory(".", "script.js")
# =========================================================
# ATTENDANCE API
# =========================================================

@app.route("/api/attendance", methods=["POST"])
def attendance_api():

    data = request.get_json()


    # -----------------------------------------------------
    # GET DATA FROM WEBSITE
    # -----------------------------------------------------

    operation = data.get("operation", "").strip().lower()

    student_name = data.get("studentName", "").strip()

    roll_no = data.get("rollNumber", "")

    subject = data.get("subject", "").strip()

    new_classes = data.get("newClasses", "")


    # -----------------------------------------------------
    # BASIC VALIDATION
    # -----------------------------------------------------

    if operation == "":

        return jsonify({
            "success": False,
            "message": "Please select an operation."
        })


    if student_name == "":

        return jsonify({
            "success": False,
            "message": "Name cannot be empty."
        })


    if roll_no == "":

        return jsonify({
            "success": False,
            "message": "Please enter roll number."
        })


    if subject == "":

        return jsonify({
            "success": False,
            "message": "Please enter subject."
        })


    try:

        roll_no = int(roll_no)

    except ValueError:

        return jsonify({
            "success": False,
            "message": "Roll number must contain numbers only."
        })


    if roll_no <= 0:

        return jsonify({
            "success": False,
            "message": "Roll number must be greater than 0."
        })


    # -----------------------------------------------------
    # CLEAN NAME
    # -----------------------------------------------------

    student_name = " ".join(
        student_name.split()
    ).lower().title()


    # -----------------------------------------------------
    # CLEAN SUBJECT
    # -----------------------------------------------------

    subject = normalize_subject(subject)


    if subject is None:

        return jsonify({
            "success": False,
            "message": "Invalid subject."
        })


    # -----------------------------------------------------
    # ATTENDANCE REPORT
    # -----------------------------------------------------

    if operation == "report":

        connection = connect_database()

        cursor = connection.cursor()


        cursor.execute("""
            SELECT
                student_name,
                roll_no,
                subject,
                total_classes,
                attended_classes
            FROM attendance
            ORDER BY roll_no, subject
        """)


        records = cursor.fetchall()

        connection.close()


        report = []


        for record in records:

            name = record[0]

            roll = record[1]

            sub = record[2]

            total = record[3]

            attended = record[4]


            percentage = calculate_attendance(
                total,
                attended
            )


            required = classes_required(
                total,
                attended
            )


            can_miss = classes_can_miss(
                total,
                attended
            )


            report.append({

                "studentName": name,

                "rollNumber": roll,

                "subject": sub,

                "totalClasses": total,

                "attendedClasses": attended,

                "attendance": round(
                    percentage,
                    2
                ),

                "classesRequired": required,

                "classesCanMiss": can_miss

            })


        return jsonify({

            "success": True,

            "operation": "report",

            "report": report

        })


    # -----------------------------------------------------
    # FIND STUDENT RECORD
    # -----------------------------------------------------

    connection = connect_database()

    cursor = connection.cursor()


    cursor.execute("""
        SELECT
            student_name,
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


    # -----------------------------------------------------
    # RECORD NOT FOUND
    # -----------------------------------------------------

    if record is None:

        connection.close()

        return jsonify({

            "success": False,

            "message":
                "No record found. Please check the student name, roll number and subject."

        })


    # -----------------------------------------------------
    # GET EXISTING DATA
    # -----------------------------------------------------

    database_name = record[0]

    database_roll = record[1]

    database_subject = record[2]

    total_classes = record[3]

    attended_classes = record[4]


    # -----------------------------------------------------
    # UPDATE ATTENDANCE
    # -----------------------------------------------------

    if operation == "update":

        try:

            new_classes = int(new_classes)

        except (ValueError, TypeError):

            connection.close()

            return jsonify({

                "success": False,

                "message":
                    "Please enter the number of classes to add."

            })


        if new_classes <= 0:

            connection.close()

            return jsonify({

                "success": False,

                "message":
                    "Number of classes must be greater than 0."

            })


        new_total = total_classes + new_classes

        new_attended = attended_classes + new_classes


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


        percentage = calculate_attendance(
            new_total,
            new_attended
        )


        return jsonify({

            "success": True,

            "operation": "update",

            "studentName": database_name,

            "rollNumber": database_roll,

            "subject": database_subject,

            "totalClasses": new_total,

            "attendedClasses": new_attended,

            "attendance": round(
                percentage,
                2
            ),

            "message":
                "Attendance updated successfully."

        })


    # -----------------------------------------------------
    # CALCULATE CURRENT ATTENDANCE
    # -----------------------------------------------------

    percentage = calculate_attendance(
        total_classes,
        attended_classes
    )


    # -----------------------------------------------------
    # VIEW ATTENDANCE
    # -----------------------------------------------------

    if operation == "view":

        connection.close()

        return jsonify({

            "success": True,

            "operation": "view",

            "studentName": database_name,

            "rollNumber": database_roll,

            "subject": database_subject,

            "totalClasses": total_classes,

            "attendedClasses": attended_classes,

            "attendance": round(
                percentage,
                2
            )

        })


    # -----------------------------------------------------
    # CALCULATE ATTENDANCE
    # -----------------------------------------------------

    if operation == "calculate":

        connection.close()

        return jsonify({

            "success": True,

            "operation": "calculate",

            "studentName": database_name,

            "rollNumber": database_roll,

            "subject": database_subject,

            "totalClasses": total_classes,

            "attendedClasses": attended_classes,

            "attendance": round(
                percentage,
                2
            )

        })


    # -----------------------------------------------------
    # CLASSES REQUIRED
    # -----------------------------------------------------

    if operation == "required":

        required = classes_required(
            total_classes,
            attended_classes
        )


        connection.close()


        return jsonify({

            "success": True,

            "operation": "required",

            "studentName": database_name,

            "rollNumber": database_roll,

            "subject": database_subject,

            "attendance": round(
                percentage,
                2
            ),

            "classesRequired": required

        })


    # -----------------------------------------------------
    # CLASSES CAN BE MISSED
    # -----------------------------------------------------

    if operation == "miss":

        if percentage < 75:

            required = classes_required(
                total_classes,
                attended_classes
            )


            connection.close()


            return jsonify({

                "success": True,

                "operation": "miss",

                "studentName": database_name,

                "rollNumber": database_roll,

                "subject": database_subject,

                "attendance": round(
                    percentage,
                    2
                ),

                "classesCanMiss": 0,

                "below75": True,

                "classesRequired": required

            })


        can_miss = classes_can_miss(
            total_classes,
            attended_classes
        )


        connection.close()


        return jsonify({

            "success": True,

            "operation": "miss",

            "studentName": database_name,

            "rollNumber": database_roll,

            "subject": database_subject,

            "attendance": round(
                percentage,
                2
            ),

            "classesCanMiss": can_miss,

            "below75": False

        })


    # -----------------------------------------------------
    # INVALID OPERATION
    # -----------------------------------------------------

    connection.close()


    return jsonify({

        "success": False,

        "message": "Invalid operation."

    })


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    app.run(
    debug=False,
    use_reloader=False
)
