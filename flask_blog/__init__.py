from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "54321"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager=LoginManager(app)

def query_one_filtered(table,**kwargs):
    return db.session.execute(db.select(table).filter_by(**kwargs)).scalar_one_or_none()

def query_all_filtered(table,**kwargs):
    return db.session.execute(db.select(table).filter_by(**kwargs)).scalars().all()

def query_one(table):
    return db.session.execute(db.select(table)).scalar_one_or_none()

def query_all(table):
    return db.session.execute(db.select(table)).scalars().all()


from flask_blog import routes
