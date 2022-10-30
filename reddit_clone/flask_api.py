from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from datetime import datetime
from sqlalchemy.sql import text

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODFICATIONS'] = True

db = SQLAlchemy(app)


# Setting up db model
class Story(db.Model):
    __tablename__ = "stories"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return self.title

        

def parse_story_to_dictionary(story_obj: Story) -> dict:
    """Takes a Story object of generated by the Story class
    and abstracts the attributes into a dictionary

    Args:
        story_obj (Story): Story object generated from Story class

    Returns:
        story_dict (dict): a dictionary pertaining key:value pairs
        for attributes
    """
    story_dict =  {
        'id': story_obj.id,
        'title': story_obj.title,
        'url': story_obj.url,
        'created_at': story_obj.created_at,
        'updated_at': story_obj.updated_at
    }

    return story_dict


@app.route("/testdb")
def testdb():
    try:
        db.session.query(text('1')).from_statement(text('SELECT 1')).all()
        return '<h1>It works.</h1>'
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

@app.route("/")
def home():
    return "Flask Reddit Clone"


@app.route("/stories")
def get_stories():
    story_objects = db.session.query(Story).all()
    
    stories = [parse_story_to_dictionary(story) for story in story_objects]

    return jsonify({"stories": (stories), "success": True, "total_stories": len(stories)})


@app.route("/stories/<story_id>")
def get_story_by_story_id():
    pass


if __name__ == "__main__":
    app.run(debug=True)
