from careercrafter import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return users.query.get(user_id)


class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    personality_type = db.Column(db.String(80), nullable=True)
    otp = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"users('{self.user_name}', '{self.email}', '{self.personality_type}')"
