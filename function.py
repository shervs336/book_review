import os

from flask import request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

def getLoggedUser(user):
    return user

def active(param, sr_only = False):
    rule = request.url_rule

    print(rule.rule);

    # Check if rule is active
    if param in rule.rule :

        if sr_only :

            return "<span class='sr-only'>(current)</span>"

        else :

            return "active"

    return ""
