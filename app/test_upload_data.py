import pytest
from io import BytesIO
from werkzeug.datastructures import FileStorage
from admin import endpoint2_process_files, endpoint3_process_files, endpoint1_process_files, endpoint4_process_files




endpoint_1_test_data = [
    (['DEGREE OF DIFFICULTY PER TOURNAMENT.docx'], ''),
    (['DEGREE OF DIFFICULTY PER TOURNAMENT 1.docx'], ['File is fake docx']),
    (['DEGREE OF DIFFICULTY PER TOURNAMENT 2.csv'], ['File is not a docx']),
    (['DEGREE OF DIFFICULTY PER TOURNAMENT 3.docx'], ['File contents are invalid']),



]

@pytest.mark.parametrize('file_names, expected', endpoint_1_test_data)
def test_endpoint1(file_names, expected):
    file_objs = []
    for file_name in file_names:
        with open(f'app/data_app/endpoint1/{file_name}', 'rb') as file:
            file_content = file.read()
            file_obj = FileStorage(BytesIO(file_content), filename=file_name, content_type='text/csv')
            file_objs.append(file_obj)

    result = endpoint1_process_files(file_objs)
    assert result == expected







endpoint_2_test_data = [
    (['MALE PLAYERS.csv', 'FEMALE PLAYERS.csv'], ''),
    (['MALE PLAYERS 1.csv', 'FEMALE PLAYERS.csv'], ['Men and women must have same number of participants! No duplicates allowed']),
    (['MALE PLAYERS 2.csv', 'FEMALE PLAYERS 2.csv'], ['Player count must be a power of 2. (e.g. 16,32,64...)']),
    (['MALE PLAYERS 3.csv', 'FEMALE PLAYERS.csv'], ['Invalid male player name'] ),
    (['ALIEN PLAYERS.csv', 'FEMALE PLAYERS.csv'], ['Only MALE or FEMALE players']),


]

@pytest.mark.parametrize('file_names, expected', endpoint_2_test_data)
def test_endpoint2(file_names, expected):
    file_objs = []
    for file_name in file_names:
        with open(f'app/data_app/endpoint2/{file_name}', 'rb') as file:
            file_content = file.read()
            file_obj = FileStorage(BytesIO(file_content), filename=file_name, content_type='text/csv')
            file_objs.append(file_obj)

    result = endpoint2_process_files(file_objs)
    assert result == expected





endpoint_3_test_data = [
    (['PRIZE MONEY.csv', 'DEGREE OF DIFFICULTY PER TOURNAMENT.docx',], ''),
    (['test1/PRIZE MONEYSSS.csv', 'DEGREE OF DIFFICULTY PER TOURNAMENT.docx',], ['File name MUST be "PRIZE MONEY.csv"']),
    (['test2/PRIZE MONEY.csv', 'DEGREE OF DIFFICULTY PER TOURNAMENT.docx',], ['Tournament name TAW11 or more is missing from CSV']),
    (['test3/PRIZE MONEY.csv', 'DEGREE OF DIFFICULTY PER TOURNAMENT.docx',], ['Tournament should have prize money for ONLY top 8']),
    (['test4/PRIZE MONEY.csv', 'DEGREE OF DIFFICULTY PER TOURNAMENT.docx',], ['Value in Place or/and Prize IS NOT an integer']),
]


@pytest.mark.parametrize('file_names, expected', endpoint_3_test_data)
def test_endpoint3(file_names, expected):
    file_objs = []
    for file_name in file_names:
        with open(f'app/data_app/endpoint3/{file_name}', 'rb') as file:
            file_content = file.read()
            file_obj = FileStorage(BytesIO(file_content), filename=file_name, content_type='text/csv') #this is the problem
            file_objs.append(file_obj)

    result = endpoint3_process_files(file_objs)
    assert result == expected








import os
test_files_0 = sorted(os.listdir('app/data_app/endpoint4/test0_correct'))
endpoint_4_test_data_test0 = [
    (test_files_0, ''),
]


@pytest.mark.parametrize('file_names, expected', endpoint_4_test_data_test0)
def test_endpoint4_0(file_names, expected):
    file_objs = []
    for file_name in file_names:
        with open(f'app/data_app/endpoint4/test0_correct/{file_name}', 'rb') as file:
            file_content = file.read()
            file_obj = FileStorage(BytesIO(file_content), filename=file_name, content_type='text/csv') #this is the problem
            file_objs.append(file_obj)

    result = endpoint4_process_files(file_objs)
    assert result == expected







test_files_1 = sorted(os.listdir('app/data_app/endpoint4/test1_normal'))
endpoint_4_test_data_test1 = [
    (test_files_1, 
    ["Invalid score in ladies match ['FP18' 2 'FP26' 2] in round 2 in TAC1", 
    "Invalid score in men match ['MP14' 1 'MP01' 2] in round 3 in TAC1", 
    "Invalid score in men match ['MP07' 1 'MP25' 2] in round 4 in TAW11"]),
]

