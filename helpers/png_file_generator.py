import cairosvg
import os.path
import pysvg.parser as pyp
import pysvg.structure
from data.common_variables import CommonVariables


class PNGFileGenerator(CommonVariables):

    def generate_png_one_character(self, action, character):
        file_exists = self.check_if_png_one_character_exists(action, character)

        if not file_exists:
            character_folder_path = f"{self.CHARACTERS_LIST_PATH}/{character}"
            template = pyp.parse(f"{self.ACTIONS_TEMPLATE_PATH}/{action}.svg")
            phases_amount = len(template._subElements)

            self.paste_character_parts_to_template(character, phases_amount, template)

            new_action_path = f"{character_folder_path}/{character}_{action}"
            template.save(f"{new_action_path}.svg")
            file = open(f"{new_action_path}.svg", "r")
            cairosvg.svg2png(file_obj=file, write_to=f"{new_action_path}.png", dpi=50)

            file.close()

        return f"{self.CHARACTERS_LIST_PATH}/{character}/{character}_{action}.png"

    def generate_png_two_characters(self, action, first_character, second_character):
        file_exists = self.check_if_png_two_characters_exists(action, first_character, second_character)

        if not file_exists:
            first_character_folder_path = f"{self.CHARACTERS_LIST_PATH}/{first_character}"
            template = pyp.parse(f"{self.ACTIONS_TEMPLATE_PATH}/{action}.svg")
            phases_amount = len(template._subElements)

            self.paste_character_parts_to_template(first_character, phases_amount, template, "f_character")
            self.paste_character_parts_to_template(second_character, phases_amount, template, "s_character")

            new_action_path = f"{first_character_folder_path}/{first_character}_{second_character}_{action}"
            template.save(f"{new_action_path}.svg")
            file = open(f"{new_action_path}.svg", "r")
            cairosvg.svg2png(file_obj=file, write_to=f"{new_action_path}.png", dpi=50)
            file.close()

        return f"{self.CHARACTERS_LIST_PATH}/{first_character}/{first_character}_{second_character}_{action}.png"

    def generate_png_two_characters_one_item(self, action, first_character, second_character, item):
        file_exists = self.check_if_png_two_characters_exists(action, first_character, second_character)

        if not file_exists:
            first_character_folder_path = f"{self.CHARACTERS_LIST_PATH}/{first_character}"
            template = pyp.parse(f"{self.ACTIONS_TEMPLATE_PATH}/{action}.svg")
            phases_amount = len(template._subElements)

            self.paste_character_parts_to_template(first_character, phases_amount, template, "f_character")
            self.paste_character_parts_to_template(second_character, phases_amount, template, "s_character")
            self.paste_item_to_template(item, phases_amount, template)

            new_action_path = f"{first_character_folder_path}/{first_character}_{second_character}_{item}_{action}"
            template.save(f"{new_action_path}.svg")
            file = open(f"{new_action_path}.svg", "r")
            cairosvg.svg2png(file_obj=file, write_to=f"{new_action_path}.png", dpi=50)
            file.close()

        return f"{self.CHARACTERS_LIST_PATH}/{first_character}/{first_character}_{second_character}_{action}.png"

    def check_if_png_one_character_exists(self, action, character):
        return os.path.isfile(f"{self.CHARACTERS_LIST_PATH}/{character}/{character}_{action}.png")

    def check_if_png_two_characters_exists(self, action, first_character, second_character):
        return os.path.isfile(f"{self.CHARACTERS_LIST_PATH}/{first_character}/"
                              f"{first_character}_{second_character}_{action}.png")

    def paste_character_parts_to_template(self, character, phases_amount, template, character_key=None):
        character_folder_path = f"{self.CHARACTERS_LIST_PATH}/{character}"
        character_parts = self.get_character_parts()

        for part in character_parts:
            part_svg = pyp.parse(f"{character_folder_path}/{character}_{part}.svg")
            elements_to_paste = part_svg.getElementAt(1).getElementAt(0)
            elements_amount = len(elements_to_paste._subElements)

            for i in range(1, phases_amount):
                phase = template.getElementAt(i)

                if character_key is None:
                    place_to_paste = phase.getElementByID(part)[0].getElementAt(0)
                else:
                    place_to_paste = phase.getElementByID(character_key)[0].getElementByID(part)[0].getElementAt(0)
                    if not isinstance(place_to_paste, pysvg.structure.G):
                        place_to_paste = phase.getElementByID(character_key)[0].getElementByID(part)[0].getElementAt(1)

                try:
                    place_to_paste.getAttributes()["transform"] = elements_to_paste.getAttributes()["transform"]
                except KeyError:
                    print(f"Part {part} has no own transform to paste to template file")

                for j in range(elements_amount):
                    place_to_paste.addElement(elements_to_paste.getElementAt(j))

    def paste_item_to_template(self, item, phases_amount, template):
        item_svg = pyp.parse(f"{self.OBJECT_PATH}/{item}.svg")
        elements_to_paste = item_svg.getElementAt(1).getElementAt(0)
        elements_amount = len(elements_to_paste._subElements)

        for i in range(1, phases_amount):
            phase = template.getElementAt(i)
            place_to_paste = phase.getElementByID("item")[0].getElementAt(0)

            try:
                place_to_paste.getAttributes()["transform"] = elements_to_paste.getAttributes()["transform"]
            except KeyError:
                print(f"Item {item} has no own transform to paste to template file")

            for j in range(elements_amount):
                place_to_paste.addElement(elements_to_paste.getElementAt(j))

    def get_character_parts(self):
        list_file = open(f"{self.DATA_PATH}/character_body_parts.txt", "r")
        parts_list = list_file.read().splitlines()
        list_file.close()

        return parts_list
