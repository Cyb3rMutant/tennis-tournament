from flask import session
from passlib.hash import sha256_crypt
from jinja2.utils import import_string
from pymongo import MongoClient
import certifi
from classes.admin import Admin
from classes.user import User
from classes.season import Season
from bson.objectid import ObjectId
from classes.rankings import Rankings
from classes.player import Player


import jsonpickle


class Model():
    def __init__(self):
        ca = certifi.where()
        cluster = "mongodb+srv://strings:6Zd69XPFvPbt0Wfw@tennis-tournament.v5i5qjj.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(cluster, tlsCAFile=ca)
        self.__db = client.TennisDB
        self.__players = {'M': Rankings(), 'F': Rankings()}

        m_players = self.__db.players.find({"type": 'M'}).sort('ranking_points')
        rank = 0
        for p in m_players:
            player = Player(p['_id'], p['name'], p['ranking_points'])
            self.__players['M'].add_player(player, rank)
            rank+=1

        f_players = self.__db.players.find({"type": 'F'}).sort('ranking_points')
        rank = 0
        for p in f_players:
            player = Player(p['_id'], p['name'], p['ranking_points'])
            self.__players['F'].add_player(player, rank)
            rank+=1

        seasons = self.__db.seasons.find()
        self.__seasons = dict()

        for s in seasons:
            season = Season(s["name"])
            tournaments = self.__db.tournaments.find({"_id": {"$in": s["tournament_ids"]}})
            for t in tournaments:
                season.add_tournament(t["_id"], t["name"], t["difficulty"], t["location"], t["time"], t["prize_id"])
            self.__seasons[s["_id"]] = season


    def logged_in(self,) -> bool:
        return "user" in session

    def login(self, email: str, password: str) -> int:
        user = self.__db.admins.find_one({'email': email})

        if not user:
            return 1

        if sha256_crypt.verify(password, user['password_hash']):
            session["user"] = jsonpickle.encode(Admin(user["_id"], user["name"]))
            return 0

        return 2

model = Model()
