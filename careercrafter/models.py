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

class questions(db.Model):
    q_id = db.Column(db.Integer, primary_key=True)
    q_text = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"questions('{self.q_text}')"

class careers(db.Model):
    title = db.Column(db.String(50), primary_key=True)
    courses = db.Column(db.String(200), unique=True, nullable=False)
    institutions = db.Column(db.String(200), nullable=False)
    entrance_exams = db.Column(db.String(80), nullable=True)

    def __repr__(self):
        return f"users('{self.title}', '{self.courses}', '{self.institutions}', '{self.entrance_exams}')"

class d(db.Model):
    personality_type = db.Column(db.String(5), primary_key=True)
    description = db.Column(db.String(400), nullable=False)