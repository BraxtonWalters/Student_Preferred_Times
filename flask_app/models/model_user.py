from flask_app import bcrypt, DATABASE, EMAIL_REGEX, NAME_REGEX, PASSWORD_REGEX
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.full_name = f"{self.first_name} {self.last_name}"

    #create
    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results

    # Read by email
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        else:
            return False

    # Read by ID
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        else:
            return False
 
    # Reg Validator
    @staticmethod
    def register_validator(data):
        is_valid = True

        if len(data["first_name"]) < 3:
            flash("Name must be longer than 2 characters", "error_users_first_name")
            is_valid = False

        if not NAME_REGEX.match(data["first_name"]):
            flash("Must contain only letters", "error_users_first_name")
            is_valid = False

        if len(data["last_name"]) < 3:
            flash("Name must be longer than 2 characters", "error_users_last_name")
            is_valid = False

        if not NAME_REGEX.match(data["last_name"]):
            flash("Must contain only letters", "error_users_last_name")
            is_valid = False
        
        if User.get_by_email(data):
            flash("Email already exists", "error_users_email")
            is_valid = False

        if not EMAIL_REGEX.match(data["email"]):
            flash("Email is not a valid email", "error_users_email")
            is_valid = False

        if not PASSWORD_REGEX.match(data["password"]):
            flash("Password must contain an uppercase and lower case letter, special character, and a number", "error_user_password")
            is_valid = False

        if data["password"] != data["confirm_password"]:
            flash("Passwords do not match", "error2_user_password")
            is_valid = False
        
        return is_valid
    
    @staticmethod
    def login_validator(data):
        is_valid = True
        user = User.get_by_email(data)
        if user:
            if not bcrypt.check_password_hash(user.password, data["password"]):
                flash("Wrong password" , "error_password_user_password")
                is_valid = False
        else:
            flash("Email is not a registered email", "error_login_user_email")
            is_valid = False

        return is_valid