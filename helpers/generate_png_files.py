import cairosvg
import os.path
import pysvg.parser as pyp
import pysvg.structure


class GeneratePNGFiles:
    ACTIONS_TEMPLATE_PATH = "./../graphics/actions_template"
    CHARACTERS_PATH = "./../graphics/characters"
    ITEM_PATH = "./../graphics/objects"

    #TODO check if works after refactor
    def generate_png_one_character(self, action, character):
        #TODO odbij obiekt poziomo jeżeli chodzenie
        #TODO check if file exists

        # bb = self.check_if_action_exist(action, character)
        character_folder_path = f"{self.CHARACTERS_PATH}/{character}"
        template = pyp.parse(f"{self.ACTIONS_TEMPLATE_PATH}/{action}.svg")
        phases_amount = len(template._subElements)

        self.paste_character_parts_to_template(character, phases_amount, template)

        new_action_path = f"{character_folder_path}/{character}_{action}"
        template.save(f"{new_action_path}.svg")
        file = open(f"{new_action_path}.svg", "r")
        cairosvg.svg2png(file_obj=file, write_to=f"{new_action_path}.png", dpi=50)
        file.close()

    def generate_png_two_character(self, action, f_character, s_character):
        #TODO check if file exists
        # bb = self.check_if_action_two_exist(action, f_character, s_character)
        f_character_folder_path = f"{self.CHARACTERS_PATH}/{f_character}"
        template = pyp.parse(f"{self.ACTIONS_TEMPLATE_PATH}/{action}.svg")
        phases_amount = len(template._subElements)

        self.paste_character_parts_to_template(f_character, phases_amount, template, "f_character")
        self.paste_character_parts_to_template(s_character, phases_amount, template, "s_character")

        new_action_path = f"{f_character_folder_path}/{f_character}_{s_character}_{action}"
        template.save(f"{new_action_path}.svg")
        file = open(f"{new_action_path}.svg", "r")
        cairosvg.svg2png(file_obj=file, write_to=f"{new_action_path}.png", dpi=50)
        file.close()

    def generate_png_two_character_one_item(self, action, f_character, s_character, item):
        #TODO check if file exists
        # bb = self.check_if_action_two_exist(action, f_character, s_character)
        f_character_folder_path = f"{self.CHARACTERS_PATH}/{f_character}"
        template = pyp.parse(f"{self.ACTIONS_TEMPLATE_PATH}/{action}.svg")
        phases_amount = len(template._subElements)

        self.paste_character_parts_to_template(f_character, phases_amount, template, "f_character")
        self.paste_character_parts_to_template(s_character, phases_amount, template, "s_character")
        self.paste_item_to_template(item, phases_amount, template)

        new_action_path = f"{f_character_folder_path}/{f_character}_{s_character}_{item}_{action}"
        template.save(f"{new_action_path}.svg")
        file = open(f"{new_action_path}.svg", "r")
        cairosvg.svg2png(file_obj=file, write_to=f"{new_action_path}.png", dpi=50)
        file.close()

    def check_if_action_exist(self, action, character):
        return os.path.isfile(f"{self.CHARACTERS_PATH}/{character}/{character}_{action}.png")

    def check_if_action_two_exist(self, action, f_character, s_character):
        return os.path.isfile(f"{self.CHARACTERS_PATH}/{f_character}/{f_character}_{s_character}_{action}.png")

    def paste_character_parts_to_template(self, character, phases_amount, template, character_key=None):
        character_folder_path = f"{self.CHARACTERS_PATH}/{character}"
        character_parts = self.get_character_parts(character, character_folder_path)

        for part in character_parts:
            part_svg = pyp.parse(f"{character_folder_path}/{character}_{part}.svg")
            part_to_paste = part_svg.getElementAt(1).getElementAt(0)
            part_group_number = len(part_to_paste._subElements)

            for i in range(1, phases_amount):
                phase = template.getElementAt(i)

                if character_key is None:
                    place_to_paste = phase.getElementByID(part)[0].getElementAt(0)
                else:
                    place_to_paste = phase.getElementByID(character_key)[0].getElementByID(part)[0].getElementAt(0)
                    if not isinstance(place_to_paste, pysvg.structure.G):
                        place_to_paste = phase.getElementByID(character_key)[0].getElementByID(part)[0].getElementAt(1)

                try:
                    place_to_paste.getAttributes()["transform"] = part_to_paste.getAttributes()["transform"]
                except KeyError:
                    print(f"Part {part} has no own transform to paste to template file")

                for j in range(part_group_number):
                    place_to_paste.addElement(part_to_paste.getElementAt(j))

    def paste_item_to_template(self, item, phases_amount, template):
        item_svg = pyp.parse(f"{self.ITEM_PATH}/{item}.svg")
        item_to_paste = item_svg.getElementAt(1).getElementAt(0)
        item_group_number = len(item_to_paste._subElements)

        for i in range(1, phases_amount):
            phase = template.getElementAt(i)
            place_to_paste = phase.getElementByID("item")[0].getElementAt(0)

            try:
                place_to_paste.getAttributes()["transform"] = item_to_paste.getAttributes()["transform"]
            except KeyError:
                print(f"Item {item} has no own transform to paste to template file")

            for j in range(item_group_number):
                place_to_paste.addElement(item_to_paste.getElementAt(j))

    def get_character_parts(self, character, folder_path):
        list_file = open(f"{folder_path}/{character}_parts.txt", "r")
        parts_list = list_file.read().splitlines()
        list_file.close()

        return parts_list


# GeneratePNGFiles().generate_png_one_character("walking", "merchant")
GeneratePNGFiles().generate_png_two_character_one_item("buy-sell 2", "main_hero", "main_hero", "flakon")
# GeneratePNGFiles().generate_png_two_character("fight_running", "main_hero", "common_man")
# GeneratePNGFiles().generate_png_two_character("fight_death", "main_hero", "main_hero")
