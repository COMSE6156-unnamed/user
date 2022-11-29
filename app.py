import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for
from flask_migrate import Migrate
from flask_dance.contrib.google import make_google_blueprint, google
import config
from utils.exts import db
from blueprints import user_bp, login_bp
from blueprints.login import set_secret_key
from oauthlib.oauth2.rfc6749.errors import TokenExpiredError

# app config
app = Flask(__name__)
app.config.from_object(config)

# DB config
db.init_app(app)
migrate = Migrate(app, db)

##
set_secret_key(app)

app.register_blueprint(user_bp)
app.register_blueprint(login_bp, url_prefix='/login')

@app.route("/")
def index():
    return "hello"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port= 5000)
    
