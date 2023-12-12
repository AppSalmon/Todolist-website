from flask_login import UserMixin
from todolist import db
from sqlalchemy.sql import func
from enum import unique
from datetime import timezone

class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone = True), default = func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(200), unique = True)
    password = db.Column(db.String(200))
    user_name = db.Column(db.String(200))
    notes = db.relationship("Note")

    def __init__(self, email, password, user_name):
        self.email = email
        self.password = password
        self.user_name = user_name