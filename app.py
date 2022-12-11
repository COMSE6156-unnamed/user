import json
import os
import requests
from oauthlib.oauth2 import WebApplicationClient
from flask import Flask, redirect, request, session, jsonify
from flask_migrate import Migrate
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_cors import CORS

# Internal imports
from utils.exts import db
from utils.model import User
from utils.model import check_registration
from blueprints import user_bp
from config import create_db_engine
import utils.constants as constants
import config

# load_dotenv() Will not be using load_dotenv() environment variable will be set in EC2
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

# oauth config
GOOGLE_CLIENT_ID = os.environ.get(constants.GOOGLE_CLIENT_ID_KEY)
GOOGLE_CLIENT_SECRET = os.environ.get(constants.GOOGLE_CLIENT_SECRET_KEY)
GOOGLE_DISCOVERY_URL = (
    os.environ.get(constants.GOOGLE_DISCOVERY_URL_KEY)
)

# frontend config
FRONTEND_ENDPOINT = os.environ.get(constants.FRONTEND_ENDPOINT_KEY)

# app config
app = Flask(__name__)
app.config.from_object(config)
app.url_map.strict_slashes = False
app.secret_key = os.environ.get(constants.SECRETKEY_KEY)
CORS(app)
app.register_blueprint(user_bp)

# db config
db.init_app(app)
migrate = Migrate(app, db)

# User session management setup
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.unauthorized_handler
def unauthorized():
    res = redirect(FRONTEND_ENDPOINT)
    return res
# OAuth2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Server UI to test login
@app.route("/")
def index():
    if current_user.is_authenticated:
        return (
            "<p>Hello, {}! You're logged in! Email: {}</p>"
            "<div><p>Google Profile Picture:</p>"
            '<img src="{}" alt="Google profile pic"></img></div>'
            '<a class="button" href="/logout">Logout</a>'.format(
                current_user.user_name, current_user.user_email, current_user.picture
            )
        )

    else:
        return '<a class="button" href="/login">Google Login</a>'

@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    # Find and hit URL from Google that gives you user's profile information
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # Make sure the email is verified
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()[constants.GOOGLE_ID_KEY]
        users_email = userinfo_response.json()[constants.GOOGLE_EMAIL_KEY]
        picture = userinfo_response.json()[constants.GOOGLE_PICTURE_KEY]
        users_name = userinfo_response.json()[constants.GOOGLE_NAME_KEY]
    else:
        # TODO: to be formated
        return "User email not available or not verified by Google.", 400

    # Create a user in our db with the information provided by Google
    user = User(user_id=unique_id, user_name=users_name, user_email=users_email, picture=picture)
    userinfo_json = userinfo_response.json()
    engine = create_db_engine()
    check_registration(engine=engine, userinfo_json=userinfo_json)
    
    # Begin user session by logging the user in
    login_user(user)

    res = redirect(FRONTEND_ENDPOINT + "/profile")
    token = token_response.json()
    res.set_cookie(constants.GOOGLE_ID_TOKEN_KEY, token[constants.GOOGLE_ID_TOKEN_KEY])
    res.set_cookie(constants.GOOGLE_ACCESS_TOKEN_KEY, token[constants.GOOGLE_ACCESS_TOKEN_KEY])
    return res


@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    res = redirect(FRONTEND_ENDPOINT)
    res.delete_cookie(constants.GOOGLE_ID_TOKEN_KEY)
    res.delete_cookie(constants.GOOGLE_ACCESS_TOKEN_KEY)
    return res

@app.route("/profile")
@login_required
def profile():
    res = redirect(FRONTEND_ENDPOINT + "/profile")
    return res

@app.route("/quiz")
@login_required
def quiz():
    res = redirect(FRONTEND_ENDPOINT + "/quiz")
    return res

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port= 5000)
