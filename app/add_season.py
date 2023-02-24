from flask import render_template, request
from app import app
from app.models import model
from app.forms import LoginForm


@app.route('/add_season')
def add_season():
    form = LoginForm(request.form)
    return render_template("add_season.html", form=form, logged_in=model.logged_in())
