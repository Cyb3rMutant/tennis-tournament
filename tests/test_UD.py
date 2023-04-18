import pytest
from io import BytesIO
from werkzeug.datastructures import FileStorage
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from admin import endpoint1_process_files, endpoint2_process_files, endpoint3_process_files, endpoint4_process_files




#Endpoint 1 Test
UD_001_parameters = [
    (['DEGREE OF DIFFICULTY PER TOURNAMENT.docx'], ''),
    (['DEGREE OF DIFFICULTY PER TOURNAMENT 1.docx'], ['File is fake docx']),
    (['DEGREE OF DIFFICULTY PER TOURNAMENT 2.csv'], ['File is not a docx']),
    (['DEGREE OF DIFFICULTY PER TOURNAMENT 3.docx'], ['File contents are invalid']),
]

@pytest.mark.parametrize('file_names, expected', UD_001_parameters)
def test_UD_001(file_names, expected):
    file_objs = []
    for file_name in file_names:
        with open(f'tests/test_UD_data/endpoint1/{file_name}', 'rb') as file:
            file_content = file.read()
            file_obj = FileStorage(BytesIO(file_content), filename=file_name, content_type='text/csv')
            file_objs.append(file_obj)

    result = endpoint1_process_files(file_objs)
    assert result == expected




#Endpoint 2 Test
UD_002_parameters = [
    (['MALE PLAYERS.csv', 'FEMALE PLAYERS.csv'], ''),
    (['MALE PLAYERS 1.csv', 'FEMALE PLAYERS.csv'], ['Men and women must have same number of participants! No duplicates allowed']),
    (['MALE PLAYERS 2.csv', 'FEMALE PLAYERS 2.csv'], ['Player count must be a power of 2. (e.g. 16,32,64...)']),
    (['MALE PLAYERS 3.csv', 'FEMALE PLAYERS.csv'], ['Invalid male player name'] ),
    (['ALIEN PLAYERS.csv', 'FEMALE PLAYERS.csv'], ['Only MALE or FEMALE players']),

]

@pytest.mark.parametrize('file_names, expected', UD_002_parameters)
def test_UD_002(file_names, expected):
    file_objs = []
    for file_name in file_names:
        with open(f'tests/test_UD_data/endpoint2/{file_name}', 'rb') as file:
            file_content = file.read()
            file_obj = FileStorage(BytesIO(file_content), filename=file_name, content_type='text/csv')
            file_objs.append(file_obj)

    result = endpoint2_process_files(file_objs)
    assert result == expected




#Endpoint 3 Test
UD_003_parameters = [
    (['PRIZE MONEY.csv', 'DEGREE OF DIFFICULTY PER TOURNAMENT.docx',], ''),
    (['test1/PRIZE MONEYSSS.csv', 'DEGREE OF DIFFICULTY PER TOURNAMENT.docx',], ['File name MUST be "PRIZE MONEY.csv"']),
    (['test2/PRIZE MONEY.csv', 'DEGREE OF DIFFICULTY PER TOURNAMENT.docx',], ['Tournament name TAW11 or more is missing from CSV']),
    (['test3/PRIZE MONEY.csv', 'DEGREE OF DIFFICULTY PER TOURNAMENT.docx',], ['Tournament should have prize money for ONLY top 8']),
    (['test4/PRIZE MONEY.csv', 'DEGREE OF DIFFICULTY PER TOURNAMENT.docx',], ['Value in Place or/and Prize IS NOT an integer']),
]


@pytest.mark.parametrize('file_names, expected', UD_003_parameters)
def test_UD_003(file_names, expected):
    file_objs = []
    for file_name in file_names:
        with open(f'tests/test_UD_data/endpoint3/{file_name}', 'rb') as file:
            file_content = file.read()
            file_obj = FileStorage(BytesIO(file_content), filename=file_name, content_type='text/csv') #this is the problem
            file_objs.append(file_obj)

    result = endpoint3_process_files(file_objs)
    assert result == expected





#Endpoint 4 Tests

import os
UD_004_files = sorted(os.listdir('tests/test_UD_data/endpoint4/test0_correct'))
UD_004_parameters = [
    (UD_004_files, ''),
]

@pytest.mark.parametrize('file_names, expected', UD_004_parameters)
def test_UD_004(file_names, expected):
    file_objs = []
    for file_name in file_names:
        with open(f'tests/test_UD_data/endpoint4/test0_correct/{file_name}', 'rb') as file:
            file_content = file.read()
            file_obj = FileStorage(BytesIO(file_content), filename=file_name, content_type='text/csv') 
            file_objs.append(file_obj)

    result = endpoint4_process_files(file_objs)
    assert result == expected







UD_005_files = sorted(os.listdir('tests/test_UD_data/endpoint4/test1_normal'))
UD_005_parameters = [
    (UD_005_files, 
    ["Invalid score in ladies match ['FP18' 2 'FP26' 2] in round 2 in TAC1", 
    "Invalid score in men match ['MP14' 1 'MP01' 2] in round 3 in TAC1", 
    "Invalid score in men match ['MP07' 1 'MP25' 2] in round 4 in TAW11"]),
]

