from flask import render_template, request, url_for, redirect
from app import app
from models import model
from forms import LoginForm, RegistrationForm

import sys
sys.path.append('..')
from data_manager import DataExtractor, DataExtractorCSV, DataExtractorDOCX

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    form = LoginForm(request.form)
    return render_template("admin.html", form=form, logged_in=model.logged_in())

@app.route('/add-admin', methods=['GET', 'POST'])
def add_admin():
    form = LoginForm(request.form)
    reg_form = RegistrationForm(request.form)

    

    if request.method == 'POST' and reg_form.validate():
        print("TEST")
        #get dict with data for each field
        details = reg_form.data

        #match statement uses what the model returns
        match status:= model.add_admin(details):
            case 0:
                print("User added")
                return redirect(url_for('admin'))
            case 1:
                return "user already exists"  #how are we doing error messages? (flash?)
            case _:
                return status
            
        
            
    return render_template("add_admin.html", form=form, logged_in=model.logged_in(), reg_form=reg_form)

@app.route('/add-matches')
def add_matches():
    form = LoginForm(request.form)
    return render_template("add_matches.html", form=form, logged_in=model.logged_in())

@app.route('/add-season')
def add_season():
    form = LoginForm(request.form)
    return render_template("add_season.html", form=form, logged_in=model.logged_in())


#Tournament difficulty (Single file)
@app.route('/endpoint1', methods=['POST'])
def endpoint1():
    files = request.files.getlist('files')
    de = DataExtractorDOCX()
    
    match(de.get_tournament_difficulty(files)):
        case -1:
            return 'File is a fake docx'
        case -2:
            return 'File is not a docx'
        case -3:
            return 'File is docx but isnt formatted correctly'
        case _:
            return ''



#Players (Multiple files)
@app.route('/endpoint2', methods=['POST'])
def endpoint2():
    print("endpoint2")
    files = request.files.getlist('files')
    for file in files:
        print(file.filename)
    return ''


#Prize money (Single file)
@app.route('/endpoint3', methods=['POST'])
def endpoint3():
    files = request.files.getlist('files')
    de = DataExtractorCSV()

    match(de.get_tournament_prizes(files)):
        case -1:
            return 'File needs to have name with prize money formatted as csv'
        
        #Room for other cases 
        # (Actual validating that the file has correct contents and not words)
        

        case _:
            return ''




#Match data (Multiple files)
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

