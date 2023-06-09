import pytest
from werkzeug.datastructures import FileStorage
import sys
sys.path.append('..')
from data_manager import DataExtractorCSV, DataExtractorDOCX, DataExtractor, WrongFileExtensionError, BadFileError
import numpy as np


@pytest.fixture
def data_extractor():
    return DataExtractor()

@pytest.fixture
def data_extractor_csv():
    return DataExtractorCSV()

@pytest.fixture
def data_extractor_docx():
    return DataExtractorDOCX()

@pytest.fixture
def open_file():
    def _method(files, filename):
        try:
            fp = open(f"data/{filename}", 'rb')
            file = FileStorage(fp)
            files.append(file)
        except:
            pass

    return _method


@pytest.mark.parametrize(
        ('input_method', 'output_method'),
        (("upload", "upload"),
        ("UPLOAD", "upload"),
        ("path", "path"),
        ("PAtH", "path"))
)
def test_set_method_success(data_extractor, input_method, output_method):
    data_extractor.set_method(input_method)
    assert data_extractor.get_method() == output_method

def test_set_method_fail(data_extractor):
    with pytest.raises(Exception):
        data_extractor.set_method("test")


@pytest.mark.parametrize(
        ('input_filename', 'expected'),

        # assert that the output is -1 if an uninitialised document file is inputted
        (("FAKE.docx", -1),
        # assert that the output is -2 if a file with the wrong extension is inputted
        ("MALE PLAYERS.csv", -2),
        # if no files are inputted, assert that an exception occured
         ("", ""),
        # using a test file make sure that the output is the expected output of that particular file
        ("TEST DEGREE OF DIFFICULTY PER TOURNAMENT.docx", {'TAC1': '2.7', 'TAE21': '2.3', 'TAW11': '3.1', 'TBS2': '3.25'}))
)
def test_get_tournament_difficulty(data_extractor_docx, open_file, input_filename, expected):
    files = []
    
    open_file(files, input_filename)
    try:
        assert data_extractor_docx.get_tournament_difficulty(files) == expected
    except FileNotFoundError:
        # assert that if an exception occurs its a FileNotFoundError exception
        with pytest.raises(FileNotFoundError):
            data_extractor_docx.get_tournament_difficulty(files)
            assert "" == expected
    except BadFileError:
        assert expected == -1
    except WrongFileExtensionError:
        assert expected == -2

@pytest.mark.parametrize(
        ('input_filenames', 'expected'),

        # if players docx file is inputted make sure it returns an exception
        (("ALIEN PLAYERS.docx", -1),
         
         # wrongly formatted csv file will return empty dict
         ("PRIZE MONEY.csv", {}),

        ("MALE PLAYERS.csv,FEMALE PLAYERS.csv", ({'data/male': np.array(['MP01', 'MP02', 'MP03', 'MP04', 'MP05', 'MP06', 'MP07', 'MP08',
                                                                    'MP09', 'MP10', 'MP11', 'MP12', 'MP13', 'MP14', 'MP15', 'MP16',
                                                                    'MP17', 'MP18', 'MP19', 'MP20', 'MP21', 'MP22', 'MP23', 'MP24',
                                                                    'MP25', 'MP26', 'MP27', 'MP28', 'MP29', 'MP30', 'MP31', 'MP32'],
                                                                    dtype=object), 'data/female': np.array(['FP01', 'FP02', 'FP03', 'FP04', 'FP05', 'FP06', 'FP07', 'FP08',
                                                                    'FP09', 'FP10', 'FP11', 'FP12', 'FP13', 'FP14', 'FP15', 'FP16',
                                                                    'FP17', 'FP18', 'FP19', 'FP20', 'FP21', 'FP22', 'FP23', 'FP24',
                                                                    'FP25', 'FP26', 'FP27', 'FP28', 'FP29', 'FP30', 'FP31', 'FP32'],
                                                                    dtype=object)})),

        # if no files are inputted, assert that an exception occured
         ("", ""))
)
def test_get_players(data_extractor_csv, open_file, input_filenames, expected):
    files = []
    
    filenames = input_filenames.split(",")

    for filename in filenames:
        open_file(files, filename)
    try:
        players = data_extractor_csv.get_players(files)
        for gender in players:
            assert np.array_equal(players[gender], expected[gender])
    except FileNotFoundError:
        # assert that if an exception occurs its a FileNotFoundError exception
        with pytest.raises(FileNotFoundError):
            data_extractor_csv.get_players(files)
            assert "" == expected
    except WrongFileExtensionError:
        assert -1 == expected
    except KeyError:
        assert {} == expected


@pytest.mark.parametrize(
        ('input_filename', 'expected'),

        #  any file other than "PRIZE MONEY.csv" will return an empty dict
        (("MALE PLAYERS.csv", {}),
         
        # if no files are inputted, assert that an exception occured
         ("", ""),
         
        ("PRIZE MONEY.csv", {'TAC1': {1: '1,000,000', 2: '500,000', 3: '250,000', 4: '250,000', 5: '75,000', 6: '75,000', 7: '75,000', 8: '75,000'}, 'TAE21': {1: '1,000,000', 2: '450,000', 3: '225,000', 4: '225,000', 5: '80,000', 6: '80,000', 7: '80,000', 8: '80,000'}, 'TAW11': {1: '1,250,000', 2: '600,000', 3: '300,000', 4: '300,000', 5: '100,000', 6: '100,000', 7: '100,000', 8: '100,000'}, 'TBS2': {1: '1,375,000', 2: '700,000', 3: '350,000', 4: '350,000', 5: '150,000', 6: '150,000', 7: '150,000', 8: '150,000'}})))

