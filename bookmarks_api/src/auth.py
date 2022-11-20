from http import HTTPStatus

from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post("/register")
def register():
    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]

    if len(password) < 8:
        return (
            jsonify({"error": "Password is too short"}),
            HTTPStatus.BAD_REQUEST.value,
            HTTPStatus.BAD_REQUEST.phrase,
        )
    

    return "User created"
