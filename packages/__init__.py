import json


def read_json_file(path):
    file = open(path, "r")
    json_data = json.load(file)
    file.close()

    return json_data
