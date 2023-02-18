from flask import Flask
from pymongo import MongoClient
import certifi

ca = certifi.where()
cluster = "mongodb+srv://strings:6Zd69XPFvPbt0Wfw@tennis-tournament.v5i5qjj.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(cluster, tlsCAFile=ca)

app = Flask(__name__)

db = client.TennisDB

from app import models, routes

if(__name__ == "__main__"):
    app.run(debug=True)