import json
from file_path_constants import DATA_CONSTANTS_JSON_FILE_NAME

def read_data_from_json():

    with open(DATA_CONSTANTS_JSON_FILE_NAME) as f:
        date = json.load(f)
        f.close()
    return date


def write_data_on_json(date):

    with open(DATA_CONSTANTS_JSON_FILE_NAME, 'w') as f:
        json.dump(date, f)
        f.close()
