from http import HTTPStatus

import validators
from flasgger import swag_from
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.database import Bookmark, db

_bookmarks = Blueprint("_bookmarks", __name__, url_prefix="/api/v1/bookmarks")


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


def parse_meta_from_bookmarks(bookmarks_obj) -> dict:
    """Parses the pagination attributes from a bookmark query

    Args:
        bookmarks_obj: a Flask-SQLAlchemy pagination object

    Returns:
        dict: dictionary with pagination attributes
    """
    return {
        "page": bookmarks_obj.page,
        "pages": bookmarks_obj.pages,
        "total_count": bookmarks_obj.total,
        "prev_page": bookmarks_obj.prev_num,
        "next_page": bookmarks_obj.next_num,
        "has_next": bookmarks_obj.has_next,
        "has_prev": bookmarks_obj.next_num,
    }


def parse_stats_from_bookmark(bookmark_obj) -> dict:
    """Parse bookmark statistics for bookmark object: id, visits,
    url, and short url

    Args:
        bookmark_obj: a bookmark object return from SQLAlchemy model

    Returns:
        dict: dictionary with attributes for statistics
    """
    return {
        "id": bookmark_obj.id,
        "visits": bookmark_obj.visits,
        "url": bookmark_obj.url,
        "short_url": bookmark_obj.short_url,
    }


@_bookmarks.route("/", methods=["GET", "POST"])
@jwt_required()
@swag_from("./docs/bookmarks/bookmarks_get.yml", methods=["GET"])
@swag_from("./docs/bookmarks/bookmarks_post.yml", methods=["POST"])
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


@_bookmarks.get("/<int:id>")
@jwt_required()
@swag_from("./docs/bookmarks/bookmark_by_id.yml")
def get_bookmark(id):
    current_user = get_jwt_identity()

    bookmark_query = Bookmark.query.filter_by(user_id=current_user, id=id).first()

    if not bookmark_query:
        return jsonify(
            {
                "message": "Item not found",
                "status": f"{HTTPStatus.NOT_FOUND} {HTTPStatus.NOT_FOUND.phrase}",
            }
        )

    bookmark = parse_bookmark_to_dictionary(bookmark_query)

    return jsonify(
        {"data": bookmark, "status": f"{HTTPStatus.OK} {HTTPStatus.OK.phrase}"}
    )


@_bookmarks.put("/<int:id>")
@_bookmarks.patch("/<int:id>")
@jwt_required()
@swag_from("./docs/bookmarks/bookmark_id_patch.yml")
def update_bookmark(id):
    current_user = get_jwt_identity()

    bookmark_query = Bookmark.query.filter_by(user_id=current_user, id=id).first()

    if not bookmark_query:
        return jsonify(
            {
                "message": "Item not found",
                "status": f"{HTTPStatus.NOT_FOUND} {HTTPStatus.NOT_FOUND.phrase}",
            }
        )

    body = request.json.get("body", "")
    url = request.json.get("url", "")

    if not validators.url(url):
        return jsonify(
            {
                "error": "Invalid url",
                "status": f"{HTTPStatus.BAD_REQUEST} {HTTPStatus.BAD_REQUEST.phrase}",
            }
        )

    bookmark_query.url = url
    bookmark_query.body = body

    db.session.commit()

    bookmark = parse_bookmark_to_dictionary(bookmark_query)

    return jsonify(
        {
            "message": "Updated item",
            "data": bookmark,
            "status": f"{HTTPStatus.OK} {HTTPStatus.OK.phrase}",
        }
    )


@_bookmarks.delete("/<int:id>")
@jwt_required()
@swag_from("./docs/bookmarks/bookmark_id_delete.yml")
def delete_bookmark(id):
    current_user = get_jwt_identity()

    bookmark_query = Bookmark.query.filter_by(user_id=current_user, id=id).first()

    if not bookmark_query:
        return jsonify(
            {
                "message": "Item not found",
                "status": f"{HTTPStatus.NOT_FOUND} {HTTPStatus.NOT_FOUND.phrase}",
            }
        )

    db.session.delete(bookmark_query)
    db.session.commit()

    return jsonify(
        {
            "message": "Item deleted",
            "status": f"{HTTPStatus.ACCEPTED} {HTTPStatus.ACCEPTED.phrase}",
        }
    )


@_bookmarks.get("/statistics")
@jwt_required()
@swag_from("./docs/bookmarks/statistics.yml")
def get_statistics():
    current_user = get_jwt_identity()

    bookmarks_query = Bookmark.query.filter_by(user_id=current_user).all()

    statistics = [parse_stats_from_bookmark(bookmark) for bookmark in bookmarks_query]

    return jsonify(
        {"data": statistics, "status": f"{HTTPStatus.OK} {HTTPStatus.OK.phrase}"}
    )
