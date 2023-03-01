from flask import render_template, request
from app import app
from models import model
from forms import LoginForm
print("Hello")


@app.route('/home')
@app.route('/index')
@app.route('/')
def home():
    form = LoginForm(request.form)
    return render_template("home.html", form=form, logged_in=model.logged_in())
