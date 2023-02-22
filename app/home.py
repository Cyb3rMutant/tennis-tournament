from flask import render_template, request
from app import app
from app.models import model
from app.forms import LoginForm


@app.route('/home')
@app.route('/index')
@app.route('/')
def home():
    form = LoginForm(request.form)
    return render_template("home.html", form=form, logged_in=model.logged_in())
