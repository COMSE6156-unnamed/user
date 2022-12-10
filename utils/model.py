
from utils.exts import db
import utils.db as db_util
import utils.constants as constants
from sqlalchemy import text, exc
import pymysql
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String)
    user_email = db.Column(db.String)
    picture = db.Column(db.String)

    def __init__(self, user_id, user_name, user_email, picture):
        self.user_id = user_id
        self.user_name = user_name
        self.user_email = user_email
        self.picture = picture
        self.id = user_id # for flask login

    def get(user_id):
        engine = db_util.create_db_engine()
        with engine.connect() as connection:
            user = connection.execute(text(constants.SQL_GET_USER_BY_ID.format(str(user_id)))
            ).fetchone()
            if not user:
                return None
            user = User(
                user_id=user[0], user_name=user[1], user_email=user[2], picture=user[3]
            )
            return user

def check_registration(engine, userinfo_json):
    user_id = userinfo_json[constants.GOOGLE_ID_KEY]
    user_email = userinfo_json[constants.GOOGLE_EMAIL_KEY]
    user_name = userinfo_json[constants.GOOGLE_NAME_KEY]
    picture = userinfo_json[constants.GOOGLE_PICTURE_KEY]
    
    with engine.connect() as connection:
        result = connection.execute(text(constants.SQL_COUNT_USER_QUERY.format(str(user_id))))
        result_as_dict = result.mappings().all()
        if len(result_as_dict) == 1 and result_as_dict[0][constants.SQL_ROW_COUNT_KEY] == 0:
            new_user = User(user_id=user_id, user_name=user_name, user_email=user_email, picture=picture)
            db.session.add(new_user)
            try:
                db.session.commit()
            except pymysql.err.IntegrityError as e:
                db.session.rollback()
            except exc.IntegrityError as e:
                db.session.rollback()
            except Exception as e:
                db.session.rollback()