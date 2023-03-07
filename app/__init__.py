from flask import Flask,render_template,url_for,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm,LoginForm
from models import User,Post



app=Flask(__name__)
app.config['SECRET_KEY']='54321'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)