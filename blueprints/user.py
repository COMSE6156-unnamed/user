from crypt import methods
from flask import Blueprint, request, Response, jsonify
from utils.exts import db
from config import SQLALCHEMY_DATABASE_URI
import json
from sqlalchemy import create_engine, text

bp = Blueprint("user", __name__, url_prefix="/user")

@bp.route("/all", methods=["GET"])
def get_all_users():
    if request.method == "GET":
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        result = ''
        with engine.connect() as connection:
            result = connection.execute(text("select user.user_id, user.user_name from user"))
            result = [dict(row._mapping) for row in result]
        return Response(json.dumps(result), status=200, content_type="user.json")

@bp.route("/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id: int):
    if request.method == "GET":
        """
        input: user_id,
        output: {
            user_id: "",
            user_name: ""
        }
        """
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        result = ''
        with engine.connect() as connection:
            result = connection.execute(text("select user_id, user_name from user where user_id = {}".format(str(user_id))))
            print("select user_id, user_name from user where user_id = {}".format(str(user_id)))
            result = [dict(row._mapping) for row in result]
        return Response(json.dumps(result), status=200, content_type="user.json")
