import json


class GlobalMethods:

    def read_json_file(self, path):
        file = open(path, "r")
        json_data = json.load(file)
        file.close()

        return json_data
