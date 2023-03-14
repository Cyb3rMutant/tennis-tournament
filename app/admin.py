from flask import render_template, request
from app import app
from models import model
from forms import LoginForm

@app.route('/admin')
def admin():
    form = LoginForm(request.form)
    return render_template("admin.html", form=form, logged_in=model.logged_in())

@app.route('/add-admin')
def add_admin():
    form = LoginForm(request.form)
    return render_template("add_admin.html", form=form, logged_in=model.logged_in())

@app.route('/add-matches')
def add_matches():
    form = LoginForm(request.form)
    return render_template("add_matches.html", form=form, logged_in=model.logged_in())

@app.route('/add-season')
def add_season():
    form = LoginForm(request.form)
    return render_template("add_season.html", form=form, logged_in=model.logged_in())



@app.route('/endpoint1', methods=['POST'])
def endpoint1():
    print("endpoint1")
    files = request.files.getlist('files')
    for file in files:
        print(file.filename)
    # print(files)
    return ''

@app.route('/endpoint2', methods=['POST'])
def endpoint2():
    print("endpoint2")
    files = request.files.getlist('files')
    for file in files:
        print(file.filename)
    # print(files)
    return ''


@app.route('/endpoint3', methods=['POST'])
def endpoint3():
    print("endpoint3")
    files = request.files.getlist('files')
    for file in files:
        print(file.filename)
    # print(files)
    return ''



@app.route('/endpoint4', methods=['POST'])
def endpoint4():
    print("endpoint4")
    files = request.files.getlist('files')
    for file in files:
        print(file.filename)
    # print(files)
    return ''


@app.route('/submit-form', methods=['POST'])
def submit_form():

    print("Submit formmmmmmm")

    files = request.files.getlist('files')
    for file in files:
        print(file.filename)
    # print(files)

    return ''

