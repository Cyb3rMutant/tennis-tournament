from abc import *
from os import listdir
from os.path import isdir, isfile
import pathlib
from docx import Document
import pandas as pd
import numpy as np
import re

DATA_PATH = f"{pathlib.Path(__file__).parent.resolve()}/data"

class ModeNotFoundError(Exception):
    pass

class DataManager:
    '''
    The Data Manager class is used to extract data from csv and docx files (WIP)

    Attributes:
        _mode: A string referring to the extension of the file(s) being read from, by default its "csv".
        _modes: An array of all the valid extensions for mode.
        _data_path: A string containing the path where the data files are located.
    '''

    def __init__(self, path=(pathlib.Path(__file__).parent.resolve())) -> None:
        self._modes = ["csv", "docx"]
        self._mode = "csv"
        self._data_path = path

    def set_mode(self, mode):
        '''
        Sets the Data Manager's mode to the input (if its valid).
        '''
        mode = mode.lower()
        if(mode in self._modes):
            self._mode = mode
        else:
            raise ModeNotFoundError(f'"{mode}" is not a valid mode.')

    def get_mode(self):
        '''
        Returns the current mode.
        '''
        return self._mode

    def set_data_path(self, path):
        '''
        Sets the data path to the input if its a real path.
        '''
        if(isdir(path)):
            if(path[-1] != "/"):
                path += "/"
            self._data_path = path
        else:
            raise FileNotFoundError(f'Path "{path}" not found')
        
    def get_data_path(self):
        '''
        Returns the data path.
        '''
        return self._data_path

    def get_data_files(self):
        '''
        Returns the names of all the files with the mode extension.
        '''
        files = [f for f in listdir(self._data_path) if (f.endswith(f".{self._mode}") and isfile(self._data_path+f))]
        return files

class DataExtractor(metaclass=ABCMeta):

    def __init__(self) -> None:
        self.dm = DataManager()
        self.dm.set_data_path(DATA_PATH)

class DataExtractorCSV(DataExtractor):

    def __init__(self) -> None:
        super().__init__()
        self.dm.set_mode("csv")
    
    def get_players(self):
        players = {}
        for doc in self.dm.get_data_files():
            if(re.findall("PLAYERS.csv$", doc)):
                df = pd.read_csv(f"{DATA_PATH}/{doc}")
                player_arr = df.to_numpy().T[0]
                key = doc.split(" ")[0].lower()
                players[key] = np.concatenate([df.columns.values, player_arr])
        return players
    
    def get_tournament_prizes(self):
        prizes = {}
        for doc in self.dm.get_data_files():
            if(doc == "PRIZE MONEY.csv"):
                df = pd.read_csv(f"{DATA_PATH}/{doc}")
                tournament = ""
                for row in df.to_numpy():
                    if(not pd.isnull(row[0])):
                        tournament = row[0]
                        prizes[tournament] = {}
                    prizes[tournament][row[1]] = row[2]
        return prizes
    
    def get_ranking_points(self):
        points = {}
        for doc in self.dm.get_data_files():
            if(doc == "RANKING POINTS.csv"):
                df = pd.read_csv(f"{DATA_PATH}/{doc}")
                for c, row in enumerate(df.to_numpy()):
                    # not sure, theres an input mistake in csv data
                    points[c+1] = row[0]
        return points
    
    def get_tournament_matches(self, tournament):
        
        tournament = tournament.upper()
        matches = {}
        files = self.dm.get_data_files()
        files.sort()
        for doc in files:
            if(re.findall(f"{tournament} ROUND [0-9]+ *", doc.upper())):
                df = pd.read_csv(f"{DATA_PATH}/{doc}")
                tournament_round = doc.split(" ")[2]
                gender = doc.split(" ")[3].split(".")[0].lower()
                if(not matches.get(gender)):
                    matches[gender] = {}
                matches[gender][tournament_round] = df.iloc[:,:4].to_numpy()
                
        return matches
class DataExtractorDOCX(DataExtractor):

    def __init__(self) -> None:
        super().__init__()
        self.dm.set_mode("docx")
    
    def get_tournament_difficulty(self):
        '''
        Returns a dictionary containing the tournament name and the tournament difficulty as key value pairs respectively.
        '''
        tournament_dict = {}
        for doc in self.dm.get_data_files():
            if(doc == "DEGREE OF DIFFICULTY PER TOURNAMENT.docx"):
                document = Document(f"{DATA_PATH}/{doc}")
                # go line by line through the document
                for i in range(len(document.paragraphs)):
                    # for every line split the text to get the tournament name and difficulty
                    tournament = document.paragraphs[i].text
                    tournament = tournament.split(" – degree of difficulty ")
                    # add the tournament name and difficulty to the tournament dictionary if they exist on that line
                    if(len(tournament) > 1):
                        tournament_dict[tournament[0]] = tournament[1]
        return tournament_dict
        

if(__name__ == "__main__"):
    # dm = DataManager()
    # dm.set_mode("docx")
    # print(dm.get_mode())
    # dm.set_data_path(DATA_PATH)
    # print(dm.get_data_files())

    # document = Document(f"{DATA_PATH}/DEGREE OF DIFFICULTY PER TOURNAMENT.docx")
    # for p in document.paragraphs:
    #     print(p.text)

    de = DataExtractorCSV()
    # import pprint 
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(de.get_tournament_matches("tac1"))
    print(de.get_tournament_matches("tac1"))
    
    