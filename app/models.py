from flask import session
from passlib.hash import sha256_crypt
from pymongo import MongoClient
import certifi
from classes.admin import Admin
from classes.season import Season
from bson.objectid import ObjectId
from classes.rankings import Rankings
from classes.player import Player
from classes.prize import Prize
from classes.match import Match
import threading
from datetime import datetime, timedelta
from time import sleep
import jsonpickle
# from data_manager import DataExtractorCSV, DataExtractorDOCX


class Model():
    def __init__(self):
        ca = certifi.where()
        cluster = "mongodb+srv://strings:6Zd69XPFvPbt0Wfw@tennis-tournament.v5i5qjj.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(cluster, tlsCAFile=ca)
        self.__db = client.TennisDB
        self.__players = {'M': Rankings(), 'F': Rankings()}
        self.__tournament_cache: list[ObjectId] = dict()

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

                season.add_tournament(t["_id"], t["name"], t["difficulty"], prizes)
            self.__seasons[s["_id"]] = season

        thread = threading.Thread(target=self.tournament_cache_handler)
        thread.daemon = True  # Set daemon to True so that the thread terminates when the main thread terminates
        thread.start()

    def tournament_cache_handler(self):
        while True:
            for t in list(self.__tournament_cache):
                if self.__tournament_cache[t][1] + timedelta(minutes= 30) < datetime.now():
                    continue

                self.__tournament_cache[t][2].clear()

                self.__tournament_cache.pop(t)

            sleep(600)

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

    def logout(self):
        session.clear()
    
    def add_admin(self, details):
        #if email exists already
        if self.__db.admins.find_one({'email': details['email']}):
            return 1
        else:
            #hash password and add to dict
            details['password_hash'] = sha256_crypt.hash(details['password'])
            #remove unnessasary data
            keys_list = ['confirm', 'accept_tos', 'password']  #keys to remove
            for key in keys_list:
                del details[key]
            #add user into database
            self.__db.admins.insert_one(details)
            return 0 #success

    def get_seasons(self) -> dict:
        return self.__seasons
    
    def get_tournament(self, s_id, t_id):
        if t_id in self.__tournament_cache:
            print("in")
            self.__tournament_cache[t_id][1] = datetime.now()
            return self.__tournament_cache[t_id][0]

        tournament = self.__seasons[ObjectId(s_id)].get_tournaments()[ObjectId(t_id)]
        competitions = self.__db.competitions.find({"tournament" : ObjectId(t_id)})

        for c in competitions:
            players = self.player_ids_to_objects(c["players"], c["type"])

            final = self.__db.matches.find({"competition_id": c["_id"]}).sort("round",-1).limit(1)[0]
            matches = [Match(players={"A":players[final["players"]["A"]],"B":players[final["players"]["B"]]}, sets=final["sets"], round= final["round"])]
            for match in matches:
                if not match.get_round()-1:
                    break
                for player in match.get_players().values():
                    prev = self.__db.matches.find_one({"competition_id": c["_id"], "round": match.get_round()-1, "$or":[{"players.A": player.get_id()}, {"players.B": player.get_id()}]})
                    matches.append(Match(players={"A":players[prev["players"]["A"]],"B":players[prev["players"]["B"]]}, sets=prev["sets"], round= prev["round"]))

            tournament.add_competition(c["type"], players, matches)

        self.__tournament_cache[t_id] = [tournament.to_json(), datetime.now(), tournament]
        return self.__tournament_cache[t_id][0]

    def player_ids_to_objects(self, ids: list[ObjectId], p_tupe : str) -> dict:
        players = {}
        all_players = self.__players[p_tupe]
        for p in all_players.get_positions():
            if p.get_id() not in ids:
                continue
            players[p.get_id()] = p
        return players
    
    def get_players(self) -> dict:
        return self.__players
    

    #methods to upload data taken from data extractor into database 
    #eg upload_players, upload_tournaments, 

    def upload_players(self, ):
        pass


model = Model()
