from http import HTTPStatus

import validators
from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from src.database import Users, db

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post("/register")
def register():
    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]

    if len(username) < 4:
        return jsonify(
            {
                "error": "Username is too short. Must be at least 5 characters.",
                "status": f"{HTTPStatus.BAD_REQUEST} {HTTPStatus.BAD_REQUEST.phrase}",
            }
        )

    if len(password) < 8:
        return jsonify(
            {
                "error": "Password is too short",
                "status": f"{HTTPStatus.BAD_REQUEST} {HTTPStatus.BAD_REQUEST.phrase}",
            }
        )

    if not username.isalnum():
        return jsonify(
            {
                "error": "Username is not alphanumeric or contains whitespace",
                "status": f"{HTTPStatus.BAD_REQUEST} {HTTPStatus.BAD_REQUEST.phrase}",
            }
        )

    if Users.query.filter_by(email=username).first() is not None:
        return jsonify(
            {
                "error": "Username is taken",
                "status": f"{HTTPStatus.CONFLICT} {HTTPStatus.CONFLICT.phrase}",
            }
        )

    if not validators.email(email):
        return jsonify(
            {
                "error": "Email is not valid",
                "status": f"{HTTPStatus.BAD_REQUEST} {HTTPStatus.BAD_REQUEST.phrase}",
            }
        )

    if Users.query.filter_by(email=email).first() is not None:
        return jsonify(
            {
                "error": "Email is taken",
                "status": f"{HTTPStatus.CONFLICT} {HTTPStatus.CONFLICT.phrase}",
            }
        )

    password_hash = generate_password_hash(password)

    new_user = Users(username=username, password=password_hash, email=email)

    db.session.add(new_user)

    db.session.commit()

    return jsonify(
        {
            "message": "User created",
            "user": {"username": username, "email": email},
            "status": f"{HTTPStatus.CREATED} {HTTPStatus.CREATED.phrase}",
        }
    )
