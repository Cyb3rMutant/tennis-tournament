from flask import render_template, request
from app import app
from models import model
from forms import LoginForm

@app.route('/view_matches/<season>/<tournament>')
def view_matches(season, tournament):
    form = LoginForm(request.form)
    t = model.get_tournament(season, tournament)
    return render_template("view_matches.html", form=form, logged_in=model.logged_in(), tournament = t)