def test_get_tournament_prizes(data_extractor_csv, open_file, input_filename, expected):
    files = []
    
    open_file(files, input_filename)
    try:
        assert data_extractor_csv.get_tournament_prizes(files) == expected
    except:
        # assert that if an exception occurs its a FileNotFoundError exception
        with pytest.raises(FileNotFoundError):
            data_extractor_csv.get_tournament_prizes(files)
            assert "" == expected

@pytest.mark.parametrize(
        ('input_filename', 'expected'),

        #  any file other than "RANKING POINTS.csv" will return an empty dict
        (("ALIEN PLAYERS.docx", {}),
         
        # if no files are inputted, assert that an exception occured
         ("", ""),
         
        ("RANKING POINTS.csv", {1: 100, 2: 50, 3: 30, 4: 30, 5: 10, 6: 10, 7: 10, 8: 10, 9: 5, 10: 5, 11: 5, 12: 5, 13: 5, 14: 5, 15: 5, 16: 5})))

def test_get_ranking_points(data_extractor_csv, open_file, input_filename, expected):
    files = []
    
    open_file(files, input_filename)
    try:
        assert data_extractor_csv.get_ranking_points(files) == expected
    except:
        # assert that if an exception occurs its a FileNotFoundError exception
        with pytest.raises(FileNotFoundError):
            data_extractor_csv.get_ranking_points(files)
            assert "" == expected

@pytest.mark.parametrize(
        ('input_filenames', 'expected'),

         # wrongly formatted files will return empty dict
        (("ALIEN PLAYERS.docx", {}),
         ("PRIZE MONEY.csv", {}),

        ("TAC1 ROUND 1 LADIES.csv,TAC1 ROUND 2 LADIES.csv,TAC1 ROUND 3 LADIES.csv,TAC1 ROUND 4 LADIES.csv,TAC1 ROUND 5 LADIES.csv", ({'ladies': {'1': np.array([['FP24', 1, 'FP01', 2],
                                                                                                                                                                ['FP14', 2, 'FP05', 1],
                                                                                                                                                                ['FP19', 0, 'FP16', 2],
                                                                                                                                                                ['FP22', 2, 'FP12', 1],
                                                                                                                                                                ['FP23', 2, 'FP32', 0],
                                                                                                                                                                ['FP17', 1, 'FP18', 2],
                                                                                                                                                                ['FP26', 2, 'FP30', 1],
                                                                                                                                                                ['FP31', 0, 'FP29', 2],
                                                                                                                                                                ['FP27', 0, 'FP28', 2],
                                                                                                                                                                ['FP02', 2, 'FP25', 0],
                                                                                                                                                                ['FP03', 2, 'FP09', 0],
                                                                                                                                                                ['FP04', 1, 'FP13', 2],
                                                                                                                                                                ['FP07', 2, 'FP06', 0],
                                                                                                                                                                ['FP10', 2, 'FP08', 0],
                                                                                                                                                                ['FP15', 2, 'FP11', 1],
                                                                                                                                                                ['FP21', 0, 'FP20', 2]], dtype=object), '2': np.array([['FP01', 2, 'FP16', 0],
                                                                                                                                                                ['FP22', 2, 'FP14', 1],
                                                                                                                                                                ['FP23', 1, 'FP29', 2],
                                                                                                                                                                ['FP18', 2, 'FP26', 2],
                                                                                                                                                                ['FP10', 2, 'FP28', 0],
                                                                                                                                                                ['FP13', 2, 'FP02', 1],
                                                                                                                                                                ['FP03', 0, 'FP07', 2],
                                                                                                                                                                ['FP15', 0, 'FP20', 2]], dtype=object), '3': np.array([['FP22', 2, 'FP29', 1],
                                                                                                                                                                ['FP10', 2, 'FP01', 1],
                                                                                                                                                                ['FP26', 2, 'FP20', 1],
                                                                                                                                                                ['FP13', 0, 'FP07', 2]], dtype=object), '4': np.array([['FP22', 0, 'FP07', 2],
                                                                                                                                                                ['FP10', 2, 'FP26', 1]], dtype=object), '5': np.array([['FP10', 0, 'FP07', 2]], dtype=object)}}
                                                                                                                                                                )),

        # if no files are inputted, assert that an exception occured
        ("", ""))
)
def test_get_matches(data_extractor_csv, open_file, input_filenames, expected):
    files = []
    
    filenames = input_filenames.split(",")

    for filename in filenames:
        open_file(files, filename)
    try:
        matches = data_extractor_csv.get_tournament_matches("TAC1", files)
        for match in matches["ladies"]:
            assert np.array_equal(matches["ladies"][match], expected["ladies"][match])
    except FileNotFoundError:
        # assert that if an exception occurs its a FileNotFoundError exception
        with pytest.raises(FileNotFoundError):
            data_extractor_csv.get_players(files)
            assert expected == ""
    except KeyError:
        assert expected == {}