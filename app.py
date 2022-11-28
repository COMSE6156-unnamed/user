import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for
from flask_migrate import Migrate
from flask_dance.contrib.google import make_google_blueprint, google
import config
from utils.exts import db
from blueprints import user_bp


# load environment variables
load_dotenv()

# app config
app = Flask(__name__)
app.config.from_object(config)

# google oauth credentials & settings
client_id = os.getenv('GOOGLE_CLIENT_ID')
client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
app.secret_key = os.getenv('secret_key')
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

google_bp = make_google_blueprint(
    client_id=client_id,
    client_secret=client_secret,
    reprompt_consent=True,
    scope=["profile", "email"]
)

# DB config
db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(user_bp)
app.register_blueprint(google_bp, url_prefix="/login")

@app.route("/")
def index():
    google_data = None
    user_info_endpoint = '/oauth2/v2/userinfo'
    if google.authorized:
        google_data = google.get(user_info_endpoint).json()
        
        user_id = google_data['id']
        user_email = google_data['email']
        user_name = google_data['name']

    return render_template('index.j2',
                           google_data=google_data,
                           fetch_url=google.base_url + user_info_endpoint)

@app.route('/login')
def login():
    return redirect(url_for("google.login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port= 5000)
    
