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


def parse_meta_from_bookmarks(bookmarks) -> dict:
    """Parses the pagination attributes from a bookmark query

    Args:
        bookmarks: a Flask-SQLAlchemy pagination object

    Returns:
        dict: dictionary with pagination attributes
    """
    return {
        "page": bookmarks.page,
        "pages": bookmarks.pages,
        "total_count": bookmarks.total,
        "prev_page": bookmarks.prev_num,
        "next_page": bookmarks.next_num,
        "has_next": bookmarks.has_next,
        "has_prev": bookmarks.next_num,
    }


@bookmarks.route("/", methods=["GET", "POST"])
@jwt_required()
def bookmarks_handler():

    current_user = get_jwt_identity()

    if request.method == "POST":
        body = request.json.get("body", "")
        url = request.json.get("url", "")

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
        # page variables for pagination
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)

        bookmarks_query = Bookmark.query.filter_by(user_id=current_user).paginate(
            page=page, per_page=per_page
        )

        bookmarks = [
            parse_bookmark_to_dictionary(bookmark) for bookmark in bookmarks_query.items
        ]

        meta_pagination = parse_meta_from_bookmarks(bookmarks_query)

        return jsonify(
            {
                "data": bookmarks,
                "meta": meta_pagination,
                "status": f"{HTTPStatus.OK} {HTTPStatus.OK.phrase}",
            }
        )
