from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Student:
    def __init__(self, data):
        self.id = data["id"]
        self.time_id = data["time_id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    # Create
    @classmethod
    def create(cls, data):
        query = "INSERT INTO students (time_id, first_name, last_name, email, password) VALUES (%(time_id)s, %(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    # Read
    @classmethod
    def get_all_students(cls):
        query = "SELECT * FROM students;"
        results = connectToMySQL(DATABASE).query_db(query)
        all_students = []
        for day in results:
            all_students.append(cls(day))
        return all_students
    
    # Update
    @classmethod
    def update(cls, data):
        query = "UPDATE "