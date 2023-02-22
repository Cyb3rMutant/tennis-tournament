from flask import render_template, request
from app import app
from app.models import model
from app.forms import LoginForm


@app.route('/upload_seasons')
def upload_seasons():
    form = LoginForm(request.form)
    return render_template("upload_seasons.html", form=form, logged_in=model.logged_in())
