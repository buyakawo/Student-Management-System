import sqlite3
import random
from datetime import date, datetime, timedelta
import os
from fpdf import FPDF


#1.a
def create_connection():
    # ensure the database directory exists
    db_dir = 'db'
    db_path = os.path.join(db_dir, 'database.sqlite')
    
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    # Connect to the SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    return conn

#1.b
def create_tables(conn):
    # create tables for database schema
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            year_of_enrollment INTEGER NOT NULL,
            major TEXT NOT NULL,
            gender TEXT NOT NULL,
            accommodation_id INTEGER NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Courses (
            course_id INTEGER PRIMARY KEY,
            course_name TEXT NOT NULL,
            credits INTEGER NOT NULL,
            test_score INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Course_Schedules (
            schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            term INTEGER NOT NULL,
            year INTEGER NOT NULL,
            FOREIGN KEY (course_id) REFERENCES Courses(course_id),
            FOREIGN KEY (student_id) REFERENCES Students(student_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Student_Advisors (
            advisor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            advisor_name TEXT NOT NULL,
            student_id INTEGER NOT NULL,
            FOREIGN KEY (student_id) REFERENCES Students(student_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Accommodation (
            accommodation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_number INTEGER NOT NULL,
            building TEXT NOT NULL,
            capacity INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_name TEXT NOT NULL,
            course_id INTEGER NOT NULL,
            FOREIGN KEY (course_id) REFERENCES Courses(course_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Purchases (
            purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            purchase_date TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES Students(student_id),
            FOREIGN KEY (book_id) REFERENCES Books(book_id)
        )
    ''')

    conn.commit()
    conn.close()



def initialize_database():
    # Create a database connection
    conn = create_connection()

    # Create tables
    create_tables(conn)

    # Close the connection
    conn.close()


#2.a
# CRUD Operations with SQL

# Create
def add_student(student):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Students (name, age, year_of_enrollment, major, gender, accommodation_id, password)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (student['name'], student['age'], student['year_of_enrollment'], student['major'], student['gender'], student['accommodation_id'], student['password']))
    conn.commit()
    conn.close()


# Read
def get_student(student_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Students WHERE student_id = ?", (student_id,))
    student = cursor.fetchone()
    conn.close()
    return student

# Update
def update_student(student_id, updated_student):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Students
        SET name = ?, age = ?, year_of_enrollment = ?, major = ?, gender = ?, accommodation_id = ?, password = ?
        WHERE student_id = ?
    """, (updated_student['name'], updated_student['age'], updated_student['year_of_enrollment'], updated_student['major'], updated_student['gender'], updated_student['accommodation_id'], updated_student['password'], student_id))
    conn.commit()
    conn.close()


# Delete
def delete_student(student_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Students WHERE student_id = ?", (student_id,))
    conn.commit()
    conn.close()

    
def reset_database():
    # reset database by dropping all tables and reinitializing
    conn = create_connection()
    cursor = conn.cursor()

    # Drop existing tables
    cursor.execute("DROP TABLE IF EXISTS Students")
    cursor.execute("DROP TABLE IF EXISTS Courses")
    cursor.execute("DROP TABLE IF EXISTS Course_Schedules")
    cursor.execute("DROP TABLE IF EXISTS Student_Advisors")
    cursor.execute("DROP TABLE IF EXISTS Accommodation")
    cursor.execute("DROP TABLE IF EXISTS Books")
    cursor.execute("DROP TABLE IF EXISTS Purchases")

    conn.commit()
    conn.close()


#2.b
# Sample data generating and insertion
def generate_sample_data():
    conn = create_connection()
    cursor = conn.cursor()

    # Sample data for Students table
    students = [
        ('Alice Johnson', 20, 2022, 'Computer Science', 'F', 201, '4569'),
        ('Bob Smith', 21, 2021, 'Mathematics', 'M', 202, '789'),
        ('Charlie Brown', 22, 2020, 'Physics', 'M', 203, 'sword123'),
        ('David Wilson', 23, 2023, 'Chemistry', 'M', 204, 'paword123'),
        ('Eva Green', 24, 2022, 'Biology', 'F', 205, 'passwo23'),
        ('Frank Miller', 19, 2023, 'Computer Science', 'M', 201, 'ssword123'),
        ('Grace Davis', 20, 2023, 'Mathematics', 'F', 202, 'pasrd123'),
        ('Hannah White', 21, 2021, 'Physics', 'F', 203, 'word123'),
        ('Ian Taylor', 22, 2022, 'Chemistry', 'M', 204, 'pas23'),
        ('Jessica Hall', 23, 2020, 'Biology', 'F', 205, 'pasword123'),
        ('Kevin Clark', 20, 2021, 'Computer Science', 'M', 201, 'pasord123'),
        ('Linda Lee', 21, 2020, 'Mathematics', 'F', 202, 'pas8765ord123'),
        ('Mike Brown', 22, 2022, 'Physics', 'M', 203, 'pass23'),
        ('Nancy Wilson', 23, 2023, 'Chemistry', 'F', 204, 'pas6525rd123'),
        ('Olivia Green', 24, 2022, 'Biology', 'F', 205, 'pass78223')
    ]
    cursor.executemany("""
        INSERT INTO Students (name, age, year_of_enrollment, major, gender, accommodation_id, password)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, students)

    # Sample data for Courses table
    courses = [
        ('Introduction to Computer Science', 4, random.randint(50, 100)),
        ('Calculus I', 3, random.randint(50, 100)),
        ('Physics I', 4, random.randint(50, 100)),
        ('Organic Chemistry', 4, random.randint(50, 100)),
        ('General Biology', 4, random.randint(50, 100)),
        ('Data Structures', 4, random.randint(50, 100)),
        ('Linear Algebra', 3, random.randint(50, 100)),
        ('Physics II', 4, random.randint(50, 100)),
        ('Biochemistry', 4, random.randint(50, 100)),
        ('Ecology', 4, random.randint(50, 100)),
        ('Algorithms', 4, random.randint(50, 100)),
        ('Statistics', 3, random.randint(50, 100)),
        ('Organic Chemistry II', 4, random.randint(50, 100)),
        ('Cell Biology', 4, random.randint(50, 100)),
        ('Genetics', 4, random.randint(50, 100))
    ]
    cursor.executemany("""
        INSERT INTO Courses (course_name, credits, test_score)
        VALUES (?, ?, ?)
    """, courses)

    # Sample data for Course_Schedules table
    course_schedules = []
    start_year = datetime.now().year - 5  # Generate data for the past 5 years
    for student_id in range(1, 16):
        for term in range(1, 5):  # 4 terms per year
            course_id = random.randint(1, 15)
            year = random.randint(start_year, datetime.now().year)
            course_schedules.append((course_id, student_id, term, year))
    cursor.executemany("""
        INSERT INTO Course_Schedules (course_id, student_id, term, year)
        VALUES (?, ?, ?, ?)
    """, course_schedules)

    # Sample data for Student_Advisors table
    student_advisors = [
        ('Dr. Smith', 1),
        ('Dr. Johnson', 2),
        ('Dr. Williams', 3),
        ('Dr. Brown', 4),
        ('Dr. Davis', 5),
        ('Dr. Lee', 6),
        ('Dr. Taylor', 7),
        ('Dr. Clark', 8),
        ('Dr. Hall', 9),
        ('Dr. Miller', 10),
        ('Dr. Green', 11),
        ('Dr. White', 12),
        ('Dr. Black', 13),
        ('Dr. Evans', 14),
        ('Dr. King', 15)
    ]
    cursor.executemany("""
        INSERT INTO Student_Advisors (advisor_name, student_id)
        VALUES (?, ?)
    """, student_advisors)

    # Sample data for Accommodation table
    accommodations = [
        (201, 101, 'Building A', 2),
        (202, 102, 'Building B', 2),
        (203, 103, 'Building C', 2),
        (204, 104, 'Building D', 3),
        (205, 105, 'Building E', 3),
        (206, 106, 'Building F', 2),
        (207, 107, 'Building G', 2),
        (208, 108, 'Building H', 3),
        (209, 109, 'Building I', 2),
        (210, 110, 'Building J', 3)
    ]
    cursor.executemany("""
        INSERT INTO Accommodation (accommodation_id, room_number ,building, capacity)
        VALUES (?, ?, ?, ?)
    """, accommodations)

    # Sample data for Books table
    books = [
        ('Computer Science Book', 1),
        ('Calculus Book', 2),
        ('Physics Book', 3),
        ('Chemistry Book', 4),
        ('Biology Book', 5),
        ('Data Structures Book', 6),
        ('Linear Algebra Book', 7),
        ('Physics II Book', 8),
        ('Biochemistry Book', 9),
        ('Ecology Book', 10),
        ('Algorithms Book', 11),
        ('Statistics Book', 12),
        ('Organic Chemistry II Book', 13),
        ('Cell Biology Book', 14),
        ('Genetics Book', 15)
    ]
    cursor.executemany("""
        INSERT INTO Books (book_name, course_id)
        VALUES (?, ?)
    """, books)

    # Sample data for Purchases table
    purchases = []
    for student_id in range(1, 16):
        for _ in range(random.randint(1, 5)):  # Random purchases per student
            book_id = random.randint(1, 15)
            purchase_date = datetime.now() - timedelta(days=random.randint(1, 365))
            purchases.append((student_id, book_id, purchase_date))
    cursor.executemany("""
        INSERT INTO Purchases (student_id, book_id, purchase_date)
        VALUES (?, ?, ?)
    """, purchases)

    conn.commit()
    conn.close()

# function to generate a test report into a txt file
def generate_test_report():
    report = []

    # Reset and initialize database
    report.append("Resetting and initializing the database...")
    reset_database()
    initialize_database()

    # Generate and insert sample data
    report.append("Generating and inserting sample data...")
    generate_sample_data()

    # CRUD operations for Students table
    report.append("Performing CRUD operations on the Students table...")

    # Create
    new_student = {
        'name': 'Zachary Scott',
        'age': 22,
        'year_of_enrollment': 2024,
        'major': 'Art',
        'gender': 'M',
        'accommodation_id': 208,
        'password': 'artlover'
    }
    add_student(new_student)
    report.append(f"Added new student: {new_student}")

    # Read
    student = get_student(1)
    report.append(f"Fetched student details: {student}")

    # Update
    updated_student = {
        'name': 'Zachary Scott',
        'age': 23,
        'year_of_enrollment': 2024,
        'major': 'Art and Design',
        'gender': 'M',
        'accommodation_id': 208,
        'password': 'artlover123'
    }
    update_student(1, updated_student)
    report.append(f"Updated student details: {updated_student}")

    # Delete
    delete_student(1)
    report.append(f"Deleted student with student_id = 1")

    # Save the report to a .txt file in the static directory
    os.makedirs('static', exist_ok=True)
    with open('static/test_report.txt', 'w') as file:
        for line in report:
            file.write(line + '\n')



# f1 - f2 - f3 - f4

def choose_course(student_id, course_id, term, year):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Course_Schedules (student_id, course_id, term, year)
        VALUES (?, ?, ?, ?)
    """, (student_id, course_id, term, year))
    conn.commit()
    conn.close()

def manage_accommodation(student_id=None, accommodation_id=None, action="query"):
    conn = create_connection()
    cursor = conn.cursor()
    
    if action == "query":
        if student_id:
            cursor.execute("""
                SELECT * FROM Accommodation WHERE accommodation_id = (
                    SELECT accommodation_id FROM Students WHERE student_id = ?
                )
            """, (student_id,))
        elif accommodation_id:
            cursor.execute("SELECT * FROM Accommodation WHERE accommodation_id = ?", (accommodation_id,))
        else:
            cursor.execute("SELECT * FROM Accommodation")
        result = cursor.fetchall()
    elif action == "assign":
        cursor.execute("""
            UPDATE Students SET accommodation_id = ? WHERE student_id = ?
        """, (accommodation_id, student_id))
        conn.commit()
        result = f"Accommodation {accommodation_id} assigned to student {student_id}"
    
    conn.close()
    return result

def buy_books(student_id, book_id):
    conn = create_connection()
    cursor = conn.cursor()
    purchase_date = date.today().strftime('%Y-%m-%d')
    cursor.execute("""
        INSERT INTO Purchases (student_id, book_id, purchase_date)
        VALUES (?, ?, ?)
    """, (student_id, book_id, purchase_date))
    conn.commit()
    conn.close()


def register_student(name, age, year, major, gender, password):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Students (name, age, year_of_enrollment, major, gender, password) VALUES (?, ?, ?, ?, ?, ?)",
                       (name, age, year, major, gender, password))
        conn.commit()
        return 'You have successfully registered!'
    except sqlite3.IntegrityError:
        return 'Student ID already exists.'
    finally:
        conn.close()

def update_student_info(student_id, name, age, year, major, gender, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Students
        SET name=?, age=?, year_of_enrollment=?, major=?, gender=?, password=?
        WHERE student_id=?
    """, (name, age, year, major, gender, password, student_id))
    conn.commit()
    conn.close()

  