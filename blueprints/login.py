import os
from dotenv import load_dotenv
from flask_dance.contrib.google import make_google_blueprint, google
from flask import Flask, render_template, redirect, url_for
from oauthlib.oauth2.rfc6749.errors import TokenExpiredError
from config import create_db_engine
from sqlalchemy import text
from utils.exts import db
from utils.model import User

# load environment variables from .env
load_dotenv()

# google oauth credentials & settings
client_id = os.getenv('GOOGLE_CLIENT_ID')
client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

bp = make_google_blueprint(
    client_id=client_id,
    client_secret=client_secret,
    reprompt_consent=True,
    scope=["profile", "email"]
)

def set_secret_key(app):
    app.secret_key = os.getenv('secret_key')

@bp.route('/', methods=['GET', 'POST'])
def index():
    google_data = None
    user_info_endpoint = '/oauth2/v2/userinfo'
    if google.authorized:
        try:
            google_data = google.get(user_info_endpoint).json()

            engine = create_db_engine()
            check_registration(engine=engine, data=google_data)

        except TokenExpiredError as e:
            return redirect(url_for("google.login"))
    else:
        return redirect(url_for('google.login'))

    return render_template('index.j2',
                           google_data=google_data,
                           fetch_url=google.base_url + user_info_endpoint)

def check_registration(engine, data):
    user_id = data['id']
    user_email = data['email']
    user_name = data['name']
    # with engine.connect() as connection:
    #     result = connection.execute(text("select count(*) from user where user_id = {}".format(str(user_id))))
    #     if len(result) == 0:
    #         db_session = db.session.query(User)
    #         new_user = User(user_id=int(user_id), user_name=str(user_name), user_email=str(user_email))

    #         db_session.add(new_user)
    #         db_session.commit()

    db_session = db.session.query(User)
    exists = db_session.filter_by(user_id=int(user_id)).first() is not None
    if not exists:
        new_user = User(user_id=int(user_id), user_name=str(user_name), user_email=str(user_email))
        db_session.add(new_user)
        db_session.commit()
