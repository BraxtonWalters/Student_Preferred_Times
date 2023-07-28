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
    
    @classmethod
    def get_schedule(cls):
        query = """
                SELECT 
                    days.*,
                    times.*,
                    ths.*
                FROM 
                    days
                JOIN
                    times ON days.id = times.day_id
                LEFT JOIN 
                    (
                    SELECT 
                        times_has_students.time_id,
                        times_has_students.student_id,
                        students.*
                    FROM
                        times_has_students
                    LEFT JOIN 
                        students ON times_has_students.student_id = students.id
                    ) AS ths ON ths.time_id = times.id;
                """
        results = connectToMySQL(DATABASE).query_db(query)
        print(results)
        week_schedule = {"mon": {},
                         "tues": {},
                         "wed" : {},
                         "thur": {},
                         "fri": {}}
        # each index should contain a list of time objects
        # every time object needs a list of student objects
        # if there are no student for that time slot then we want an empty list
        for row in results:
            time_slot = row["start_time"] + "-" + row["end_time"]
            student = {
                "id": row["student_id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"]
            }
            if row["name"] == "monday":
                if time_slot not in week_schedule["mon"]:
                    week_schedule["mon"][time_slot] = [student]
                else:
                    week_schedule["mon"][time_slot].append(student)

            elif row["name"] == "tuesday":
                if time_slot not in week_schedule["tues"]:
                    week_schedule["tues"][time_slot] = [student]
                else:
                    week_schedule["tues"][time_slot].append(student)

            elif row["name"] == "wednesday":
                if time_slot not in week_schedule["wed"]:
                    week_schedule["wed"][time_slot] = [student]
                else:
                    week_schedule["wed"][time_slot].append(student)

            elif row["name"] == "thursday":
                if time_slot not in week_schedule["thur"]:
                    week_schedule["thur"][time_slot] = [student]
                else:
                    week_schedule["thur"][time_slot].append(student)

            else:
                if time_slot not in week_schedule["fri"]:
                    week_schedule["fri"][time_slot] = [student]
                else:
                    week_schedule["fri"][time_slot].append(student)
        print(week_schedule)
        return week_schedule
    
    @classmethod
    def get_schedule2(cls):
        query = """
                SELECT 
                    days.*,
                    times.*,
                    ths.*
                FROM 
                    days
                JOIN
                    times ON days.id = times.day_id
                LEFT JOIN 
                    (
                    SELECT 
                        times_has_students.time_id,
                        times_has_students.student_id,
                        students.*
                    FROM
                        times_has_students
                    LEFT JOIN 
                        students ON times_has_students.student_id = students.id
                    ) AS ths ON ths.time_id = times.id;
                """
        results = connectToMySQL(DATABASE).query_db(query)
        week_schedule = []
        # each index should contain a list of time objects
        # every time object needs a list of student objects
        # if there are no student for that time slot then we want an empty list
        for row in results:
            time_slot = row["start_time"] + "-" + row["end_time"]
            student = {
                "id": row["student_id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
            }
            if row["name"] == "monday":
                if time_slot not in week_schedule["mon"]:
                    week_schedule["mon"][time_slot] = [student]
                else:
                    week_schedule["mon"][time_slot].append(student)
            elif row["name"] == "tuesday":
                if time_slot not in week_schedule["mon"]:
                    week_schedule["mon"][time_slot] = [student]
                else:
                    week_schedule["mon"][time_slot].append(student)
            elif row["name"] == "wednesday":
                if time_slot not in week_schedule["mon"]:
                    week_schedule["mon"][time_slot] = [student]
                else:
                    week_schedule["mon"][time_slot].append(student)
            elif row["name"] == "thursday":
                if time_slot not in week_schedule["mon"]:
                    week_schedule["mon"][time_slot] = [student]
                else:
                    week_schedule["mon"][time_slot].append(student)
            else:
                if time_slot not in week_schedule["mon"]:
                    week_schedule["mon"][time_slot] = [student]
                else:
                    week_schedule["mon"][time_slot].append(student)
        return week_schedule
    
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


