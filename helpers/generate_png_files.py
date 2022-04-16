import cairosvg
import os.path
import pysvg.parser as pyp


class GeneratePNGFiles:

    def generate_png_one_character(self, action, character):
        #TODO odbij obiekt poziomo jeżeli chodzenie
        #TODO check if file exists
        bb = self.check_if_action_exist(action, character)
        self.character_folder_path = f"./../graphics/characters/{character}"
        template = pyp.parse(f"./../graphics/actions_template/{action}.svg")
        phases_amount = len(template._subElements)
        character_parts = self.get_character_parts(character)

        for part in character_parts:
            part_svg = pyp.parse(f"{self.character_folder_path}/{character}_{part}.svg")
            part_to_paste = part_svg.getElementAt(1).getElementAt(0)
            part_group_number = len(part_to_paste._subElements)

            for i in range(1, phases_amount):
                phase = template.getElementAt(i)
                place_to_paste = phase.getElementByID(part)[0].getElementAt(0)

                try:
                    place_to_paste.getAttributes()["transform"] = part_to_paste.getAttributes()["transform"]
                except KeyError:
                    print(f"Part {part} has no own transform to paste to template file")

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


GeneratePNGFiles.generate_png_one_character(GeneratePNGFiles, "walk3", "main_hero")
