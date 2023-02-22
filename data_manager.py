from abc import *
from os import listdir
from os.path import isdir, isfile
import pathlib
from docx import Document

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

    de = DataExtractorDOCX()
    print(de.get_tournament_difficulty())
    