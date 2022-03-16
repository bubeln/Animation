import packages as read_file
from dto.character_dto import CharacterDTO
from dto.frontground_dto import FrontgroundDTO
from dto.item_dto import ItemDTO
from dto.location_dto import LocationDTO
from dto.move_dto import MoveDTO
from helpers.common_variables import CommonVariables
from helpers.object_type import ObjectType


class JsonOperation(CommonVariables):

    def __init__(self):
        self.characters_dic = {}
        self.moves = []
        self.world_characters = []
        self.world_locations = []
        self.frontground_data = {}

    def prepare_data_for_animation(self, file_path):
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

            self.world_locations.append(LocationDTO(location["Id"], location["Name"], characters, items))

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
                    characters.append(CharacterDTO(node[self.NODE_ID_KEY], node[self.NODE_NAME_KEY]))
                elif type == self.ITEM_TYPE:
                    items.append(ItemDTO(node[self.NODE_ID_KEY], node[self.NODE_NAME_KEY]))
                else:
                    locations.append(LocationDTO(node[self.NODE_ID_KEY], node[self.NODE_NAME_KEY]))

            self.moves.append(MoveDTO(title, locations, characters, items))

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
            id = character["Id"]

            if self.ITEMS_KEY in character:
                items = self.get_items(character[self.ITEMS_KEY])

            character_to_add = CharacterDTO(id, name, items)
            self.world_characters.append(character_to_add)
            self.characters_dic[id] = name
            characters.append(character_to_add)

        return characters

    def get_items(self, items_path):
        items = []

        for item in items_path:
            items.append(ItemDTO(item["Id"], item["Name"]))

        return items


# def main():
#     json_operation = JsonOperation()
#     json_operation.prepare_data_for_animation("./../productions/gameplay.json")
#
#
# if __name__ == "__main__":
#     main()
