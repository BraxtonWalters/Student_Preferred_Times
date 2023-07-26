from flask_app import app
from flask import render_template, redirect, request, session

# landing
@app.route("/")
def landing():
    if "user_id" in session:
        return redirect("/dashboard")
    return render_template("login.html")