@pytest.mark.parametrize('file_names, expected', endpoint_4_test_data_test1)
def test_endpoint4_1(file_names, expected):
    file_objs = []
    for file_name in file_names:
        with open(f'app/data_app/endpoint4/test1_normal/{file_name}', 'rb') as file:
            file_content = file.read()
            file_obj = FileStorage(BytesIO(file_content), filename=file_name, content_type='text/csv') #this is the problem
            file_objs.append(file_obj)

    result = endpoint4_process_files(file_objs)
    assert result == expected






test_files_2 = sorted(os.listdir('app/data_app/endpoint4/test2'))
endpoint_4_test_data_test2 = [
    (test_files_2, ['Number of files uploaded should be 40 not 41']),
]

@pytest.mark.parametrize('file_names, expected', endpoint_4_test_data_test2)
def test_endpoint4_2(file_names, expected):
    file_objs = []
    for file_name in file_names:
        with open(f'app/data_app/endpoint4/test2/{file_name}', 'rb') as file:
            file_content = file.read()
            file_obj = FileStorage(BytesIO(file_content), filename=file_name, content_type='text/csv') #this is the problem
            file_objs.append(file_obj)

    result = endpoint4_process_files(file_objs)
    assert result == expected







test_files_3 = sorted(os.listdir('app/data_app/endpoint4/test3'))
endpoint_4_test_data_test3 = [
    (test_files_3,["""Invalid file name TAC1 ROUND 2 MEN I AM IMPOSTER.csv: ['File name should be formatted in `TNAME "ROUND" RNUM GENDER`.']"""]),
]

@pytest.mark.parametrize('file_names, expected', endpoint_4_test_data_test3)
def test_endpoint4_3(file_names, expected):
    file_objs = []
    for file_name in file_names:
        with open(f'app/data_app/endpoint4/test3/{file_name}', 'rb') as file:
            file_content = file.read()
            file_obj = FileStorage(BytesIO(file_content), filename=file_name, content_type='text/csv') #this is the problem
            file_objs.append(file_obj)

    result = endpoint4_process_files(file_objs)
    assert result == expected






test_files_4 = sorted(os.listdir('app/data_app/endpoint4/test4'))
endpoint_4_test_data_test4 = [
    (test_files_4,
    ["Invalid file name SS ROUND 3 MEN.csv: ['Invalid tournament name SS.']",
    """Invalid file name TAC1 NOTROUND 5 LADIES.csv: ['Second word has to be "ROUND" not NOTROUND.']""",
    "Invalid file name TAC1 ROUND 3 ALIENS.csv: ['Invalid gender ALIENS should be either LADIES or MEN.']",
    "Invalid file name TAC1 ROUND 6 LADIES.csv: ['Round number should be between 1 and 5.']",
    "Invalid file name TAE21 ROUND SS LADIES.csv: ['Round number should be an integer between 1 and 5.']",
    ]
    ),
]

@pytest.mark.parametrize('file_names, expected', endpoint_4_test_data_test4)
def test_endpoint4_4(file_names, expected):
    file_objs = []
    for file_name in file_names:
        with open(f'app/data_app/endpoint4/test4/{file_name}', 'rb') as file:
            file_content = file.read()
            file_obj = FileStorage(BytesIO(file_content), filename=file_name, content_type='text/csv') #this is the problem
            file_objs.append(file_obj)

    result = endpoint4_process_files(file_objs)
    assert result == expected




test_files_5 = sorted(os.listdir('app/data_app/endpoint4/test5'))
endpoint_4_test_data_test5 = [
    (test_files_5,
    ["""Invalid player name in men's match ['SP23' 3 'MP22' 0] in round 3 in TAC1""",
    """Duplicate player name in men's match ['MP29' 3 'MP32' 1] in round 4 in TAE21""",
    """Invalid score in ladies match ['FP04' 3 'FP03' 0] in round 2 in TBS2"""]
    ),
]

@pytest.mark.parametrize('file_names, expected', endpoint_4_test_data_test5)
def test_endpoint4_5(file_names, expected):
    file_objs = []
    for file_name in file_names:
        with open(f'app/data_app/endpoint4/test5/{file_name}', 'rb') as file:
            file_content = file.read()
            file_obj = FileStorage(BytesIO(file_content), filename=file_name, content_type='text/csv') #this is the problem
            file_objs.append(file_obj)

    result = endpoint4_process_files(file_objs)
    assert result == expected



test_files_6 = sorted(os.listdir('app/data_app/endpoint4/test6'))
endpoint_4_test_data_test6 = [
    (test_files_6,['Invalid number of matches  in men  round 5 in TAW11'] ),
]

@pytest.mark.parametrize('file_names, expected', endpoint_4_test_data_test6)
def test_endpoint4_6(file_names, expected):
    file_objs = []
    for file_name in file_names:
        with open(f'app/data_app/endpoint4/test6/{file_name}', 'rb') as file:
            file_content = file.read()
            file_obj = FileStorage(BytesIO(file_content), filename=file_name, content_type='text/csv') #this is the problem
            file_objs.append(file_obj)

    result = endpoint4_process_files(file_objs)
    assert result == expected