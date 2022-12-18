from flask import Blueprint, request, Response
from utils.exts import db
from utils.model import User
from utils.format import format_user
import json

bp = Blueprint("user", __name__, url_prefix="/user")

@bp.route("/", methods=["GET"])
def get_all_users():
    if request.method == "GET":
        content = []
        for user in db.session.query(User).all():
            content.append(format_user(user))

        return Response(json.dumps(content), status=200, content_type="user.json")

@bp.route("/<user_id>", methods=["GET"])
def get_user_by_id(user_id):
    if request.method == "GET":
        content = []
        for user in db.session.query(User).filter(User.user_id == user_id):
            content.append(format_user(user))

        return Response(json.dumps(content), status=200, content_type="user.json")

@bp.route("/<user_id>/increment_dog_num", methods=["PUT"])
def increment_user_dog_num(user_id):
    if request.method=="PUT":
        content = []
        for user in db.session.query(User).filter(User.user_id == user_id):
            user.dog_num = user.dog_num + 1
            content.append(format_user(user))
            db.session.commit()
        return Response(json.dumps(content), status=200, content_type="user.json")