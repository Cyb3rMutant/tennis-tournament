from flask import render_template, request, url_for, redirect
from app import app
from models import model
from forms import LoginForm, RegistrationForm
import math
import sys
sys.path.append('..')
from data_manager import DataExtractor, DataExtractorCSV, DataExtractorDOCX, WrongFileExtensionError, BadFileError, UnformattedDocx

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # if not model.logged_in():
    #     return redirect(url_for('home'))

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
    de = DataExtractorCSV()

    players = {'male': set(), 'female': set()}
    for f in files:
        try:
            data = de.get_players([f])
            if data == {}: 
                return 'Files are Invalid'
            
            #UNIQUE values for set allowed only
            for k, v in data.items():
                players[k].update(v)  
                
        except WrongFileExtensionError:
            return 'Files are not CSV' 

        except:
            return 'Only MALE or FEMALE players'
    
    #Case 2 - Uneven participant number
    if len(players['male']) != len(players['female']): #Something with Nan's sometimes randomly
        return 'Men and women must have same number of participants! No duplicates allowed'



    if math.log2(len(players)).is_integer() == False:
        return 'Player count must be a power of 2. (e.g. 16,32,64)'


    #Case 3 - Player name does not start with MP or FP
    prefixes = {'male': 'MP', 'female': 'FP'}
    for gender in prefixes:
        for player in players[gender]:
            if not player.startswith(prefixes[gender]):
                return f'Invalid {gender} player name'


    # print(players)
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
 

    print(prize_money)

    #Case 1
    for key in de2.get_tournament_difficulty([files[1]]):

        if key not in prize_money:
            return f'Tournament name {key} or more is missing from CSV'


    #Case 2/3
    for k,v in prize_money.items():
        if len(v) != 8:
            return 'Tournament should have prize money for ONLY top 8'
        for k2,v2 in v.items():
            try:
                k2 = int(k2)
                v2 = v2.replace(",", "")
                v2 = int(v2)
            except:
                return 'Value in Place & Prize IS NOT an integer'


    return ''


#Match data (Multiple files)
@app.route('/endpoint4', methods=['POST'])
def endpoint4():
    print("endpoint4")
    files = request.files.getlist('files')

    de = DataExtractorCSV()
    de2 = DataExtractorDOCX()

    print(files)

    #Preprocessing, Getting players & Difficulty which will be used for validation.
    tournament_difficulty = de2.get_tournament_difficulty([files[0]])
    players = {'male': set(), 'female': set()}
    for i in range (2):
        data = de.get_players([files[i+1]])
        for k, v in data.items():
            players[k].update(v)
    length_of_players = len(players['male']) #32

    #5
    number_of_rounds = math.log2(length_of_players) #This is  number 5, because 5 rounds
    number_of_rounds = round(number_of_rounds)



    # print(tournament_difficulty)
    # print(players)

    #Case 1 Validate file names:
    for f in files[3:]:
        print (f.filename)



    #Case 2 Validate file lengths:
    


    #Case 3 Validate file contents (big one):




    #One player must have no more or less than 3 score for a win
    #One player must have no more or less than 2 score for a win
        
    #Case 1, Validate file names & lengths



    return ''



@app.route('/submit-form', methods=['POST'])
def submit_form():

    print("Submit formmmmmmm")

    files = request.files.getlist('files')
    for file in files:
        print(file.filename)
    # print(files)

    return ''

