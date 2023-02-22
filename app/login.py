from flask import render_template, request, redirect
from app import app
from app.models import model
from app.forms import LoginForm


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        match status:= model.login(form.email.data, form.password.data):
            case 0:
                return redirect(request.referrer)
                # return render_template("admin.html", form=form, logged_in=model.logged_in())
            case 1:
                return render_template("message.html", form=form, logged_in=model.logged_in(), success = False, message = "user not found")
            case 2:
                return render_template("message.html", form=form, logged_in=model.logged_in(), success = False, message = "incorrect password")
            case _:
                return status

