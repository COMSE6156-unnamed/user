from crypt import methods
from flask import Blueprint, request, Response, jsonify
from utils.exts import db
from utils.model import User
import json
from sqlalchemy import create_engine, text

bp = Blueprint("user", __name__, url_prefix="/user")

@bp.route("/all", methods=["GET"])
def get_all_users():
    if request.method == "GET":
        #content = []
        #print('db: ', db)
        #print('db session: ', db.session)
        #print('db session query: ', db.session.query(User))
        #for user in db.session.query(User):
        #    content.append(user)
        #return Response(json.dumps(content), status=200, content_type="user.json")
        engine = create_engine('mysql+pymysql://admin:dbuserdbuser@e6156.ccgom5f9kwrf.us-east-1.rds.amazonaws.com:3306/user_db')
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
        #content = {}
        #cur_user = db.session.query(User).filter(User.user_id == user_id)
        #content[user_id] = {
        #    "user_id": cur_user.user_id,
        #    "user_name": cur_user.user_name
        #}
        #return Response(json.dumps(content), status=200, content_type="user.json")
        engine = create_engine('mysql+pymysql://admin:dbuserdbuser@e6156.ccgom5f9kwrf.us-east-1.rds.amazonaws.com:3306/user_db')
        result = ''
        with engine.connect() as connection:
            result = connection.execute(text("select user_id, user_name from user where user_id = {}".format(str(user_id))))
            print("select user_id, user_name from user where user_id = {}".format(str(user_id)))
            result = [dict(row._mapping) for row in result]
        return Response(json.dumps(result), status=200, content_type="user.json")
