from flask import render_template, request
from app import app
from app.models import model
from app.forms import LoginForm


@app.route('/view_tournaments')
def view_tournaments():
    form = LoginForm(request.form)
    return render_template("view_tournaments.html", form=form, logged_in=model.logged_in())
