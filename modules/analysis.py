import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
from modules.database import create_connection


# function to create a connection to the database
def create_connection():
    conn = sqlite3.connect('db/database.sqlite')
    return conn

#3.a.1
def calculate_students_gender_ratio():
    conn = create_connection()
    query = """
    SELECT major, gender, COUNT(*) as count
    FROM Students
    GROUP BY major, gender
    """
    df = pd.read_sql(query, conn)  # Read the SQL query into a DataFrame
    conn.close()

    pivot_df = df.pivot(index='major', columns='gender', values='count').fillna(0)
    
    # Ensure both male and female columns exist in the DataFrame
    if 'M' not in pivot_df.columns:
        pivot_df['M'] = 0
    if 'F' not in pivot_df.columns:
        pivot_df['F'] = 0
    
    pivot_df['total'] = pivot_df.sum(axis=1)  # Calculate total students per major
    pivot_df['male_ratio'] = pivot_df['M'] / pivot_df['total']  # Calculate male ratio
    pivot_df['female_ratio'] = pivot_df['F'] / pivot_df['total']  # Calculate female ratio
    
    return pivot_df

#3.a.2
def compare_results_in_majors():
    conn = create_connection()
    query = """
    SELECT Students.major, AVG(Courses.test_score) as average_score
    FROM Course_Schedules
    JOIN Students ON Course_Schedules.student_id = Students.student_id
    JOIN Courses ON Course_Schedules.course_id = Courses.course_id
    GROUP BY Students.major
    """
    df = pd.read_sql(query, conn) #read the sql query into a dataframe
    conn.close()
    return df

#3.a.3
def analyze_age_vs_test_scores():
    conn = create_connection()
    query = """
    SELECT Students.age, Courses.test_score
    FROM Course_Schedules
    JOIN Students ON Course_Schedules.student_id = Students.student_id
    JOIN Courses ON Course_Schedules.course_id = Courses.course_id
    """
    df = pd.read_sql(query, conn) #read the sql query into a dataframe
    conn.close()
    return df

#3.a.4
def analyze_regional_distribution_vs_test_scores():
    conn = create_connection()
    query = """
    SELECT Students.major, Students.accommodation_id, AVG(Courses.test_score) as average_score
    FROM Course_Schedules
    JOIN Students ON Course_Schedules.student_id = Students.student_id
    JOIN Courses ON Course_Schedules.course_id = Courses.course_id
    GROUP BY Students.major, Students.accommodation_id
    """
    df = pd.read_sql(query, conn) #read the sql query into a dataframe
    conn.close()
    return df

#3.a.5
def custom_analysis():
    conn = create_connection()
    query = """
    SELECT Students.name, Courses.course_name, Courses.test_score
    FROM Course_Schedules
    JOIN Students ON Course_Schedules.student_id = Students.student_id
    JOIN Courses ON Course_Schedules.course_id = Courses.course_id
    """
    df = pd.read_sql(query, conn) #read the sql query into a dataframe
    conn.close()
    return df


#3.b
def generate_reports():
    sns.set(style="whitegrid")

    # Directory to save images
    image_dir = "static/"

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Calculate the number of students and gender ratio for each major
    gender_ratio_df = calculate_students_gender_ratio()
    if gender_ratio_df.empty:
        print("Gender ratio DataFrame is empty.")
    else:
        pdf.set_font("Arial", size=16)
        pdf.cell(200, 10, txt="Gender Ratio by Major:", ln=True, align='L')
        pdf.ln(10)
        
        gender_ratio_img = f"{image_dir}gender_ratio.png"
        gender_ratio_df[['male_ratio', 'female_ratio']].plot(kind='bar', stacked=True)
        plt.title('Gender Ratio by Major')
        plt.xlabel('Major')
        plt.ylabel('Ratio')
        plt.savefig(gender_ratio_img)
        plt.close()

        pdf.image(gender_ratio_img, x=10, y=None, w=180)
        pdf.ln(95)

    # Compare results in different majors
    results_df = compare_results_in_majors()
    if results_df.empty:
        print("Results DataFrame is empty.")
    else:
        pdf.cell(200, 10, txt="Average Test Scores by Major:", ln=True, align='L')
        pdf.ln(10)

        results_img = f"{image_dir}average_test_scores.png"
        sns.barplot(x='average_score', y='major', data=results_df)
        plt.title('Average Test Scores by Major')
        plt.xlabel('Average Score')
        plt.ylabel('Major')
        plt.savefig(results_img)
        plt.close()

        pdf.image(results_img, x=10, y=None, w=180)
        pdf.ln(95)

    # Analyze the relationship between student age and test scores
    age_scores_df = analyze_age_vs_test_scores()
    if age_scores_df.empty:
        print("Age vs. test scores DataFrame is empty.")
    else:
        pdf.cell(200, 10, txt="Relationship Between Age and Test Scores:", ln=True, align='L')
        pdf.ln(10)

        age_scores_img = f"{image_dir}age_vs_test_scores.png"
        sns.scatterplot(x='age', y='test_score', data=age_scores_df)
        plt.title('Relationship Between Age and Test Scores')
        plt.xlabel('Age')
        plt.ylabel('Test Score')
        plt.savefig(age_scores_img)
        plt.close()

        pdf.image(age_scores_img, x=10, y=None, w=180)
        pdf.ln(95)

    # Analyze the relationship between students' regional distribution and test scores
    regional_scores_df = analyze_regional_distribution_vs_test_scores()
    if regional_scores_df.empty:
        print("Regional distribution vs. test scores DataFrame is empty.")
    else:
        pdf.cell(200, 10, txt="Regional Distribution vs. Test Scores:", ln=True, align='L')
        pdf.ln(10)

        regional_scores_img = f"{image_dir}regional_vs_test_scores.png"
        sns.barplot(x='accommodation_id', y='average_score', hue='major', data=regional_scores_df)
        plt.title('Regional Distribution vs. Test Scores')
        plt.xlabel('Accommodation ID')
        plt.ylabel('Average Score')
        plt.legend(title='Major')
        plt.savefig(regional_scores_img)
        plt.close()

        pdf.image(regional_scores_img, x=10, y=None, w=180)
        pdf.ln(95)

    # Custom analysis
    custom_df = custom_analysis()
    if custom_df.empty:
        print("Custom analysis DataFrame is empty.")
    else:
        custom_img = f"{image_dir}custom_analysis.png"
        sns.scatterplot(x='course_name', y='test_score', hue='name', data=custom_df)
        plt.title('Custom Analysis - Students and Their Courses with Test Scores')
        plt.xlabel('Course Name')
        plt.ylabel('Test Score')
        plt.xticks(rotation=90)  # Rotate x labels if there are many course names
        plt.legend(title='Student Name')
        plt.savefig(custom_img)
        plt.close()

# Call the function to generate the reports
generate_reports()
