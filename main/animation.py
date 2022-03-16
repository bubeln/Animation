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
            try:
                location = self.json_operation.frontground_data[move.locations[0].name]
            except KeyError:
                location = None

            self.scene_controller.setup(location, move.locations[0].name, move.characters, move.title)
            self.scene_controller.run()
            self.scene_controller.switch_to()

        #TODO uaktualnianie swiata po akcji

def main():
    animation = Animation()
    animation.generate_animation()


if __name__ == "__main__":
    main()
