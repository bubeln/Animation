from data.common_variables import CommonVariables
from helpers.json_operations import JsonOperation
from scene_controller import SceneController


class Animation(CommonVariables):

    def __init__(self):
        self.json_operation = JsonOperation()
        self.json_operation.prepare_data_for_animation(self.GAMEPLAY_PATH)
        self.scene_controller = SceneController(self.SCENE_WIDTH, self.SCENE_HEIGHT)

    def generate_animation(self):
        for move in self.json_operation.moves:
            self.filter_out_characters_and_items_taking_action(move)
            self.setup_scene(move)
            self.scene_controller.run()
            self.scene_controller.switch_to()

            #TODO display the world after last scene

    def filter_out_characters_and_items_taking_action(self, move):
        self.filter_out_characters(move)
        self.filter_out_items(move)

    def setup_scene(self, move):
        items = self.prepare_items_for_animation(move)
        location = self.prepare_location_for_animation(move)

        if len(move.locations) == 2:
            try:
                second_location = self.json_operation.frontground_data[move.locations[1].name]
            except KeyError:
                second_location = None

            self.scene_controller.setup(location, move.locations[0], move.characters, move.title, items,
                                        second_location, move.locations[1])
        else:
            self.scene_controller.setup(location, move.locations[0], move.characters, move.title, items)

    def filter_out_characters(self, move):
        for character in move.characters:
            for item in move.items:
                try:
                    character.items.remove(item)
                except (KeyError, ValueError):
                    print(f"Character {character.id} doesn't have item {item}")
                except AttributeError:
                    print(f"Character {character.id} has no items")
                    break
                    #TODO check which loop end after break
            try:
                del move.locations[0].characters[character.id]
            except KeyError:
                print(f"Character {character.id} is not in location {move.locations[0].id} or was already removed")

    def filter_out_items(self, move):
        for item in move.items:
            try:
                move.locations[0].items.remove(item)
            except (KeyError, ValueError):
                print(f"Item {item} is not in location {move.locations[0].id} or was already removed")
            except AttributeError:
                print(f"Location {move.locations[0].id} has no items")
                break

    def prepare_items_for_animation(self, move):
        try:
            if move.locations[0].items:
                return move.items + move.locations[0].items
            else:
                return move.items
        except KeyError:
            return None

    def prepare_location_for_animation(self, move):
        try:
            location = self.json_operation.frontground_data[move.locations[0].name]
        except KeyError:
            location = None

        return location


def main():
    animation = Animation()
    animation.generate_animation()


if __name__ == "__main__":
    main()
