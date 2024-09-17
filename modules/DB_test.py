import unittest
import sqlite3
from datetime import date
import database  


class TestDatabase(unittest.TestCase):


    # Setup method to reset and initialize the database before each test
    def setUp(self):
        database.reset_database()  # Reset the database to a clean state
        database.initialize_database()  # Initialize the database schema
        database.generate_sample_data()  # Populate the database with sample data


    # Test to ensure the database is initialized with the correct tables
    def test_initialize_database(self):
        conn = database.create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        conn.close()

        expected_tables = {
            'Students',
            'Courses',
            'Course_Schedules',
            'Student_Advisors',
            'Accommodation',
            'Books',
            'Purchases'
        }

        existing_tables = {table[0] for table in tables}
        self.assertTrue(expected_tables.issubset(existing_tables))

    # test to add a new student to the database
    def test_add_student(self):
        student = {
            'name': 'John Doe',
            'age': 25,
            'year_of_enrollment': 2024,
            'major': 'Engineering',
            'gender': 'M',
            'accommodation_id': 206,
            'password': 'password123'
        }
        database.add_student(student)

        conn = database.create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Students WHERE name = ?", (student['name'],))
        added_student = cursor.fetchone()
        conn.close()

        self.assertIsNotNone(added_student)
        self.assertEqual(added_student[1], student['name'])

    # test to retrieve a student by ID
    def test_get_student(self):
        student = database.get_student(1)
        self.assertIsNotNone(student)
        self.assertEqual(student[1], 'Alice Johnson')

    # test to update an existing student's details
    def test_update_student(self):
        updated_student = {
            'name': 'Alice Johnson',
            'age': 21,
            'year_of_enrollment': 2022,
            'major': 'Data Science',
            'gender': 'F',
            'accommodation_id': 201,
            'password': 'newpass123'
        }
        database.update_student(1, updated_student)

        student = database.get_student(1)
        self.assertIsNotNone(student)
        self.assertEqual(student[1], updated_student['name'])
        self.assertEqual(student[2], updated_student['age'])
        self.assertEqual(student[3], updated_student['year_of_enrollment'])
        self.assertEqual(student[4], updated_student['major'])
        self.assertEqual(student[5], updated_student['gender'])
        self.assertEqual(student[6], updated_student['accommodation_id'])
        self.assertEqual(student[7], updated_student['password'])


    # test to delete a student by id
    def test_delete_student(self):
        database.delete_student(1)
        student = database.get_student(1)
        self.assertIsNone(student)

    # test to enroll a student in a course
    def test_choose_course(self):
        database.choose_course(1, 2, 3, 2024) # Enroll student 1 in course 2 for term 3 in year 2024
        conn = database.create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Course_Schedules WHERE student_id = 1 AND course_id = 2 AND term = 3 AND year = 2024")
        course_schedule = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(course_schedule)    


    # test to manage a student's accomodation
    def test_manage_accommodation(self):
        result = database.manage_accommodation(student_id=1, action="query")
        self.assertEqual(result[0][1], 101)  # Assuming accommodation ID 101 is assigned to student 1

        database.manage_accommodation(student_id=1, accommodation_id=202, action="assign")
        student = database.get_student(1)
        self.assertEqual(student[6], 202)  # Check if the accommodation ID has been updated

    # test to purchase books for a student
    def test_buy_books(self):
        database.buy_books(1, 1)  # student 1 buy book 1
        conn = database.create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Purchases WHERE student_id = 1 AND book_id = 1")
        purchase = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(purchase)
        self.assertEqual(purchase[1], 1)
        self.assertEqual(purchase[2], 1)
        self.assertEqual(purchase[3], str(date.today()))  # check if purchase date is today   


if __name__ == '__main__':
    unittest.main()
