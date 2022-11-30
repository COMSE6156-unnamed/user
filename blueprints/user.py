from crypt import methods
from flask import Blueprint, request, Response, jsonify
from utils.exts import db
from config import create_db_engine
import json
from sqlalchemy import text
from utils.model import User
from utils.format import format_user

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
        # """
        # input: user_id,
        # output: {
        #     user_id: "",
        #     user_name: ""
        # }
        # """
        # engine = create_db_engine()
        # result = ''
        # with engine.connect() as connection:
        #     result = connection.execute(text("select user_id, user_name from user where user_id = {}".format(str(user_id))))
        #     print("select user_id, user_name from user where user_id = {}".format(str(user_id)))
        #     result = [dict(row._mapping) for row in result]
        content = []
        user = db.session.query(User).filter(User.user_id == user_id)
        content.append(format_user(user))

        return Response(json.dumps(content), status=200, content_type="user.json")
