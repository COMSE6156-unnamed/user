import os
from dotenv import load_dotenv
from flask_dance.contrib.google import make_google_blueprint, google
from flask import redirect, url_for, jsonify, session
from oauthlib.oauth2.rfc6749.errors import TokenExpiredError
from sqlalchemy import text, exc
import pymysql
from utils.exts import db
from utils.model import User
import utils.constants as constants

# load environment variables from .env
load_dotenv()

# google oauth credentials & settings
client_id = os.getenv(constants.GOOGLE_CLIENT_ID_KEY)
client_secret = os.getenv(constants.GOOGLE_CLIENT_SECRET_KEY)
os.environ[constants.OAUTHLIB_INSECURE_TRANSPORT_KEY] = '1'
os.environ[constants.OAUTHLIB_RELAX_TOKEN_SCOPE_KEY] = '1'

bp = make_google_blueprint(
    client_id=client_id,
    client_secret=client_secret,
    reprompt_consent=True,
    scope=[constants.BLUE_PRINT_SCOPE_PROFILE,
        constants.BLUE_PRINT_SCOPE_EMAIL],
    redirect_url="http://127.0.0.1:8080",
    redirect_to="http://127.0.0.1:5000"
)

def set_secret_key(app):
    app.secret_key = os.getenv(constants.SECRETKEY_KEY)

@bp.route("/", methods=['GET', 'POST'])
def index():
    try:
        if not google.authorized:
            return redirect(url_for(constants.GOOGLE_LOGIN))
        
    except TokenExpiredError as e:
        return redirect(url_for(constants.GOOGLE_LOGIN))

    return redirect("/")

def check_registration(engine, data):
    user_id = data[constants.GOOGLE_ID_KEY]
    user_email = data[constants.GOOGLE_EMAIL_KEY]
    user_name = data[constants.GOOGLE_NAME_KEY]

    with engine.connect() as connection:
        result = connection.execute(text(constants.SQL_COUNT_USER_QUERY.format(str(user_id))))
        result_as_dict = result.mappings().all()
        if len(result_as_dict) == 1 and result_as_dict[0][constants.SQL_ROW_COUNT_KEY] == 0:
            new_user = User(user_id=int(user_id), user_name=str(user_name), user_email=str(user_email))
            db.session.add(new_user)
            try:
                db.session.commit()
            except pymysql.err.IntegrityError as e:
                db.session.rollback()
            except exc.IntegrityError as e:
                db.session.rollback()
            except Exception as e:
                db.session.rollback()
