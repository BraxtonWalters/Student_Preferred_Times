from flask_app import app, bcrypt
from flask import render_template, redirect, request, session
from flask_app.models.model_user import User
from flask_app.models.model_time import Time
from flask_app.models.model_day import Day

@app.route("/user/create/display")
def user_display():
    return render_template("create_account.html")

@app.route("/user/create", methods=["POST"])
def user_create():
    if not User.register_validator(request.form):
        return redirect("/user/create/display")
    password_hash = bcrypt.generate_password_hash(request.form["password"])
    data = {**request.form}
    data["password"] = password_hash
    user_id = User.create(data)
    session["user_id"] = user_id
    return redirect("/dashboard")

@app.route("/user/login", methods=["POST"])
def user_login():
    if not User.login_validator(request.form):
        return redirect("/")
    user = User.get_by_email(request.form)
    session["user_id"] = user.id
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    user = User.get_by_id({"id": session["user_id"]})
    all_days = Day.get_all_days()
    testy_boy = Day.get_schedule()
    return render_template("dashboard.html", user=user, all_days=all_days, testy_boy=testy_boy)

@app.route("/user/logout")
def logout():
    session.clear()
    return redirect("/")