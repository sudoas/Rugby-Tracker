from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb+srv://tyytann:123@cluster0.hrr6fhr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client.RugbyDB # main database
users = db.users # collection users

@app.route('/')
def home():
    return redirect(url_for('login')) # login page redirect if the url is just /

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST': # Check if the request method is POST (if the user sent something)
        username = request.form['username']
        password = request.form['password']
        user = users.find_one({'username': username}) # Find the user in the database

        # Check if the user exists and the password matches
        if user and password(user['password'], password):
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard')) # Redirect to the dashboard (will make a dashboard html page)
        else:
            flash('Invalid username or password', 'danger') # does not exist

    return render_template('login.html') # Render the login page

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST': # Check if the request method is POST
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        if users.find_one({'username': username}):
            flash('Username already exists!')
        else:
            users.insert_one({'username': username, 'password': password) # Insert the new user into the database
            flash('Registration successful! You can now log in.')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return 'dasboard' # Return a simple dashboard message

if __name__ == '__main__':
    app.run(debug=True)
