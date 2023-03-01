from flask import render_template, request
from app import app
from models import model
from forms import LoginForm

@app.route('/view_matches')
def matches():
    form = LoginForm(request.form)
    return render_template("view_matches.html", form=form, logged_in=model.logged_in())
