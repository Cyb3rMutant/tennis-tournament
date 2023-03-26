import sys
sys.path.append('..')
import os
from data_manager import DataExtractor, DataExtractorCSV, DataExtractorDOCX, WrongFileExtensionError, BadFileError, UnformattedDocx
from flask import render_template, request, url_for, redirect
from app import app
from models import model
from forms import LoginForm, RegistrationForm
import math


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

    print(reg_form.data)
    for i in reg_form.data:
        print(i)

    if request.method == 'POST' and reg_form.validate():
        print("TEST")
        # get dict with data for each field
        details = reg_form.data

        # match statement uses what the model returns
        match status := model.add_admin(details):
            case 0:
                print("User added")
                return "success"
            case 1:
                # how are we doing error messages? (flash?)
                return "user already exists"
            case _:
                return status

    print("hereeeeeeeeeeeee")
    return render_template("add_admin.html", form=form, logged_in=model.logged_in(), reg_form=reg_form)


@app.route('/add-matches')
def add_matches():
    form = LoginForm(request.form)
    return render_template("add_matches.html", form=form, logged_in=model.logged_in())


@app.route('/add-season')
def add_season():
    form = LoginForm(request.form)
    return render_template("add_season.html", form=form, logged_in=model.logged_in())


# Tournament difficulty (Single file)
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


# Players (Multiple files)
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

            # UNIQUE values for set allowed only
            for k, v in data.items():
                players[k].update(v)

        except WrongFileExtensionError:
            return 'Files are not CSV'

        except:
            return 'Only MALE or FEMALE players'

    # Case 2 - Uneven participant number
    # Something with Nan's sometimes randomly
    if len(players['male']) != len(players['female']):
        return 'Men and women must have same number of participants! No duplicates allowed'

    if math.log2(len(players)).is_integer() == False:
        return 'Player count must be a power of 2. (e.g. 16,32,64)'

    # Case 3 - Player name does not start with MP or FP
    prefixes = {'male': 'MP', 'female': 'FP'}
    for gender in prefixes:
        for player in players[gender]:
            if not player.startswith(prefixes[gender]):
                return f'Invalid {gender} player name'

    # print(players)
    return ''


# Prize money (Single file)
@app.route('/endpoint3', methods=['POST'])
def endpoint3():
    files = request.files.getlist('files')
    de = DataExtractorCSV()
    de2 = DataExtractorDOCX()

    try:
        prize_money = de.get_tournament_prizes([files[0]])
        if (prize_money == {}):
            return 'File name MUST be "PRIZE MONEY.csv"'
        else:
            pass
    except:
        return 'Invalid File ??'

    print(prize_money)

    # Case 1
    for key in de2.get_tournament_difficulty([files[1]]):

        if key not in prize_money:
            return f'Tournament name {key} or more is missing from CSV'

    # Case 2/3
    for k, v in prize_money.items():
        if len(v) != 8:
            return 'Tournament should have prize money for ONLY top 8'
        for k2, v2 in v.items():
            try:
                k2 = int(k2)
                v2 = v2.replace(",", "")
                v2 = int(v2)
            except:
                return 'Value in Place & Prize IS NOT an integer'

    return ''


# Match data (Multiple files)
@app.route('/endpoint4', methods=['POST'])
def endpoint4():
    print("endpoint4")
    files = request.files.getlist('files')

    de = DataExtractorCSV()
    de2 = DataExtractorDOCX()

    # PREPROCESSING PREPROCESSING PREPROCESSING
    # Getting players & Difficulty which will be used for validation.
    tournament_difficulty = de2.get_tournament_difficulty([files[0]])

    # We dont use this (Only length matters)
    players = {'male': set(), 'female': set()}
    for i in range(2):  # We dont use this
        data = de.get_players([files[i+1]])  # We dont use this
        for k, v in data.items():  # We dont use this
            players[k].update(v)  # We dont use this

    length_of_players = len(players['male'])  # 32 - Only this matters

    # nubmer_of_rounds = 5
    # This is  number 5, because 5 rounds
    number_of_rounds = math.log2(length_of_players)
    number_of_rounds = round(number_of_rounds)

    # Number of files allowed to be uploaded = 40. 5 rounds * 2 = for 1 tournament then * 4 for each tournament
    number_of_files_allowed = (number_of_rounds * 2) * \
        len(tournament_difficulty)

    # VALIDATION #VALIDATION #VALIDATION #VALIDATION #VALIDATION #VALIDATION

    # Case 1 validate file upload number:
    if len(files[3:]) != number_of_files_allowed:
        return f'Number of files uploaded should be {number_of_files_allowed} not {len(files[3:])}'

    # Case 2 validate file names:
    file_count = {}

    def validate_filename(filename):
        basename = os.path.basename(filename)
        name_only = os.path.splitext(basename)[0]
        splitted_filename = name_only.split()

        try:
            tournament_name, round_txt, round_number, gender = splitted_filename
        except:
            return 'File name should have four parts separated by spaces.'

        if tournament_name not in tournament_difficulty:
            return f'Invalid tournament code {tournament_name}.'
        if gender not in ['LADIES', 'MEN']:
            return f'Invalid gender {gender} should be LADIES or MEN.'
        if round_txt != 'ROUND':
            return f"Second word has to be 'ROUND' not {round_txt}."
        try:
            round_number = int(round_number)
            if round_number < 1 or round_number > number_of_rounds:
                return f'Round number should be between 1 and {number_of_rounds}.'
        except:
            return f'Round number should be an integer between 1 and {number_of_rounds}.'

        if filename in file_count:
            return f'Duplicate file name found {filename}'

        file_count[filename] = 1

        return None

    errors = []
    for f in files[3:]:
        error = validate_filename(f.filename)
        if error:
            errors.append(f'Invalid file name {f.filename}: {error}')

    # Case 3: Check for N round length  & Check if number of rounds is okay

    # Get a count of all the labels
    round_counts = {}
    for f in files[3:]:
        basename = os.path.basename(f.filename)
        name_only = os.path.splitext(basename)[0]
        splitted_filename = name_only.split()

        try:
            tournament_name, round_txt, round_number, gender = splitted_filename
        except:
            return 'File name should have four parts separated by spaces.'

        if tournament_name not in round_counts:
            round_counts[tournament_name] = {'LADIES': 0, 'MEN': 0}

        round_counts[tournament_name][gender] += 1

    # print(round_counts)
    # Case 3.5 Check if number of rounds in each tournament is equal to correct number of rounds
    for tournament_name in round_counts:
        if round_counts[tournament_name]['LADIES'] != number_of_rounds or round_counts[tournament_name]['MEN'] != number_of_rounds:
            errors.append(
                f'Tournament {tournament_name} should have {number_of_rounds} rounds for both men and women.')

    # Return list of errors for files
    if errors:
        return errors

    # File name/upload validation over.

    # FILE CONTENT VALIDATION #FILE CONTENT VALIDATION #FILE CONTENT VALIDATION #FILE CONTENT VALIDATION #FILE CONTENT VALIDATION

    # One player must have no more or less than 3 score for a win
    # One player must have no more or less than 2 score for a win

    return ''


@app.route('/submit-form', methods=['POST'])
def submit_form():

    print("Submit formmmmmmm")

    files = request.files.getlist('files')
    for file in files:
        print(file.filename)
    # print(files)

    return ''
