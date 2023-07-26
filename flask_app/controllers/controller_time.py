from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.model_user import User
from flask_app.models.model_day import Day
from flask_app.models.model_time import Time

@app.route("/time/create/<int:id>")
def time_create(id):
    weekday = Day.get_all_times({"id": id})
    user = User.get_by_id({"id": session["user_id"]})
    return render_template("create_time.html", user=user, weekday=weekday)

@app.route("/time/create/add", methods=["POST"])
def time_create_add():
    data = {**request.form}
    Time.create(data)
    return redirect(f"/time/create/{request.form['day_id']}")

@app.route("/time/edit/<int:id>")
def time_edit(id):
    time_slot = Time.get_by_id(id)
    user = User.get_by_id({"id": session["user_id"]})
    return render_template("edit_time.html", time_slot=time_slot, user=user)

@app.route("/time/update/<int:id>", methods=["POST"])
def time_update(id):
    data = {**request.form}
    Time.update(data)
    return redirect("/")


@app.route("/time/delete/<int:id>")
def time_delete(id):
    time_slot = Time.get_by_id(id)
    Time.delete(id)
    return redirect(f"/time/create/{time_slot.day_id}")


