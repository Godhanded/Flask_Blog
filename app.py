from flask import Flask,render_template,url_for,redirect
import json

app=Flask(__name__)

data=[
    {
        "user":"test user",
        "body":"bshdkcohjbdjshybgjshcjbdhsjchuychdhbgfjhshiybcdhsjhsjuhdjssdgtchd\
        sdhdsjdkjlujgsdjhsjuhygjdshjhbydhsjhdybdsjibhdsjjihdbhsdsbhdn",
        "author":"Adams",
        "date":"12/07/2023",
    },

    {
        "user":"test user",
        "body":"bshdkcohjbdjshybgjshcjbdhsjchuychdhbgfjhshiybcdhsjhsjuhdjssdgtchd\
        sdhdsjdkjlujgsdjhsjuhygjdshjhbydhsjhdybdsjibhdsjjihdbhsdsbhdn",
        "author":"Kate",
        "date":"13/07/2023",
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html",datas=data)

@app.route("/about")
def about():
    return render_template("about.html")


if (__name__== __name__):
    app.debug=True
    app.run()