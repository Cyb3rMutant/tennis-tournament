
from flask import render_template, request
from app import app
from models import model
from forms import LoginForm


@app.route('/view_player_rankings')
def view_player_rankings():
    form = LoginForm(request.form)
    return render_template("view_player_rankings.html", form=form, logged_in=model.logged_in())
