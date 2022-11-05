from utils.exts import db

class User(db.Model):
    __tablename__ = "user_db"
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column