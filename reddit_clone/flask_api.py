from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


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
    app.run()
