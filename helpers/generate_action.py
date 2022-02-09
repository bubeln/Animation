import cairosvg
import os.path
import pysvg.parser as pyp


class GenerateAction:

    def generate_action_one_character(self, action, character):
        bb = self.check_if_action_exist(self, action, character)
        self.character_folder_path = f"./../graphics/characters/{character}"
        template = pyp.parse(f"./../graphics/actions_template/{action}.svg")
        phases_amount = len(template._subElements)
        character_parts = self.get_character_parts(self, character)

        for part in character_parts:
            part_svg = pyp.parse(f"{self.character_folder_path}/{character}_{part}.svg")
            part_to_paste = part_svg.getElementAt(1).getElementAt(0)
            part_group_number = len(part_to_paste._subElements)

            for i in range(1, phases_amount):
                phase = template.getElementAt(i)
                place_to_paste = phase.getElementByID(part)[0].getElementAt(0)

                for j in range(part_group_number):
                    place_to_paste.addElement(part_to_paste.getElementAt(j))

        new_action_path = f"{self.character_folder_path}/{character}_{action}"
        template.save(f"{new_action_path}.svg")
        file = open(f"{new_action_path}.svg", "r")
        cairosvg.svg2png(file_obj=file, write_to=f"{new_action_path}.png")
        file.close()

    def get_character_parts(self, character):
        list_file = open(f"{self.character_folder_path}/{character}_parts.txt", "r")
        parts_list = list_file.read().splitlines()
        list_file.close()

        return parts_list

    def check_if_action_exist(self, action, character):
        return os.path.isfile(f"./../graphics/characters/{character}/{character}_{action}.png")


GenerateAction.generate_action_one_character(GenerateAction, "walk1", "my_hero")
