from flask import render_template, request, redirect, jsonify
from app import app
from app.models import model
from app.forms import LoginForm


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    print("1")
    print(request)
    if request.method == 'POST' and form.validate():
        print("2")
        match status:= model.login(form.email.data, form.password.data):
            case 0:
                return ''
            case 1:
                return "user not found"
            case 2:
                return "incorrect password"
            case _:
                return status
