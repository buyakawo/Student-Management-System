from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from modules.database import create_connection, initialize_database, generate_sample_data, reset_database, create_tables,  generate_test_report
from functools import wraps

# Reset and initialize the database with sample data and reports
reset_database()
conn = create_connection()
create_tables(conn)
generate_sample_data()
generate_test_report()

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = 'miawmiaw'  # secret key for session management

# Decorator to ensure the user is logged in before accessing certain routes
def login_required(f):
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    wrap.__name__ = f.__name__
    return wrap

# Route for the home page
@app.route('/')
def home():
    return redirect(url_for('login'))

# Route for login page 
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = create_connection()
        cursor = conn.cursor()
        #check if student exist in the database
        cursor.execute("SELECT * FROM Students WHERE name=? AND password=?", (username, password))
        result = cursor.fetchone()
        conn.close()
    #if account exists in students table , log them in   
        if result:
            session['logged_in'] = True
            session['student_id'] = result[0]
            session['student_name'] = result[1]
            return redirect(url_for('dashboard'))
        else:
    #if account does not exist or username/password, show an error message        
            msg = 'Invalid Username or Password'
        
    return render_template('login.html', msg=msg)

# route for registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        #get form data
        name = request.form['name']
        age = request.form['age']
        year = request.form['year_of_enrollment']
        major = request.form['major']
        gender = request.form['gender']
        accommodation_id = request.form['accommodation_id']
        password = request.form['password']

        # Simple validation checks
        if not name or not age or not year or not major or not gender or not accommodation_id or not password:
            msg = 'Please fill out the form completely!'
        else:
            conn = create_connection()
            cursor = conn.cursor()
            try:
                #insert the new student into the database
                cursor.execute("INSERT INTO Students (name, age, year_of_enrollment, major, gender, accommodation_id, password) VALUES (?, ?, ?, ?, ?, ?, ?)",
                               (name, age, year, major, gender, accommodation_id, password))
                conn.commit()
                msg = 'You have successfully registered!'
            except sqlite3.IntegrityError:
                msg = 'An error occurred. Please try again.'
            finally:
                conn.close()
        return render_template('register.html', msg=msg)
    return render_template('register.html', msg=msg)

# route for the dashboard page
@app.route('/dashboard')
@login_required
def dashboard():
    student_name = session['student_name']
    return render_template('dashboard.html', student_name=student_name)


#route for updating student information or deleting account
@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    msg = ''
    student_id = session['student_id']
    conn = create_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        if request.form['action'] == 'update':
            # get form data for update
            name = request.form['name']
            age = request.form['age']
            year_of_enrollment = request.form['year_of_enrollment']
            major = request.form['major']
            gender = request.form['gender']
            password = request.form['password']
            # update student information in the database
            cursor.execute("""
                UPDATE Students
                SET name=?, age=?, year_of_enrollment=?, major=?, gender=?, password=?
                WHERE student_id=?
            """, (name, age, year_of_enrollment, major, gender, password, student_id))
            conn.commit()
            msg = 'Information updated successfully!'
        elif request.form['action'] == 'delete':
            # delete student from database
            cursor.execute("DELETE FROM Students WHERE student_id=?", (student_id,))
            conn.commit()
            session.clear() # clear session after deletion
            return redirect(url_for('login'))
    cursor.execute("SELECT name, age, year_of_enrollment, major, gender FROM Students WHERE student_id=?", (student_id,))
    student_info = cursor.fetchone()
    conn.close()
    return render_template('update.html', student_info=student_info, msg=msg)

# route for generating and displaying reports, accessible only after login
@app.route('/reports')
@login_required
def reports():
    from modules.analysis import generate_reports
    generate_reports()  
    return render_template('analysis.html')  

# route for logging out
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# run the flask app
if __name__ == '__main__':
    app.run(debug=True)
