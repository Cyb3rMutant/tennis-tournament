from flask import render_template, request
from app import app
from models import model
from forms import LoginForm

@app.route('/add_admin')
def add_admin():
    form = LoginForm(request.form)
    return render_template("add_admin.html", form=form, logged_in=model.logged_in())
