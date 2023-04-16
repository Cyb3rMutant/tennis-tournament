import pytest
from io import BytesIO
from werkzeug.datastructures import FileStorage
from admin import endpoint2_process_files

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
        with open(f'app/data_app/{file_name}', 'rb') as file:
            file_content = file.read()
            file_obj = FileStorage(BytesIO(file_content), filename=file_name, content_type='text/csv')
            file_objs.append(file_obj)

    result = endpoint2_process_files(file_objs)
    assert result == expected

