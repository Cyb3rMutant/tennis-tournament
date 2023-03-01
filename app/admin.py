from flask import render_template, request
from app import app
from models import model
from forms import LoginForm

@app.route('/admin')
def admin():
    form = LoginForm(request.form)
    return render_template("admin.html", form=form, logged_in=model.logged_in())
