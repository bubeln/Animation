import packages as read_file
from helpers.common_variables import CommonVariables


class ObjectType(CommonVariables):

    CHARACTER_PATH = "../helpers/nodes_lists/characters.json"
    ITEM_PATH = "../helpers/nodes_lists/items.json"
    LOCATION_PATH = "../helpers/nodes_lists/locations.json"

    def __init__(self):
        self.characters = read_file.read_json_file(self.CHARACTER_PATH)
        self.items = read_file.read_json_file(self.ITEM_PATH)
        self.locations = read_file.read_json_file(self.LOCATION_PATH)

    def define_object_type(self, object_name):
        if object_name in self.characters:
            return self.CHARACTER_TYPE

        if object_name in self.items:
            return self.ITEM_TYPE

        if object_name in self.locations:
            return self.LOCATION_TYPE
        else:
            raise "Unsupported data type"
