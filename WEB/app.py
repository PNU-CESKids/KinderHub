from flask import Flask, render_template, request, session, redirect, url_for
import psycopg2
from test_all import *

app = Flask(__name__)

# Configure your database connection here
DATABASE_URI = "postgresql://db2023:db!2023@::1:5432/termkk"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_email = request.form['useremail']
        user_pw = request.form['password']
        con, conn = connect_to_database()
        logged_in_user_id = log_in(con, conn, user_email, user_pw)
        if logged_in_user_id is not None:
            session['user_id'] = logged_in_user_id
            return redirect(url_for('dashboard'))
        else:
            error_message = "Invalid credentials. Please try again."
            return render_template('login.html', error_message=error_message)
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        con, conn = connect_to_database()

        user_info = view_user_info(conn, int(user_id))
        print("User Info : ", user_info)
        
        if user_info:
            user_name = user_info[0]
            user_role = user_info[1]
            user_id = user_info[2]
            user_email = user_info[3]

            return render_template('dashboard.html', user_id=user_id, user_name=user_name, user_role=user_role, user_email=user_email)
        else:
            return render_template('dashboard.html', user_id=user_id, user_name='Unknown', user_role='Unknown', user_email='Unknown')
        
    return redirect(url_for('login'))
    
# app.py 파일에서
@app.route('/board')
def board():
    return render_template('board.html')

@app.route('/meals')
def meals():
    return render_template('meal.html')

# notification
@app.route('/notification')
def notification():
    return render_template('notification.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/registering', methods=['GET', 'POST'])
def registering():
    if request.method == 'POST':
        # Extract form data
        username = request.form['username']
        useremail = request.form['useremail']
        password = request.form['password']
        role = request.form['role']
        student_id = request.form['student_id']

        # Validate the form data (you can add more validation as needed)
        if not username or not useremail or not password or not role or not student_id:
            return render_template('registering.html', error="All fields are required.")

        # Process the user data and store it in the database
        try:
            # Establish a new database connection
            con, conn = connect_to_database()

            # Print or log debug information
            print(f"Form Data: {username}, {useremail}, {password}, {role}, {student_id}")
            print(f"Database Connection: {conn}")

            # Assuming 'conn' is your database connection
            result = register(con, conn, username, useremail, password, role, student_id)

            # Print or log the result of the registration
            print(f"Registration Result: {result}")

            # Close the connection after the operation
            conn.close()

            # Redirect to the dashboard or login page after a successful registration
            return redirect(url_for('index'))
        except Exception as e:
            session.clear()
            # Handle database errors or other exceptions
            print(f"Error during registration: {e}")
            return render_template('registering.html', error=f"Registration failed: {str(e)}")

    # If it's a GET request, simply render the template
    return render_template('registering.html')


if __name__ == '__main__':
    app.secret_key = 'your_secret_key'
    app.run(debug=True)
