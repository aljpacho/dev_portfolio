from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")

db = SQLAlchemy()

# Setting up db model 
class story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    url = db.Columnn(db.String, nullable=False)
    created_at = db.Column(db.Datetime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.Datetime, nullable=False, default=datetime.now())

    def __repr__(self):
        return self.title



@app.route("/")
def get_home_page():
    return "<h1>Flask Reddit Clone</h1>"


@app.route("/stories")
def get_stories():
    pass


@app.route("/stories/<story_id>")
def get_story_by_story_id():
    pass


if __name__ == "__main__":
    app.run(debug=True)
