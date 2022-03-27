import re
import packages as read_file
from dto.character_dto import CharacterDTO
from dto.frontground_dto import FrontgroundDTO
from dto.location_dto import LocationDTO
from dto.move_dto import MoveDTO
from helpers.common_variables import CommonVariables
from helpers.object_type import ObjectType


class JsonOperation(CommonVariables):

    PATH_REGEX = '[\[\].]'

    def __init__(self):
        self.action_result_json = None
        self.moves = []
        self.world_characters = {}
        self.world_locations = {}
        self.frontground_data = {}

    def prepare_data_for_animation(self, file_path):
        self.action_result_json = read_file.read_json_file("../productions/action_results.json")
        json_data = read_file.read_json_file(file_path)
        self.get_init_world_state(json_data["WorldSource"][0]["LSide"]["Locations"])
        self.get_moves(json_data["Moves"])
        self.get_frontground_size()

    def get_init_world_state(self, locations):
        for location in locations:
            characters = None
            items = None

            if self.CHARACTERS_KEY in location:
                characters = self.get_characters(location[self.CHARACTERS_KEY])

            if self.ITEMS_KEY in location:
                items = self.get_items(location[self.ITEMS_KEY])

            self.world_locations[location["Id"]] = LocationDTO(location["Id"], location["Name"], characters, items)

    def get_moves(self, moves):
        objects = ObjectType()

        for move in moves:
            characters = []
            items = []
            locations = []
            title = move["ProductionTitle"].split("/")[0]
            nodes = move["LSMatching"]

            for node in nodes:
                type = objects.define_object_type(node[self.NODE_NAME_KEY])

                if type == self.CHARACTER_TYPE:
                    characters.append(self.world_characters[f"{node[self.NODE_ID_KEY]}"])
                elif type == self.ITEM_TYPE:
                    items.append(node[self.NODE_NAME_KEY])
                else:
                    locations.append(self.world_locations[f"{node[self.NODE_ID_KEY]}"])

            new_move = MoveDTO(title, locations, characters, items)
            self.moves.append(new_move)

            if "Turning a dead" in new_move.title:
                tmp = move["ModifiedNodesNames"]
                new_items = []

                for item in tmp:
                    if item != locations[0].name:
                        new_items.append(item)

                self.update_world_after_move(new_move, new_items)
            else:
                self.update_world_after_move(new_move)

    def get_frontground_size(self):
        front_data = read_file.read_json_file(f"{self.SIZE_FILE_PATH}/frontground_size.json")

        for front in front_data:
            frontground = FrontgroundDTO(front[self.WIDTH_KEY], front[self.HEIGHT_KEY], front[self.CENTER_X_KEY],
                                         front[self.CENTER_Y_KEY], front[self.IMAGE_X_KEY], front[self.IMAGE_Y_KEY])
            self.frontground_data[front["name"]] = frontground

    def get_characters(self, characters_path):
        characters = []

        for character in characters_path:
            items = None
            name = character["Name"]
            character_id = character["Id"]

            if self.ITEMS_KEY in character:
                items = self.get_items(character[self.ITEMS_KEY])

            character_to_add = CharacterDTO(character_id, name, items)
            self.world_characters[character_id] = character_to_add
            characters.append(character_to_add)

        return characters

    def get_items(self, items_path):
        items = []

        for item in items_path:
            items.append(item["Name"])

        return items

    def update_world_after_move(self, move, new_item_name=None):
        for action in self.action_result_json:
            if action["title"] in move.title:
                modifications = action["instructions"]

                for modification in modifications:
                    node = self.read_attribute(move, modification, "node")
                    source = self.read_attribute(move, modification, "from")
                    target = self.read_attribute(move, modification, "to")
                    self.update_world_modification(modification["op"], node, source, target, new_item_name)

                break

    def update_world_modification(self, operator, node, source=None, target=None, new_items=None):
        node_type = type(node)
        if operator == "move":
        #TODO check fight with character's escape, if removing item from characters, remove it also from location.character
            if node_type == CharacterDTO:
                source.characters.remove(node)
                target.characters.append(node)
            elif node_type == str:
                source.items.remove(node)
                target.items.append(node)
        elif operator == "delete":
            if node_type == str:
                source.items.remove(node)
            elif node_type == CharacterDTO:
                source.characters.remove(node)
        elif operator == "create":
            try:
                target.items.extend(new_items)
            except AttributeError:
                target.items = new_items

    def read_attribute(self, move, modification, node_name):
        try:
            path = modification[node_name]
            path_parts = re.split(self.PATH_REGEX, path)
            tmp = move
            for part in path_parts:
                if len(part) == 1:
                    tmp = tmp[int(part)]
                elif len(part) > 1:
                    tmp = getattr(tmp, part)

            return tmp
        except (KeyError, AttributeError):
            return None


# def main():
#     json_operation = JsonOperation()
#     json_operation.prepare_data_for_animation("./../productions/gameplay.json")
#
#
# if __name__ == "__main__":
#     main()
