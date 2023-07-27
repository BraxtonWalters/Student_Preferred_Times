from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import model_time


class Day:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @property
    def get_times(self):
        return model_time.Time.get_all_on_day({"id": self.id})
    
    # create
    @classmethod
    def create(cls, data):
        query = "INSERT INTO days (name) VALUES (%(name)s)"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    # read
    @classmethod
    def get_all_days(cls):
        query = "SELECT * FROM days"
        results = connectToMySQL(DATABASE).query_db(query)
        all_days = []
        for day in results:
            all_days.append(cls(day))
            
        return all_days
    
    #read
    @classmethod
    def get_all_times(cls, data):
        query = "SELECT * FROM days LEFT JOIN times ON days.id = times.day_id WHERE days.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if not results:
            return []
        
        day_instance = cls(results[0])
        day_instance.all_times = []
        if results[0]["times.id"] != None:
            for day in results:
                time_data = {
                    **day,
                    "id": day["times.id"],
                    "created_at": day["times.created_at"],
                    "updated_at": day["times.updated_at"]
                }
                time_instance = model_time.Time(time_data)
                day_instance.all_times.append(time_instance)
        return day_instance

    # read
    @classmethod
    def get_by_id(cls, id):
        query = "SELECT * FROM days WHERE id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, {"id": id})
        return cls(results[0])
    
    #read
    # @classmethod
    # def get_all_days(cls):
    #     query = "SELECT * FROM days LEFT JOIN times ON days.id = times.day_id;"
    #     results = connectToMySQL(DATABASE).query_db(query)

    #     if not results:
    #         return []
    #     all_days = []
    #     for day in results:
    #         day_instance = cls(day)
    #         day_instance.all_times = []
    #         if day["times.id"] != None:
    #             for time_slot in day:
    #                 time_data = {
    #                     **time_slot,
    #                     "id": time_slot["times.id"],
    #                     "created_at": time_slot["times.created_at"],
    #                     "updated_at": time_slot["times.updated_at"]
    #                 }
    #                 time_instance = model_time.Time(time_data)
    #                 day_instance.all_times.append(time_instance)
    #     print("*" * 100)
    #     print(all_days)
    #     return all_days


    # read
    @classmethod
    def get_by_name(cls, name):
        query = "SELECT * FROM days WHERE name = %(name)s"
        results = connectToMySQL(DATABASE).query_db(query, {"name": name})
        return cls(results[0])

    # update
    @classmethod
    def update(cls, data):
        query = "UPDATE days SET name = %(name)s"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    # delete
    @classmethod
    def delete(cls, id):
        query = "DELETE FROM days where id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, {"id": id})


