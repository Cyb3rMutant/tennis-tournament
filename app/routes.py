from flask import render_template
from app import app
from app.models import Model

model = Model()

@app.route('/')
def index():
    # collections is for testing only feel free to remove
    collections = model.get_collections()
    return render_template("index.html", collections=collections)

@app.route('/view_tournaments')
def view_tournaments():
    return render_template("view_tournaments.html")
    