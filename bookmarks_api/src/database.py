import random
import string
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    bookmarks = db.relationship("Bookmark", backref="user")

    def __repr__(self):
        return f"User: {self.username}"


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=True)
    url = db.Column(db.Text, nullable=False)
    short_url = db.Column(db.String(3), nullable=True)
    visits = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

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
