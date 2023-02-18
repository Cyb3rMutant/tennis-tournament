from app import db

class Model():

    def __init__(self):
        pass

    # collections is for testing only feel free to remove
    def get_collections(self):
        return db.list_collection_names()