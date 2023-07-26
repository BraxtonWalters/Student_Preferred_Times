import re
from flask import Flask
app = Flask(__name__)
app.secret_key = "shhhhhh"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$') 
TIME_REGEX = re.compile(r'^/((1[0-2]|0?[1-9]):([0-5][0-9]) ?([AaPp][Mm]))/')
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# add the database!!!
DATABASE = "student_preferred_times"


# pipenv install flask pymysql flask-bcrypt
# pipenv shell
# python server.py