from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.column(db.Integer, primary_key=True)
    username = db.column(db.String(80), unique=True, nullable=False)
    email = db.column(db.String(120), unique=True, nullable=False)
    password = db.column(db.Text, nullable=False)
    created_at = db.column(db.DateTime, default=datetime.now())
    updated_at = db.column(db.Datetime, onupdate=datetime.now())


    def __repr__(self):
        return f'User: {self.username}'

class Bookmark(db.Model):
    id = db.column(db.Integer, primary_key=True)
    body = db.column(db.Text, nullable=True)
    url  = db. column(db.Text, nullable=False)
    short_url = db.column(db.String(3), nullable=True)
    visits = db.column(db.Integer, default=0)
    created_at = db.column(db.DateTime, default=datetime.now())
    updated_at = db.column(db.Datetime, onupdate=datetime.now())
    user_id = db.column(db.Integer, db.ForeignKey('user.id'))