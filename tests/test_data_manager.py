import pytest
from werkzeug.datastructures import FileStorage
import sys
sys.path.append('..')
from data_manager import DataExtractorCSV, DataExtractorDOCX, DataExtractor


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

        # assert that the output is {} if a wrongly formatted file is inputted
        (("TEST MALE PLAYERS.csv", {}),
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
    except:
        # assert that if an exception occurs its a FileNotFoundError exception
        with pytest.raises(FileNotFoundError):
            data_extractor_docx.get_tournament_difficulty(files)
