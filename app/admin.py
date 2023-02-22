from flask import render_template, request
from app import app
from app.models import model
from app.forms import LoginForm

@app.route('/admin')
def admin():
    form = LoginForm(request.form)
    return render_template("admin.html", form=form, logged_in=model.logged_in())
