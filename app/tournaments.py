from flask import render_template, request
from app import app
from app.models import model
from app.forms import LoginForm


@app.route('/tournaments')
def tournaments():
    form = LoginForm(request.form)
    return render_template("tournaments.html", form=form, logged_in=model.logged_in())
