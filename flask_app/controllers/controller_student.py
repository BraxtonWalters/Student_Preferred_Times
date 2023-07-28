from flask_app import app, bcrypt
from flask import render_template, redirect, request, session
from flask_app.models.model_student import Student
from flask_app.models.model_day import Day

@app.route("/student/create/")
def student_create():
    if "student_id" in session:
        return redirect("/student/thankyou")
    return render_template("create_student.html")

@app.route("/student/add", methods=["POST"])
def student_add():
    if not Student.student_validator(request.form):
        return redirect("/student/create/")
    password_hash = bcrypt.generate_password_hash(request.form["password"])
    data = {**request.form}
    data["password"] = password_hash
    student_id = Student.create(data)
    session["student_id"] = student_id
    return redirect("/student/time/slots")

@app.route("/student/time/slots")
def student_time_slots():
   if "student_id" not in session:
       return redirect("/student/create/")
   all_days = Day.get_all_days()
   user = Student.get_by_id({"id": session["student_id"]})
   return render_template("student_time_selector.html", all_days=all_days, user=user)

@app.route("/student/times", methods=["POST"])
def student_times():
    data = {**request.form}
    user = Student.get_by_id({"id": session["student_id"]})
    time_data = {}
    for key in data:
        time_data["time_id"] = int(key)
        time_data["student_id"] = user.id
        Student.time_has_students(time_data)
    return redirect("/student/thankyou")

@app.route("/student/thankyou")
def student_thankyou():
    if "student_id" not in session:
        return redirect("/student/create/")
    user = Student.get_by_id({"id": session["student_id"]})
    session.pop("student_id")
    return render_template("student_thankyou.html", user=user)
