from flask import render_template, request
from app import app
from models import model
from forms import LoginForm


@app.route('/view-tournaments')
def view_tournaments():
    form = LoginForm(request.form)

    seasons = model.get_seasons()

    return render_template("view_tournaments.html", form=form, logged_in=model.logged_in(), seasons = seasons)

@app.route('/view-matches/<season>/<tournament>')
def view_matches(season, tournament):
    form = LoginForm(request.form)
    t = model.get_tournament(season, tournament)
    return render_template("view_matches.html", form=form, logged_in=model.logged_in(), tournament = t)

@app.route('/view-player-rankings')
def view_player_rankings():
    form = LoginForm(request.form)
    return render_template("view_player_rankings.html", form=form, logged_in=model.logged_in())
