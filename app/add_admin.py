from flask import render_template
from app import app
from app.models import model
from app.forms import LoginForm

@app.route('/add_admin')
def add_admin():
    form = LoginForm(request.form)
    return render_template("add_admin.html", form=form, logged_in=model.logged_in())
