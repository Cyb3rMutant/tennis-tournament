from flask import session
from passlib.hash import sha256_crypt
from pymongo import MongoClient
import certifi
import pymongo
from classes.admin import Admin
from classes.season import Season, Tournament
from bson.objectid import ObjectId
from classes.rankings import Rankings
from classes.player import Player
from classes.prize import Prize
from classes.match import Match
import threading
from datetime import datetime, timedelta
from time import sleep
import jsonpickle
import sys
sys.path.append('..')
from data_manager import DataExtractor, DataExtractorCSV, DataExtractorDOCX, WrongFileExtensionError, BadFileError, UnformattedDocx

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
        self.load_tournament(tournament)
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
    
    def load_tournament(self, tournament: Tournament) -> None:
        competitions = self.__db.competitions.find({"tournament" : tournament.get_id()})

        for c in competitions:
            players = self.player_ids_to_objects(c["players"], c["type"][0].upper())

            final = self.__db.matches.find({"competition_id": c["_id"]}).sort("round",-1).limit(1)[0]
            matches = [Match(
                players={"A":players[final["players"]["A"]],
                         "B":players[final["players"]["B"]]}, 
                sets=final["sets"], 
                round= final["round"])]
            for match in matches:
                if not match.get_round()-1:
                    break
                for player in match.get_players().values():
                    prev = self.__db.matches.find_one({"competition_id": c["_id"], "round": match.get_round()-1, "$or":[{"players.A": player.get_id()}, {"players.B": player.get_id()}]})
                    matches.append(Match(players={"A":players[prev["players"]["A"]],"B":players[prev["players"]["B"]]}, sets=prev["sets"], round= prev["round"]))

            tournament.add_competition(c["type"], players, matches)




    #process is - data input into form, validated, uploaded, given to my function is 2d array containing file objects 
    #where is my upload players function called

    #data is passed to the function in a 2d array
    #essentially we dont know how many columns in each row (dont know how many files for each)
    # [degreeofdifficuly][][][]
    # [players][players][players]
    # [prizedata][prizedata]

    #then take 2d array of files and pass each one through data extractor then into the db
    #data extractor should give them in dict (need to check format)

    #upload validated file data into the database
    def upload_data(self, files) -> Season:
        de_csv = DataExtractorCSV()
        de_doc = DataExtractorDOCX()

        players_dict = de_csv.get_players(files[1])  #players stored as array under key for their gender
        for t in players_dict:
            for p in players_dict[t]:
                if p_id:=self.__db.players.update_one({"name": p}, {"$setOnInsert": {"ranking_points": 0, "type": t[0].upper()}}, upsert=True).upserted_id:
                    player = Player(p_id, p, 0)
                    self.__players[t[0].upper()].add_player(player, len(self.__players[t[0].upper()].get_positions()))
 
        tournament_dict = de_doc.get_tournament_difficulty(files[0])
        prize_dict = de_csv.get_tournament_prizes(files[2])
        tournament_ids = []
        #get prize data 
        for tournament in tournament_dict.keys():
            prize_money = [p for p in prize_dict[tournament].items()]
            prize_id = self.__db.prizes.insert_one({'amounts': prize_money, 'currency': "$"}).inserted_id
            print(tournament_dict)
            t_id = self.__db.tournaments.insert_one({'name': tournament, 'difficulty': float(tournament_dict[tournament]), 'prize_id': prize_id}).inserted_id
            for t in players_dict:
                player_ids = [p["_id"] for p in self.__db.players.find({"name": {"$in": list(players_dict[t])}})]
                self.__db.competitions.insert_one({"players": player_ids, "tournament": t_id, "type": t[0].upper()})
            tournament_ids.append(t_id)

            matches_dict = de_csv.get_tournament_matches(tournament, files[3])

            for competition, matches_info in matches_dict.items():   #eg ladies
                competition_round_matches = []     #list of dictionaries of all the matches to be insert for a specific competition and round
                #get competition id
                competition_type = "M"  #default
                if competition == 'ladies':
                    competition_type = "F"
                competition_id = self.__db.competitions.find_one({'tournament': t_id, 'type': competition_type})['_id']

                for comp_round in matches_info:
                    matches_array = matches_info[comp_round]
                    for match in matches_array:  #row
                        player_A = match[0]
                        player_A_sets = match[1]

                        player_B = match[2]
                        player_B_sets = match[3]

                        #get player ids
                        player_A_id = self.__db.players.find_one({'name': player_A})['_id']
                        player_B_id = self.__db.players.find_one({'name': player_B})['_id']

                        #add to list
                        competition_round_matches.append({'competition_id': competition_id, 'round': int(comp_round), 'players' : {'A': player_A_id, 'B': player_B_id}, 'sets': {'A': player_A_sets, 'B': player_B_sets}})

                #insert all the matches for that competition and round into the db
                self.__db.matches.insert_many(competition_round_matches)

        s_id = self.__db.seasons.insert_one({"name": "Season %d"%len(self.__seasons), "tournament_ids": tournament_ids}).inserted_id

        new_season = self.__db.seasons.find_one({"_id": s_id})

        season = Season(new_season["name"])
        tournaments = self.__db.tournaments.find({"_id": {"$in": new_season["tournament_ids"]}})
        for t in tournaments:
            prizes = self.__db.prizes.find_one({"_id": t["prize_id"]})
            prizes = [Prize(p, prizes["currency"]) for p in prizes["amounts"]]

            season.add_tournament(t["_id"], t["name"], t["difficulty"], prizes)
        self.__seasons[new_season["_id"]] = season

        return season

    def calculate_points(self, season: Season):
        points = [p['points'] for p in self.__db.ranking_points.find().sort('place', pymongo.ASCENDING)]
        for tournament in season.get_tournaments().values():
            self.load_tournament(tournament)
            for competition in tournament.get_competitions():
                matches = competition.get_matches()
                matches[0].get_players()[matches[0].get_winner()].update_ranking_points(points[0])
                for i, m in enumerate(matches):
                    print(m.get_round())
                    if i > len(points)-2:
                        break
                    print(type(tournament.get_difficulty()))
                    points_won = points[i+1] * tournament.get_difficulty()
                    player = m.get_players()[m.get_loser()]
                    player.update_ranking_points(points_won)
                    self.__db.players.update_one({"_id": player.get_id()}, {"$inc": {"ranking_points": points_won}})


        for r in self.__players.values():
            r.update_positions()



model = Model()
