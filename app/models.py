from flask import session
from passlib.hash import sha256_crypt
from jinja2.utils import import_string
from pymongo import MongoClient
import certifi
from classes.admin import Admin
from classes.user import User

import jsonpickle


class Model():
    def __init__(self):
        ca = certifi.where()
        cluster = "mongodb+srv://strings:6Zd69XPFvPbt0Wfw@tennis-tournament.v5i5qjj.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(cluster, tlsCAFile=ca)
        self.__db = client.TennisDB
        self.__session = session

    def logged_in(self,) -> bool:
        return "user" in self.__session

    def login(self, email: str, password: str) -> int:
        user = self.__db.test.find_one({'email': email})

        if not user:
            return 1

        if sha256_crypt.verify(password, user['password_hash']):
            self.__session["user"] = jsonpickle.encode(Admin(user["_id"], user["name"]))
            return 0

        return 2


model = Model()
