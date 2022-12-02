from flask import Flask, session, jsonify, redirect
from flask_migrate import Migrate
from flask_dance.contrib.google import google
import config
from config import create_db_engine
from utils.exts import db
import utils.constants as constants
from blueprints import user_bp, login_bp
from blueprints.login import set_secret_key, check_registration
from oauthlib.oauth2.rfc6749.errors import TokenExpiredError
from flask_cors import CORS

# app config
app = Flask(__name__)
app.config.from_object(config)
CORS(app)

# DB config
db.init_app(app)
migrate = Migrate(app, db)

##
set_secret_key(app)

app.register_blueprint(user_bp)
app.register_blueprint(login_bp, url_prefix='/login')

@app.route("/")
def index():
    try:
        if not google.authorized:
            return redirect("/login")

        google_data = google.get(constants.GOOGLE_USER_INFO_ENDPOINT).json()
        session[constants.GOOGLE_DATA_KEY] = google_data
        engine = create_db_engine()
        check_registration(engine=engine, data=google_data)

        return jsonify(session[constants.GOOGLE_DATA_KEY])

    except TokenExpiredError:
        del login_bp.token
        session.clear()
        return redirect("/login")

@app.route("/logout")
def logout():
    token = login_bp.token[constants.GOOGLE_ACCESS_TOKEN_KEY]
    if google.authorized:
        try:
            google.post(
                constants.GOOGLE_REVOKE_TOKEN_URL,
                params={"token": token},
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            del login_bp.token
            session.clear()
            return jsonify({"message": "success"})

        except TokenExpiredError:
            del login_bp.token
            session.clear()
            return jsonify({"message": "success"})
        
    return jsonify({"message": "success"})
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port= 5000)
    
