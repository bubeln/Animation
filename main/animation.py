from helpers.common_variables import CommonVariables
from helpers.json_operations import JsonOperation
from scene_controller import SceneController


class Animation(CommonVariables):

    def __init__(self):
        self.json_operation = JsonOperation()
        self.json_operation.prepare_data_for_animation(self.GAMEPLAY_PATH)
        self.scene_controller = SceneController(self.SCENE_WIDTH, self.SCENE_HEIGHT)

    def generate_animation(self):
        for move in self.json_operation.moves:
            #TODO usunąć bohaterów biorących udziałw akcji z lokalizacji (tylko dla tego ruchu, nie dla świata)
            self.setup_scene(move)
            self.scene_controller.run()
            self.scene_controller.switch_to()

    def setup_scene(self, move):
        try:
            location = self.json_operation.frontground_data[move.locations[0].name]
        except KeyError:
            location = None

        if len(move.locations) == 2:
            try:
                second_location = self.json_operation.frontground_data[move.locations[1].name]
            except KeyError:
                second_location = None

            self.scene_controller.setup(location, move.locations[0].name, move.characters, move.title,
                                        second_location, move.locations[1].name)
        else:
            self.scene_controller.setup(location, move.locations[0].name, move.characters, move.title)


def main():
    animation = Animation()
    animation.generate_animation()


if __name__ == "__main__":
    main()
