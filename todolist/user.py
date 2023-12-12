from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from todolist.models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from todolist import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import timedelta

user = Blueprint("user", __name__)
user.permanent_session_lifetime = timedelta(minutes = 1)
@user.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                session.permanent = True
                login_user(user, remember = True)
                flash("Logged is sucess!", category = "sucess")
                return redirect(url_for("views.home"))
            else:
                flash("Wrong password!", category = "error")
        else:
            flash("Wrong email or user not exist!", category = "error")

    return render_template("login.html", user = current_user)

@user.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == 'POST':
        email = request.form.get("email")
        user_name = request.form.get("user_name")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        user = User.query.filter_by(email = email).first()
        if user:
            flash("User existsed!", category = "error")
        elif len(email) < 4:
            flash("Email must > 4 characters", category = "error")
        elif len(password) < 7:
            flash("Password must 7 characters", category = "error")
        elif password != confirm_password:
            flash("Password not match with confirm password!", category = "error")
        else:
            password = generate_password_hash(password, method = "sha256")
            new_user = User(email, password, user_name)
            try:
                db.session.add(new_user)
                db.session.commit()
                
                flash("User created!", category = "sucess")
                login_user(user, remember = True)
                return redirect(url_for("views.home"))
            except:
                flash("Error!", category = "error")

    return render_template("signup.html", user = current_user)

@user.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("user.login"))