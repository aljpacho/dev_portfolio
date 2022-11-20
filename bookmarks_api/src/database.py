import random
import string
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
    bookmarks = db.relationship("Bookmark", backref="user")

    def __repr__(self):
        return f"User: {self.username}"


class Bookmark(db.Model):
    id = db.column(db.Integer, primary_key=True)
    body = db.column(db.Text, nullable=True)
    url = db.column(db.Text, nullable=False)
    short_url = db.column(db.String(3), nullable=True)
    visits = db.column(db.Integer, default=0)
    created_at = db.column(db.DateTime, default=datetime.now())
    updated_at = db.column(db.Datetime, onupdate=datetime.now())
    user_id = db.column(db.Integer, db.ForeignKey("user.id"))

    def generate_short_id(self, num_of_chars=3) -> str:
        """Generates a short ID using all digits and ASCII letters
        Args:
            num_of_chars (int): Number of characters in the ID Defaults to 3.

        Returns:
            str: random characters if they don't already exist in the database
        """
        characters = string.digits + string.ascii_letters
        random_chars = "".join(random.choices(characters, k=num_of_chars))

        short_id_exists = self.query.filter_by(short_url=random_chars).first()

        if short_id_exists:
            self.generate_short_id()
        else:
            return random_chars

    def __repr__(self):
        return f"Bookmark: {self.url}"
