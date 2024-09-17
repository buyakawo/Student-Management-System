import threading
import requests
import time

# The base URL of our Flask application
BASE_URL = 'http://127.0.0.1:5000'  

# Function to simulate login action
def login(username, password):
    response = requests.post(f"{BASE_URL}/login", data={"username": username, "password": password})
    print(f"Login response for {username}: {response.status_code}")

# Function to simulate registration action
def register(name, age, year, major, gender, password):
    data = {
        "name": name,
        "age": age,
        "year_of_enrollment": year,
        "major": major,
        "gender": gender,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/register", data=data)
    print(f"Registration response for {name}: {response.status_code}")

# Simulate concurrent logins and registrations
def simulate_concurrent_actions():
    threads = []

    # Simulate concurrent logins
    for i in range(5):  # Example: 5 concurrent logins
        username = f"user{i+1}"
        password = "password"
        thread = threading.Thread(target=login, args=(username, password))
        threads.append(thread)
        thread.start()

    # Simulate concurrent registrations
    for i in range(3):  # Example: 3 concurrent registrations
        name = f"User{i+1}"
        age = 25
        year = 2023
        major = "Computer Science"
        gender = "Male"
        password = "password"
        thread = threading.Thread(target=register, args=(name, age, year, major, gender, password))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

# Entry point
if __name__ == "__main__":
    print("Simulating concurrent logins and registrations...")
    simulate_concurrent_actions()
    print("Concurrent actions simulation complete.")
