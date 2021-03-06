import os
import requests
import sys

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from function import active
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Add template global
app.add_template_global(active, name = "active")

@app.route("/index")
@app.route("/")
def index():

    res = requests.get('https://www.goodreads.com/book/review_counts.json',params={"key": "bUBB89aFTLNjMwCMDnOWfQ", "isbns": "9781632168146"})
    print(res.json())
    return render_template("home.html", title = 'Home Page - Book Review')

# Auth Routes
@app.route("/register", methods=['POST', 'GET'])
def registration():

    # Redirect if logged in
    if session["auth"] :
        return redirect(url_for('index'));

    # Assign an empty error list
    errors = []
    form_data = {}

    # Must load template if method is GET
    if request.method == 'GET':
        return render_template("auth/registration.html", title = 'Registration - Book Review', errors = errors, form_data = form_data)

    form_data = request.form
    name = form_data.get("name")
    username = form_data.get("username")
    password = form_data.get("password")
    confirm_password = form_data.get("confirm_password")

    if not name :
        errors.append('Name is required')

    if not username :
        errors.append('Username is required')

    if username :
        # Look for duplicate username
        users = db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).fetchall()

        if len(users) > 0:
            errors.append('Username already exists')

    if not password :
        errors.append('Password is required')

    if not confirm_password :
        errors.append('Confirm Password is required')

    if password != confirm_password :
        errors.append('Password did not match confirm password')

    if len(errors) > 0:
        return render_template("auth/registration.html", title = 'Registration - Book Review', errors = errors, form_data = form_data)

    # Start inserting new user to database
    user =  db.execute("INSERT INTO users (name, username, password) VALUES (:name, :username, :password)",
            {"name": name, "username": username, "password": password})
    print(f"Added user {name} with username {username}.")
    db.commit()

    return render_template("auth/success.html",  title = 'Registered Successfully - Book Review')

@app.route("/login", methods=['GET', 'POST'])
def login():
    print(session.get("auth"));

    # Redirect if logged in
    if session["auth"] :
        return redirect(url_for('index'));

    # Assign an empty error list
    errors = []

    if request.method == 'GET':
        return render_template("auth/login.html", title = 'Login - Book Review', errors = errors)

    username = request.form.get("username")
    password = request.form.get("password")

    # Validate Form
    if not username :
        errors.append('Username is required')

    if not password :
        errors.append('Password is required')

    if len(errors) > 0:
        return render_template("auth/login.html", title = 'Registration - Book Review', errors = errors, form_data = form_data)

    # Check for successful login
    session["auth"] = db.execute("SELECT * FROM users WHERE username = :username AND password = :password", {"username": username, "password": password}).fetchone()

    if session["auth"] :
        return redirect(url_for("index"))
    else :
        errors.append('Username and Password did not matched in our records')
        return render_template("auth/login.html", title = 'Login - Book Review', errors = errors)

@app.route('/logout', methods = ['GET', 'POST'])
def logout():

    if request.method == 'GET':
        return redirect(url_for("err_404"))

    session['auth'] = None
    return redirect(url_for("index"))

# Error Routes
@app.route('/404')
def err_404():
    return render_template('error/404.html', title = '404 Page Not Found - Book Review')
