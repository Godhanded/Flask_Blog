from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_blog.models import User, db
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = db.session.execute(
            db.select(User).filter_by(username=username.data)
        ).scalar_one_or_none()
        if user:
            raise ValidationError("Username already exists, please use another")

    def validate_email(self, email):
        user = db.session.execute(
            db.select(User).filter_by(email=email.data)
        ).scalar_one_or_none()
        if user:
            raise ValidationError("Email already exists")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])

    picture = FileField(
        "Update Profile Picture", validators=[FileAllowed(["jpg", "png"])]
    )

    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = db.session.execute(
                db.select(User).filter_by(username=username.data)
            ).scalar_one_or_none()
            if user:
                raise ValidationError("Username already exists, please use another")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = db.session.execute(
                db.select(User).filter_by(email=email.data)
            ).scalar_one_or_none()
            if user:
                raise ValidationError("Email already exists")


class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Reset Password")
