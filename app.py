import hashlib
from flask import Flask, redirect, render_template, request, session
from user_booking import book_hall
import sqlite3
import json

app = Flask(__name__)

# Set secret key for session management
app.secret_key = 'your_secret_key'

# Route to render the signup page
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/support")
def support():
    return render_template("support.html")

# Route to render the signup page
@app.route("/signup")
def signup_page():
    return render_template("signup.html")

# Route to handle signup form submission
@app.route("/signup", methods=["POST"])
def signup():
    result_message = None
    result_type = None 
    # Get form data
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    user_type = request.form.get("user_type")

    # Save user data into the database
    result_message = save_user(username, email, password, user_type)
    if result_message == "User data saved successfully!":
        result_type = "success"
        return render_template("signup.html", result_type=result_type,result_message=result_message)
    else:
        result_type = "danger"
        return render_template("signup.html", result_message=result_message,result_type=result_type)

    return "Signup successful!"

# Function to save user data into the database
def save_user(username, email, password, user_type):
    try:
        conn = sqlite3.connect("HallManagement.db")
        cursor = conn.cursor()

        # Check if the username or email already exists
        cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email))
        existing_user = cursor.fetchone()
        if existing_user:
            return "User  with the username & email already exists!"
        
        # Create the users table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            username TEXT NOT NULL,
                            email TEXT NOT NULL,
                            password TEXT NOT NULL,
                            user_type TEXT NOT NULL
                        )''')

        # Insert user data into the users table
        cursor.execute("INSERT INTO users (username, email, password, user_type) VALUES (?, ?, ?, ?)",
                       (username, email, password, user_type))
        
        conn.commit()
        return "User data saved successfully!"
    except sqlite3.Error as error:
        return "Failed to save user data: " + str(error)
    finally:
        conn.close()

# Route to render the login page
@app.route("/")
def login_page():
    return render_template("login.html")

# Route to handle login form submission
@app.route("/login", methods=["POST"])
def login():
    # Get username and password from the form
    username = request.form.get("username")
    password = request.form.get("password")

    # Query the database to check if the user exists and the password matches
    conn = sqlite3.connect("HallManagement.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        # Store the username in the session
        session['username'] = username
        if user[4] == "admin":
            # User is an admin, redirect to admin dashboard or perform admin-specific actions
            return redirect("/approve_booking")
        elif user[4] == "student":
            # User is a student, redirect to student dashboard or perform student-specific actions
            return redirect("/user_booking")
    else:
        # Unknown user type or invalid credentials, handle accordingly
        result_type = "danger"
        
        return render_template("login.html",result_type=result_type,result_message="Invalid username or password.")
        #return "Invalid username or password."

# Route to display user booking page and handle booking form submission
@app.route("/user_booking", methods=["GET", "POST"])
def user_booking():
    result_message = None
    result_type = None 
    # Check if the user is logged in
    # if 'username' in session:
    
    if request.method == "POST":
            user_name = request.form.get("user_name")
            hall_name = request.form.get("hall_name")
            booking_date = request.form.get("booking_date")
            result_message = book_hall(user_name, hall_name, booking_date)
          
    if result_message == "A booking for the same hall and date already exists.":
        username = session['username']
        result_type = "danger"
        
        return render_template("user_booking.html", username=username,result_type=result_type,result_message=result_message,  existing_bookings=get_existing_bookings(username))
    else:
        username = session['username']
        result_type = "success"
        return render_template("user_booking.html", username=username,result_message=result_message,result_type=result_type, existing_bookings=get_existing_bookings(username))

# Function to fetch existing bookings associated with the user
def get_existing_bookings(username):
    conn = sqlite3.connect("HallManagement.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings WHERE user_name = ?", ( username.lower(),))
    existing_bookings = cursor.fetchall()
    conn.close()
    
    # Convert booking_requests to a list of dictionaries
    booking_dicts = []
    for booking in existing_bookings:
        booking_dict = {
            "id": booking[0],
            "user_name": booking[1],
            "hall_name": booking[2],
            "booking_date": booking[3],
            "status": booking[4]
            # Add more fields as needed
        }
        booking_dicts.append(booking_dict)
    
    # Convert list of dictionaries to JSON format
    booking_json = json.dumps(booking_dicts)
    return booking_json

# Function to fetch booking requests from the database
def get_booking_requests():
    conn = sqlite3.connect("HallManagement.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings WHERE status='Pending'")
    booking_requests = cursor.fetchall()
    conn.close()

    # Convert booking_requests to a list of dictionaries
    booking_dicts = []
    for booking in booking_requests:
        booking_dict = {
            "id": booking[0],
            "user_name": booking[1],
            "hall_name": booking[2],
            "booking_date": booking[3]
            # Add more fields as needed
        }
        booking_dicts.append(booking_dict)
    
    # Convert list of dictionaries to JSON format
    booking_json = json.dumps(booking_dicts)
    return booking_json

@app.route("/approve_booking")
def approve_booking():
    return render_template("admin_approval.html", bookings=get_booking_requests())

@app.route("/approve_booking/<int:id>", methods=["GET", "POST"])
def approve_specific_booking(id):
    if request.method == "POST":
        # Code to approve or reject booking request in the database
        # You need to implement this functionality based on your database schema
        # For demonstration purposes, let's assume you have a function to update the booking status
        update_booking_status(id, request.form["action"])
        result_type = "success"
        #return f"Booking with ID {id} has been {request.form['action']}ed."
    return render_template("admin_approval.html",result_type=result_type,result_message=f"Booking with ID {id} has been {request.form['action']}ed.", bookings=get_booking_requests())

# Function to update booking status in the database
def update_booking_status(booking_id, action):
    conn = sqlite3.connect("HallManagement.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE bookings SET status = ? WHERE id = ?", (action, booking_id))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    app.run(debug=True)
