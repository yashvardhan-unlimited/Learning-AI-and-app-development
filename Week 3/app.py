import os
from datetime import datetime

from flask import request
import requests

def banklogin():
    # Get the username and password from the form.
    username = request.form.get("username")
    password = request.form.get("password")
    # Find the user in the database by username and password.
    # In a real application, you should never store passwords in plain text.
    # Instead, you should hash the password using a secure hashing algorithm like bcrypt,
    # and then store the hashed password in the database. When verifying the password,
    # Anew feature 2 















































# A new line of code
