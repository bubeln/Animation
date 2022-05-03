import packages as read_file
from data.common_variables import CommonVariables


class NodeType(CommonVariables):

    def __init__(self):
        self.characters = read_file.read_json_file("../data/nodes_lists/characters.json")
        self.items = read_file.read_json_file("../data/nodes_lists/items.json")
        self.locations = read_file.read_json_file("../data/nodes_lists/locations.json")

    def define_node_type(self, node_name):
        if node_name in self.characters:
            return self.CHARACTER_TYPE

        if node_name in self.items:
            return self.ITEM_TYPE

        if node_name in self.locations:
            return self.LOCATION_TYPE
        else:
            raise "Unsupported data type"
