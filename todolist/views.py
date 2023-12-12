from flask import Blueprint, render_template, flash, request, jsonify, session
from flask_login import current_user, login_required
from sqlalchemy.sql.functions import user
from todolist.models import Note
from todolist import db
import json

views = Blueprint("views", __name__)

@views.route("/", methods = ["POST", "GET"])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get("note")
        if len(note) < 1:
            flash("Too short!", category = "error")
        else:
            new_note = Note(data = note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added!", category = "success")
    session.permanent = True
    return render_template("index.html", user = current_user)

@views.route("/delete-note", methods = ["GET", "POST"])
def delete_note():
    note = json.loads(request.data)
    note_id = note["note_id"]
    result = Note.query.get(note_id)
    if result:
        if result.user_id == current_user.id:
            db.session.delete(result)
            db.session.commit()
    return jsonify({"code":200})
