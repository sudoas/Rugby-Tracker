from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)  # Initialize the Flask application

# Set a secret key for securely signing the session cookie
app.secret_key = os.environ.get('SECRET_KEY', '123')

# MongoDB connection code gotten from MongoDB
print("Connecting to Mongo DB")
uri = os.environ.get('MONGO_URI',
                     "mongodb+srv://tyytann:123@cluster0.hrr6fhr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)
db = client.RugbyDB  # main database
users = db.users  # collection users


@app.route('/')  # Default route
def home():
    print("Redirect to Home")
    return redirect(url_for('login'))  # Redirect to login page


@app.route('/login', methods=['GET', 'POST'])  # Login route, accepts GET and POST methods
def login():
    print("calling login function")
    invalid = None  # Initialize message as None, for feedback
    if request.method == 'POST':  # Check if the request method is POST
        print("enter POST method")
        username = request.form['username']  # Get username from form data
        password = request.form['password']  # Get password from form data
        print("Username: ", username)
        print("Password: ", password)
        user = users.find_one({'username': username}, {'username': 1, '_id': 0})  # Look for the user in the database
        print("User from DB:", user)
        pwd = users.find_one({'password': password}, {'password': 1, '_id': 0})
        print("Password from DB:", pwd)

        # Check if user exists and password is correct
        if user and pwd:
            print("Redirecting dashboard ")
            session['username'] = user['username']  # Set the session for the logged-in user
            return redirect(url_for('admindashboard'))  # Redirect to dashboard
        else:
            print("Invalid username or password")
            # Render login template if no account works
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get data from the form
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        # Check if the username or email already exists in the database
        existing_user = users.find_one({'username': username}, {'role': role})
        if existing_user is None:
            # Insert the new user document into MongoDB
            users.insert_one({
                'username': username,
                'password': password,
                'role': role
            })
            # Store the username in the session
            session['username'] = username
            print("Inserted new user")
            return redirect(url_for('admindashboard'))
        else:
            flash('Username or email already exists.')
            return redirect(url_for('register'))

    # If GET request, render the registration form
    return render_template('register.html')


@app.route('/admindashboard')  # Dashboard route
def admindashboard():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    return render_template('admindashboard.html')  # Render the dashboard page


@app.route('/logout')  # Logout route
def logout():
    session.pop('username', None)  # Remove the user session
    return redirect(url_for('login'))  # Redirect to the login page after logout


@app.route('/player_stat_recorder')  # Admin access page
def player_stat_recorder():
    return render_template('player_stat_recorder.html')


@app.route('/game_stat_recorder')  # Admin access page
def game_stat_recorder():
    return render_template('game_stat_recorder.html')


@app.route('/player_results')  # All access page
def player_results():
    return render_template('player_results.html')


@app.route('/game_results')  # All access page
def game_results():
    return render_template('game_results.html')


if __name__ == '__main__':
    app.run(debug=True)  # Run the application with debugging enabled
