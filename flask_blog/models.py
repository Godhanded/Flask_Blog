from flask_blog import db, login_manager, query_all_filtered, query_one_filtered
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return query_one_filtered(User, id=user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.Relationship("Post", backref="author", lazy=True)

    def __init__(self, username, email, password, image_file="default.jpg"):
        self.username = username
        self.email = email
        self.image_file = image_file
        self.password = password

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, title, date_posted, content, user_id) -> None:
        self.title = title
        self.date_posted = date_posted
        self.content = content
        self.user_id = user_id

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
