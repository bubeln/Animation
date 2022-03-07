from common_variables import CommonVariables
from global_methods import GlobalMethods


class ObjectType(CommonVariables, GlobalMethods):

    CHARACTER_PATH = "./nodes_lists/characters.json"
    ITEM_PATH = "./nodes_lists/items.json"
    LOCATION_PATH = "./nodes_lists/locations.json"

    def __init__(self):
        self.characters = self.read_json_file(self.CHARACTER_PATH)
        self.items = self.read_json_file(self.ITEM_PATH)
        self.locations = self.read_json_file(self.LOCATION_PATH)

    def define_object_type(self, object_name):
        if object_name in self.characters:
            return self.CHARACTER_TYPE

        if object_name in self.items:
            return self.ITEM_TYPE

        if object_name in self.locations:
            return self.LOCATION_TYPE
        else:
            raise "Unsupported data type"