@pytest.mark.parametrize('file_names, expected', UD_005_parameters)
def test_UD_005(file_names, expected):
    file_objs = []
    for file_name in file_names:
        with open(f'tests/test_UD_data/endpoint4/test1_normal/{file_name}', 'rb') as file:
            file_content = file.read()
            file_obj = FileStorage(BytesIO(file_content), filename=file_name, content_type='text/csv') 
            file_objs.append(file_obj)

    result = endpoint4_process_files(file_objs)
    assert result == expected






UD_006_files = sorted(os.listdir('tests/test_UD_data/endpoint4/test2'))
UD_006_parameters = [
    (UD_006_files, ['Number of files uploaded should be 40 not 41']),
]

@pytest.mark.parametrize('file_names, expected', UD_006_parameters)
def test_UD_006(file_names, expected):
    file_objs = []
    for file_name in file_names:
        with open(f'tests/test_UD_data/endpoint4/test2/{file_name}', 'rb') as file:
            file_content = file.read()
            file_obj = FileStorage(BytesIO(file_content), filename=file_name, content_type='text/csv') 
            file_objs.append(file_obj)

    result = endpoint4_process_files(file_objs)
    assert result == expected







UD_007_files = sorted(os.listdir('tests/test_UD_data/endpoint4/test3'))
UD_007_parameters = [
    (UD_007_files,["""Invalid file name TAC1 ROUND 2 MEN I AM IMPOSTER.csv: ['File name should be formatted in `TNAME "ROUND" RNUM GENDER`.']"""]),
]

@pytest.mark.parametrize('file_names, expected', UD_007_parameters)
def test_UD_007(file_names, expected):
    file_objs = []
    for file_name in file_names:
        with open(f'tests/test_UD_data/endpoint4/test3/{file_name}', 'rb') as file:
            file_content = file.read()
            file_obj = FileStorage(BytesIO(file_content), filename=file_name, content_type='text/csv') 
            file_objs.append(file_obj)

    result = endpoint4_process_files(file_objs)
    assert result == expected






UD_008_files = sorted(os.listdir('tests/test_UD_data/endpoint4/test4'))
UD_008_parameters = [
    (UD_008_files,
    ["Invalid file name SS ROUND 3 MEN.csv: ['Invalid tournament name SS.']",
    """Invalid file name TAC1 NOTROUND 5 LADIES.csv: ['Second word has to be "ROUND" not NOTROUND.']""",
    "Invalid file name TAC1 ROUND 3 ALIENS.csv: ['Invalid gender ALIENS should be either LADIES or MEN.']",
    "Invalid file name TAC1 ROUND 6 LADIES.csv: ['Round number should be between 1 and 5.']",
    "Invalid file name TAE21 ROUND SS LADIES.csv: ['Round number should be an integer between 1 and 5.']",
    ]
    ),
]

@pytest.mark.parametrize('file_names, expected', UD_008_parameters)
def test_UD_008(file_names, expected):
    file_objs = []
    for file_name in file_names:
        with open(f'tests/test_UD_data/endpoint4/test4/{file_name}', 'rb') as file:
            file_content = file.read()
            file_obj = FileStorage(BytesIO(file_content), filename=file_name, content_type='text/csv') 
            file_objs.append(file_obj)

    result = endpoint4_process_files(file_objs)
    assert result == expected




UD_009_files = sorted(os.listdir('tests/test_UD_data/endpoint4/test5'))
UD_009_parameters = [
    (UD_009_files,
    ["""Invalid player name in men's match ['SP23' 3 'MP22' 0] in round 3 in TAC1""",
    """Duplicate player name in men's match ['MP29' 3 'MP32' 1] in round 4 in TAE21""",
    """Invalid score in ladies match ['FP04' 3 'FP03' 0] in round 2 in TBS2"""]
    ),
]

@pytest.mark.parametrize('file_names, expected', UD_009_parameters)
def test_UD_009(file_names, expected):
    file_objs = []
    for file_name in file_names:
        with open(f'tests/test_UD_data/endpoint4/test5/{file_name}', 'rb') as file:
            file_content = file.read()
            file_obj = FileStorage(BytesIO(file_content), filename=file_name, content_type='text/csv') 
            file_objs.append(file_obj)

    result = endpoint4_process_files(file_objs)
    assert result == expected




UD_010_files = sorted(os.listdir('tests/test_UD_data/endpoint4/test6'))
UD_010_parameters = [
    (UD_010_files,['Invalid number of matches  in men  round 5 in TAW11'] ),
]

@pytest.mark.parametrize('file_names, expected', UD_010_parameters)
def test_UD_010(file_names, expected):
    file_objs = []
    for file_name in file_names:
        with open(f'tests/test_UD_data/endpoint4/test6/{file_name}', 'rb') as file:
            file_content = file.read()
            file_obj = FileStorage(BytesIO(file_content), filename=file_name, content_type='text/csv') 
            file_objs.append(file_obj)

    result = endpoint4_process_files(file_objs)
    assert result == expected