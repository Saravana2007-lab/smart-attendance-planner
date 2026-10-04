import sqlite3

connection = sqlite3.connect("smart_attendance.db")
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

# Remove old sample data
cursor.execute("DELETE FROM attendance")


students = [

    # Harshita
    ("Harshita", 101, "Python", 50, 42),
    ("Harshita", 101, "Operating System", 45, 36),
    ("Harshita", 101, "Computer Network", 40, 31),
    ("Harshita", 101, "DBMS", 48, 34),

    # Spoorthi
    ("Spoorthi", 102, "Python", 50, 44),
    ("Spoorthi", 102, "Operating System", 45, 35),
    ("Spoorthi", 102, "Computer Network", 40, 34),
    ("Spoorthi", 102, "DBMS", 50, 40),

    # Reetesh
    ("Reetesh", 103, "Python", 48, 38),
    ("Reetesh", 103, "Operating System", 50, 39),
    ("Reetesh", 103, "Computer Network", 42, 30),
    ("Reetesh", 103, "DBMS", 45, 32),

    # Ravi
    ("Ravi", 104, "Python", 55, 45),
    ("Ravi", 104, "Operating System", 55, 44),
    ("Ravi", 104, "Computer Network", 45, 36),
    ("Ravi", 104, "DBMS", 60, 48),

    # Preetam
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

print("Database created successfully!")
print("5 students with 4 subjects each added successfully!")

connection.close()
