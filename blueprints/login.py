import os
from dotenv import load_dotenv
from flask_dance.contrib.google import make_google_blueprint, google
from flask import Flask, render_template, redirect, url_for
from oauthlib.oauth2.rfc6749.errors import TokenExpiredError

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
            
            user_id = google_data['id']
            user_email = google_data['email']
            user_name = google_data['name']

        except TokenExpiredError as e:
            return redirect(url_for("google.login"))
    else:
        return redirect(url_for('google.login'))

    return render_template('index.j2',
                           google_data=google_data,
                           fetch_url=google.base_url + user_info_endpoint)