from crypt import methods
from flask import Blueprint, request, Response
from utils.exts import db
from utils.model import User
import json

bp = Blueprint("user", __name__, url_prefix="/user")

@bp.route("/<int:user_id", methods=["GET"])
def get_user_by_id(user_id: int):
    if request.method == "GET":
        """
        input: user_id,
        output: {
            user_id: "",
            user_name: ""
        }
        """
        content = {}
        cur_user = db.session.query(User).filter(User.user_id == user_id)
        content[user_id] = {
            "user_id": cur_user.user_id,
            "user_name": cur_user.user_name
        }
        return Response(json.dumps(content), status=200, content_type="user.json")