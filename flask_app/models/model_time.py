from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import model_day

class Time:
    def __init__(self, data):
        self.id = data["id"]
        self.day_id = data["day_id"]
        self.start_time = data["start_time"]
        self.end_time = data["end_time"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    # create
    @classmethod
    def create(cls, data):
        query = "INSERT INTO times (day_id, start_time, end_time) VALUES (%(day_id)s, %(start_time)s, %(end_time)s);"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    # read 
    @classmethod
    def get_all_on_day(cls, data):
        query = "SELECT * FROM times WHERE day_id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if not results:
            return []
        all_times = []
        for time in results:
            all_times.append(cls(time))
        return all_times

    # read 
    @classmethod
    def get_all_times(cls):
        query = "SELECT * FROM times JOIN days ON days.id = times.day_id;"
        results = connectToMySQL(DATABASE).query_db(query)
        all_times = []
        for time in results:
            time_instance = cls(time)
            day_data = {
                **time,
                "id": time["days.id"],
                "created_at": time["days.created_at"],
                "updated_at": time["days.updated_at"]
            }
            day_instance = model_day.Day(day_data)
            time_instance.day = day_instance
            all_times.append(time_instance)
        return all_times
    
    # read
    @classmethod
    def get_by_id(cls, id):
        query = "SELECT * FROM times WHERE id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, {"id": id})
        if results:
            return cls(results[0])
        else:
            return False
        
    #update 
    @classmethod
    def update(cls, data):
        query = "UPDATE times SET day_id = %(day_id)s, start_time = %(start_time)s, end_time = %(end_time)s WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    # delete
    @classmethod
    def delete(cls, id):
        query = "DELETE FROM times WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, {"id": id})
