from os import listdir
from os.path import isdir, isfile
import pathlib

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

if(__name__ == "__main__"):
    dm = DataManager()
    dm.set_mode("csv")
    print(dm.get_mode())
    dm.set_data_path(f"{pathlib.Path(__file__).parent.resolve()}/data")
    print(dm.get_data_files())