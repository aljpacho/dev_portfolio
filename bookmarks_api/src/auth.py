from http import HTTPStatus

import validators
from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from src.database import User, db

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post("/register")
def register():
    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]

    if len(username) < 4:
        return (
            jsonify({"Error": "Username is too short. Must be at least 5 characters."}),
            HTTPStatus.BAD_REQUEST.value,
            HTTPStatus.BAD_REQUEST.phrase,
        )

    if len(password) < 8:
        return (
            jsonify({"Error": "Password is too short"}),
            HTTPStatus.BAD_REQUEST.value,
            HTTPStatus.BAD_REQUEST.phrase,
        )

    if not username.isalnum():
        return (
            jsonify({"Error": "Username is not alphanumeric or contains whitespace"}),
            HTTPStatus.BAD_REQUEST.value,
            HTTPStatus.BAD_REQUEST.phrase,
        )

    if User.objects.filter_by(email=username).first() is not None:
        return (
            {"Error": "Username is taken"},
            HTTPStatus.CONFLICT.value,
            HTTPStatus.CONFLICT.phrase,
        )

    if not validators.email(email):
        return (
            jsonify({"Error": "Email is not valid"}),
            HTTPStatus.BAD_REQUEST.value,
            HTTPStatus.BAD_REQUEST.phrase,
        )

    if User.objects.filter_by(email=email).first() is not None:
        return (
            {"Error": "Email is taken"},
            HTTPStatus.CONFLICT.value,
            HTTPStatus.CONFLICT.phrase,
        )

    password_hash = generate_password_hash(password)

    new_user = User(username=username, password=password_hash, email=email)

    db.session.add(new_user)

    db.session.commit()

    return (
        jsonify(
            {"Message": "User Created", "User": {"Username": username, "Email": email}}
        ),
        HTTPStatus.CREATED.value,
        HTTPStatus.CREATED.phrase,
    )
