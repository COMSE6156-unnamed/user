
from utils.exts import db

class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String)
    password = db.Column(db.String)

    def __init__(self, user_id, user_name, password):
        self.user_id = user_id
        self.user_name = user_name
        self.password = password