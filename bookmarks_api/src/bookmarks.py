from flask import Blueprint, request, jsonify
import validators
from http import HTTPStatus
from src.database import Bookmark, db
from flask_jwt_extended import get_jwt_identity, jwt_required

bookmarks = Blueprint("bookmarks", __name__, url_prefix="/api/v1/bookmarks")


def parse_bookmark_to_dictionary(bookmark_obj) -> dict:
    """Parses a bookmark model object to a dictionary

    Args:
        bookmark_obj: a bookmark object returned from an SQLAlchemy query

    Returns:
        dict: dictionary with bookmark attributes
    """
    return {
        "id": bookmark_obj.id,
        "url": bookmark_obj.url,
        "short_url": bookmark_obj.short_url,
        "visits": bookmark_obj.visits,
        "body": bookmark_obj.body,
        "created_at": bookmark_obj.created_at,
        "updated_at": bookmark_obj.updated_at,
    }


@bookmarks.route("/", methods=["GET", "POST"])
@jwt_required
def bookmarks():

    current_user = get_jwt_identity()

    if request.method == "POST":
        body = request.json("body", "")
        url = request.json("url", "")

        if not validators.url(url):
            return jsonify(
                {
                    "error": "Invalid url",
                    "status": f"{HTTPStatus.BAD_REQUEST} {HTTPStatus.BAD_REQUEST.phrase}",
                }
            )

        if Bookmark.query.filter_by(url=url).first():
            return jsonify(
                {
                    "error": "URL already exists",
                    "status": f"{HTTPStatus.CONFLICT} {HTTPStatus.CONFLICT.phrase}",
                }
            )

        new_bookmark = Bookmark(url=url, body=body, user_id=current_user)

        db.session.add(new_bookmark)

        db.session.commit()

        return jsonify(
            {
                "message": "Bookmark added",
                "bookmark": {
                    "id": new_bookmark.id,
                    "url": new_bookmark.url,
                    "short_url": new_bookmark.short_url,
                    "visits": new_bookmark.visits,
                    "body": new_bookmark.body,
                    "created_at": new_bookmark.created_at,
                    "updated_at": new_bookmark.updated_at,
                },
                "status": f"{HTTPStatus.CREATED} {HTTPStatus.CREATED.phrase} ",
            }
        )

    else:

        bookmarks_query = Bookmark.query.filter_by(user_id=current_user)

        bookmarks = [
            parse_bookmark_to_dictionary(bookmark) for bookmark in bookmarks_query
        ]

        return jsonify(
            {"data": bookmarks, "status": f"{HTTPStatus.OK} {HTTPStatus.OK.phrase}"}
        )
