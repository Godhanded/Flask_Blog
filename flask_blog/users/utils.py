import secrets
import os
from PIL import Image
from flask import url_for, current_app
from flask_blog import mail
from flask_mail import Message


def save_picture(picture_data):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture_data.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, "static/profile_pics", picture_fn
    )
    output_size = (125, 125)
    i = Image.open(picture_data)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        "Password Reset Request", sender="noreply@demo.com", recipients=[user.email]
    )
    msg.body = f"""To reset your password, visit the following link <h1>Hey there</h1>
{url_for('reset_token',token=token,_external=True)}

<p style="color: bisque;">If you did not make this request then simply ignore this email, no changes will be made</p>
"""
    mail.send(msg)
