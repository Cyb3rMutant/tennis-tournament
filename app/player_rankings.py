from flask import render_template, request
from app import app
from app.models import model
from app.forms import LoginForm


@app.route('/player_rankings')
def player_rankings():
    form = LoginForm(request.form)
    return render_template("player_rankings.html", form=form, logged_in=model.logged_in())
