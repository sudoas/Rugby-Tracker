from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__) # Initialize the Flask application

# MongoDB connection
client = MongoClient('mongodb+srv://tyytann:123@cluster0.hrr6fhr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client.RugbyDB  # main database
users = db.users  # collection users

@app.route('/')  # Default route
def home():
    return redirect(url_for('login'))  # Redirect to login page

@app.route('/login', methods=['GET', 'POST'])  # Login route, accepts GET and POST methods
def login():
    message = None  # Initialize message as None, for feedback
    if request.method == 'POST':  # Check if the request method is POST
        username = request.form['username']  # Get username from form data
        password = request.form['password']  # Get password from form data
        user = users.find_one({'username': username})  # Look for the user in the database

        # Check if user exists and password is correct
        if user and check_password_hash(user['password'], password):
            session['username'] = user['username']  # Set the session for the logged-in user
            return redirect(url_for('dashboard'))  # Redirect to dashboard
        elif not user:
            message = 'Username does not exist'  # Set message if username is not found
        else:
            message = 'Incorrect Password'  # Set message if password does not match

    # Render login template with any message feedback
    return render_template('login.html', message=message)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']  # Capture email from the form

        # Check if username or email already exists
        existing_user = users.find_one({'$or': [{'username': username}, {'email': email}]})
        if existing_user is None:
            # Hash the password for security
            hashed_password = generate_password_hash(password)
            # Insert the new user into the database
            users.insert_one({
                'username': username,
                'password': hashed_password,
                'email': email
            })
            # Set user session and redirect to dashboard
            session['username'] = username
            flash('You are successfully registered and logged in.', 'success')
            return redirect(url_for('dashboard'))
        else:
            # Flash message for existing user or email
            flash('Username or email already exists.', 'danger')

    return render_template('register.html')

@app.route('/dashboard')  # Dashboard route
def dashboard():
    # Check if a user is logged in
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if no user is logged in
    return render_template('dashboard.html')  # Render the dashboard page

@app.route('/logout')  # Logout route
def logout():
    session.pop('username', None)  # Remove the user session
    return redirect(url_for('login'))  # Redirect to the login page after logout

if __name__ == '__main__':
    app.run(debug=True)  # Run the application with debugging enabled

