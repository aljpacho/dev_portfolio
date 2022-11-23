from http import HTTPStatus

import validators
from flask import Blueprint, jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, jwt_required)
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


@auth.post("/login")
def login():
    email = request.json.get("email", "")
    password = request.json.get("password", "")

    user = Users.query.filter_by(email=email).first()

    if user:
        valid_password = check_password_hash(user.password, password)

        if valid_password:
            refresh_token = create_refresh_token(identity=user.id)
            access_token = create_access_token(identity=user.id)

            return jsonify(
                {
                    "user": {
                        "refresh-token": refresh_token,
                        "access-token": access_token,
                        "username": user.username,
                        "email": user.email,
                    },
                    "status": f"{HTTPStatus.OK} {HTTPStatus.OK.phrase}",
                }
            )

    return jsonify(
        {
            "error": "Wrong credentials",
            "status": f"{HTTPStatus.UNAUTHORIZED} {HTTPStatus.UNAUTHORIZED.phrase}",
        }
    )


@auth.get("/token/refresh")
@jwt_required(refresh=True)
def refresh_users_token():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)

    return jsonify(
        {
            "access-token": access_token,
            "status": f"{HTTPStatus.OK} {HTTPStatus.OK.phrase}",
        }
    )
