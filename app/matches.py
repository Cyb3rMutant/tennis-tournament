from flask import render_template, request
from app import app
from app.models import model

@app.route('/matches')
def matches():
    form = LoginForm(request.form)
    return render_template("matches.html", form=form, logged_in=model.logged_in())
