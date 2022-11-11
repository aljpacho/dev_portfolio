import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import case, func, text

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODFICATIONS"] = False

CORS(app, origins=["http://127.0.0.1:8080"], supports_credentials=True)

db = SQLAlchemy(app)


# Setting up db model
class Story(db.Model):
    __tablename__ = "stories"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=datetime.now()
    )

    def __repr__(self):
        return "<Story %r>" % self.title


class Vote(db.Model):
    __tablename__ = "votes"
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey("stories.id"))
    direction = db.Column(db.String, nullable=False)

    def __repr__(self):
        return "Vote %r>" % self.id


def story_object_to_dictionary(story_objs: Story) -> dict:
    """Takes a Story object generated by the Story class
    and abstracts the attributes into a dictionary

    Args:
        story_obj (Story): Story object generated from Story class

    Returns:
        story_dict (dict): a dictionary pertaining key:value pairs
        for attributes
    """

    story_obj = story_objs[0]

    story_dict = {
        "id": story_obj.id,
        "title": story_obj.title,
        "url": story_obj.url,
        "created_at": story_obj.created_at,
        "score": story_objs[1],
    }

    return story_dict


def vote_object_to_dictionary(vote_obj: Vote) -> dict:
    """Takes a Vote object generated by the Vote class
    and abstracts the attributes into a dictionary

    Args:
        vote_obj (Vote): Vote object generated from the Vote class

    Returns:
        vote_dict (dict): a dictionary pertaining key:values pairs
        for attributes
    """
    vote_dict = {
        "id": vote_obj.id,
        "story_id": vote_obj.story_id,
        "direction": vote_obj.direction,
    }

    return vote_dict


@app.route("/testdb")
def testdb():
    try:
        db.session.query(text("1")).from_statement(text("SELECT 1")).all()
        return "<h1>It works.</h1>"
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = "<h1>Something is broken.</h1>"
        return hed + error_text


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stories", methods=["GET"])
def get_stories():

    story_objects = (
        db.session.query(
            Story,
            func.sum(
                case(
                    (Vote.direction == "up", 1), (Vote.direction == "down", -1), else_=0
                )
            ).label("score"),
        )
        .outerjoin(Vote, Vote.story_id == Story.id)
        .group_by(Story.id)
        .all()
    )

    """
    select stories.*,
        sum(case 
            when votes.direction = 'up' then 1
            when votes.direction = 'down' then -1
            else 0
        end) score

        from stories
        left join votes 
            on votes.story_id = stories.id

        group by stories.id;
    """

    stories_list = [story_object_to_dictionary(story) for story in story_objects]

    return jsonify(
        {"stories": stories_list, "success": True, "total_stories": len(stories_list)}
    )


@app.route("/stories/<id>", methods=["GET"])
def get_story_by_id(id):

    story_object = (
        db.session.query(
            Story,
            func.sum(
                case(
                    (Vote.direction == "up", 1), (Vote.direction == "down", -1), else_=0
                )
            ).label("score"),
        )
        .filter(Story.id == id)
        .outerjoin(Vote, Vote.story_id == Story.id)
        .group_by(Story.id)
        .all()
    )

    story_dictionary = story_object_to_dictionary(story_object[0])

    return jsonify({"story": story_dictionary, "success": True})


@app.route("/stories/<id>/votes", methods=["POST"])
def add_vote(id):
    if request.method == "POST":
        vote_direction = request.json.get("direction")  # either up or down

        vote = Vote(story_id=id, direction=vote_direction)

        db.session.add(vote)

    db.session.commit()

    return jsonify({"response": "vote added", "success": True})


if __name__ == "__main__":
    app.run(debug=True)
