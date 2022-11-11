from flask import Flask, render_template, request, jsonify, session, redirect
from flask_migrate import Migrate
import config
from utils.exts import db
from blueprints import user_bp


# app config
app = Flask(__name__)
app.config.from_object(config)

# DB config
db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(user_bp)

@app.route("/")
def index():
    return "hello"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port= 5000)
    
