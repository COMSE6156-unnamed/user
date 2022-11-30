from flask import Blueprint, request, Response
from utils.exts import db
from utils.model import User
from utils.format import format_user
import json

bp = Blueprint("user", __name__, url_prefix="/user")

@bp.route("/all", methods=["GET"])
def get_all_users():
    if request.method == "GET":
        content = []
        for user in db.session.query(User).all():
            content.append(format_user(user))

        return Response(json.dumps(content), status=200, content_type="user.json")

@bp.route("/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id: int):
    if request.method == "GET":
        content = []
        for user in db.session.query(User).filter(User.user_id == user_id):
            print(user)
            content.append(format_user(user))

        return Response(json.dumps(content), status=200, content_type="user.json")
