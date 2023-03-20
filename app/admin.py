from flask import render_template, request, url_for, redirect
from app import app
from models import model
from forms import LoginForm, RegistrationForm

import sys
sys.path.append('..')
from data_manager import DataExtractor, DataExtractorCSV, DataExtractorDOCX, WrongFileExtensionError, BadFileError, UnformattedDocx

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not model.logged_in():
        return redirect(url_for('home'))

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
    
    try:
        de.get_tournament_difficulty(files)
        return ''
    except BadFileError:
        return 'File is fake docx'
    except WrongFileExtensionError:
        return 'File is not a docx'
    except UnformattedDocx: 
        return 'File contents are invalid'



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
    de2 = DataExtractorDOCX()
    
    try:
        prize_money = de.get_tournament_prizes([files[0]])
        if(prize_money == {}):
            return 'File name MUST be "PRIZE MONEY.csv"'
        else:
            pass
    except:
        return 'Invalid File ??'
 
    #Case 1
    for key in de2.get_tournament_difficulty([files[1]]):

        #TEMPORARY FIX FOR TAW11 & TBS2 & TAE21. e.g keys are as follows {'TAC1', 'TAW11 ', 'TBS2 ', 'TAE21 '}
        if key == 'TAW11' or key =='TBS2' or key == 'TAE21':
            key+= ' '

        if key not in prize_money:
            return f'Type1_Error: Tournament name {key} or more is missing from CSV'


    #Case 2/3
    for k,v in prize_money.items():
        if len(v) != 8:
            return 'Type2_Error: Tournament should have prize money for ONLY top 8'
        for k2,v2 in v.items():
            try:
                k2 = int(k2)
                v2 = v2.replace(",", "")
                v2 = int(v2)
            except:
                return 'Type3_Error: Value in Place & Prize IS NOT an integer'


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

