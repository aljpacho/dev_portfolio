import os

from flask import Flask, redirect, jsonify
from flask_jwt_extended import JWTManager
from http import HTTPStatus

from src.auth import auth
from src.bookmarks import bookmarks
from src.database import Bookmark, db


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("BOOKMARKS_DEV_SK"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("BOOKMARKS_DB_URI"),
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
        )
    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)

    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)

    @app.get("/<short_url>")
    def redirect_to_url(short_url):
        bookmark_query = Bookmark.query.filter_by(short_url=short_url).first_or_404()

        if bookmark_query:
            bookmark_query.visits = bookmark_query.visits + 1
            db.session.commit()
            return redirect(bookmark_query.url)

    @app.errorhandler(HTTPStatus.NOT_FOUND)
    def handle_not_found_error(e):
        return jsonify(
            {"error": f"{HTTPStatus.NOT_FOUND} {HTTPStatus.NOT_FOUND.phrase}"}
        )

    @app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
    def handle_internal_server_error(e):
        return jsonify(
            {
                "error": f"{HTTPStatus.INTERNAL_SERVER_ERROR} {HTTPStatus.INTERNAL_SERVER_ERROR.phrase}"
            }
        )

    return app
