from flask import render_template, redirect, url_for, flash, request, abort, Blueprint
from flask_login import current_user,login_required


student=Blueprint("student",__name__)

@student.route('/cgpa',methods=["POST","GET"])
def cgpa():
    if request.method=="POST":
        [print(item) for item in request.form.items()]
        # print(request.form.)
    return render_template('student/gp.html',title='cgpa')