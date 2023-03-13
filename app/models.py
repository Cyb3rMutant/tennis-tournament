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
from classes.prize import Prize
from classes.match import Match


import jsonpickle


class Model():
    def __init__(self):
        ca = certifi.where()
        cluster = "mongodb+srv://strings:6Zd69XPFvPbt0Wfw@tennis-tournament.v5i5qjj.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(cluster, tlsCAFile=ca)
        self.__db = client.TennisDB
        self.__players = {'M': Rankings(), 'F': Rankings()}
        self.__tournament_cache: [ObjectId] = list()

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
                prizes = self.__db.prizes.find_one({"_id": t["prize_id"]})
                prizes = [Prize(p, prizes["currency"]) for p in prizes["amounts"]]

                season.add_tournament(t["_id"], t["name"], t["difficulty"], t["location"], t["time"], prizes)
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

    def get_seasons(self) -> dict:
        return self.__seasons
    
    def get_tournament(self, s_id, t_id):
        tournament = self.__seasons[ObjectId(s_id)].get_tournaments()[ObjectId(t_id)]
        if t_id in self.__tournament_cache:
            print("in")
            return tournament.to_json()

        competitions = self.__db.competitions.find({"tournament" : ObjectId(t_id)})

        for c in competitions:
            players = self.player_ids_to_objects(c["players"], c["type"])

            final = self.__db.matches.find({"competition_id": c["_id"]}).sort("round",-1).limit(1)[0]
            matches = [Match(players={"A":players[final["players"]["A"]],"B":players[final["players"]["B"]]}, sets=final["sets"], round= final["round"])]
            for match in matches:
                if match.get_round()-1 == 1:
                    break
                for player in match.get_players().values():
                    prev = self.__db.matches.find_one({"competition_id": c["_id"], "round": match.get_round()-1, "$or":[{"players.A": player.get_id()}, {"players.B": player.get_id()}]})
                    matches.append(Match(players={"A":players[prev["players"]["A"]],"B":players[prev["players"]["B"]]}, sets=prev["sets"], round= prev["round"]))

            print(matches)
            tournament.add_competition(c["type"], players, matches)

        return tournament.to_json()

    def player_ids_to_objects(self, ids: [ObjectId], p_tupe : str) -> dict:
        players = {}
        all_players = self.__players[p_tupe]
        for p in all_players.get_positions():
            if p.get_id() not in ids:
                continue
            players[p.get_id()] = p
        return players


model = Model()
