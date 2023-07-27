from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, DATABASE, EMAIL_REGEX, NAME_REGEX, PASSWORD_REGEX
from flask import flash

class Student:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    # Create
    @classmethod
    def create(cls, data):
        query = "INSERT INTO students (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def time_has_students(cls, data):
        query = "INSERT INTO times_has_students (time_id, student_id) VALUES (%(time_id)s, %(student_id)s);"
        connectToMySQL(DATABASE).query_db(query, data)

    # Read
    @classmethod
    def get_all_students(cls):
        query = "SELECT * FROM students;"
        results = connectToMySQL(DATABASE).query_db(query)
        all_students = []
        for day in results:
            all_students.append(cls(day))
        return all_students
    
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        else:
            return False
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM students WHERE id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        else:
            return False
    
    @staticmethod
    def student_validator(data):
        is_valid = True

        if len(data["first_name"]) < 3:
            flash("Name must be longer than 2 characters", "error_students_first_name")
            is_valid = False

        if not NAME_REGEX.match(data["first_name"]):
            flash("Must contain only letters", "error_students_first_name")
            is_valid = False

        if len(data["last_name"]) < 3:
            flash("Name must be longer than 2 characters", "error_students_last_name")
            is_valid = False

        if not NAME_REGEX.match(data["last_name"]):
            flash("Must contain only letters", "error_students_last_name")
            is_valid = False
    
        if Student.get_by_email(data):
            flash("Email already exists", "error_students_email")
            is_valid = False

        if not EMAIL_REGEX.match(data["email"]):
            flash("Email is not a valid email", "error_students_email")
            is_valid = False

        if not PASSWORD_REGEX.match(data["password"]):
            flash("Password must contain an uppercase and lower case letter, special character, and a number", "error2_students_password")
            is_valid = False

        if data["password"] != data["confirm_password"]:
            flash("Passwords do not match", "error2_students_password")
            is_valid = False
        
        return is_valid