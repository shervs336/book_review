import os
import requests
import function

from flask import Flask, session, render_template, request
from flask_session import Session
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


@app.route("/")
def index():

    res = requests.get('https://www.goodreads.com/book/review_counts.json',params={"key": "bUBB89aFTLNjMwCMDnOWfQ", "isbns": "9781632168146"})
    print(res.json())
    return render_template("home.html")

@app.route("/register", methods=['POST', 'GET'])
def registration():
    error = [];

    if request.method == 'GET':
        return render_template("auth/registration.html")

    name = request.form.get("name")
    username = request.form.get("username")
    password = request.form.get("password")

    return render_template("auth/success.html")

@app.route("/login", methods=['GET', 'POST'])
def login():

    return 'Login'
