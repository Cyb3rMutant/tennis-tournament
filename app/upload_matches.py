from flask import render_template, request
from app import app
from app.models import model
from app.forms import LoginForm

@app.route('/upload_matches')
def upload_matches():
    form = LoginForm(request.form)
    return render_template("upload_matches.html", form = form, logged_in=model.logged_in())
