import arcade as ac
import PIL.Image as pim
import packages as read_file
from data.common_variables import CommonVariables
from helpers.png_file_generator import PNGFileGenerator


class SceneController(ac.Window, CommonVariables):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.set_location(1, 25)
        self.action = None
        self.action_list = None
        self.animation_break = 100
        self.background = None
        self.characters_list = ac.SpriteList()
        self.character_sprite = None
        self.frame = 0
        self.front_objects_list = ac.SpriteList()
        self.front_object_sprite = None
        self.initial_center_x = 0
        self.item_sprite = None
        self.items_list = ac.SpriteList()
        self.second_location_front_objects = None
        self.second_location = None
        self.title = ""
        self.update_center_x = 0

    def setup(self, location_front_object, location, characters, title, items=None, second_location_front_object=None,
              second_location=None):
        self.frame = 0
        self.background = ac.load_texture(f"{self.BACKGROUND_PATH}/back/{location.name}_back.png",
                                          width=self.BACKGROUND_WIDTH, height=self.BACKGROUND_HEIGHT)
        self.title = title

        if second_location:
            self.second_location_front_objects = second_location_front_object
            self.second_location = second_location

        if location_front_object:
            self.load_front_object(location.name, location_front_object)

        if title in self.ANIMATED_ACTIONS:
            self.load_animation(title, characters, items)
            self.load_characters(list(location.characters.values()))
            self.load_location_items(location.items)
        else:
            self.load_characters(characters + list(location.characters.values()))
            self.load_location_items(location.items, items)

    def on_draw(self):
        ac.start_render()

        if self.background is None:
            ac.draw_lrtb_rectangle_filled(0, self.SCENE_WIDTH, self.SCENE_HEIGHT, 0, ac.color.BLACK)
            ac.draw_text("Loading", 200, 200, font_size=15)
        else:
            ac.draw_lrwh_rectangle_textured(0, 0, self.SCENE_WIDTH, self.SCENE_HEIGHT, self.background)
            ac.draw_text(self.title, 300, 600, font_size=15)

        self.characters_list.draw()
        self.items_list.draw()

        if self.action_list:
            self.action_list.draw()

        self.front_objects_list.draw()
        ac.finish_render()

    def on_update(self, delta_time):
        self.frame += 1

        if self.action_list:
            self.action.center_x += self.update_center_x
            self.action_list.update_animation()

        if self.frame == int(self.animation_break * 2 / 3) and "Location change" in self.title:
            self.front_objects_list = ac.SpriteList()
            self.background = ac.load_texture(f"{self.BACKGROUND_PATH}/back/{self.second_location.name}_back.png",
                                              width=self.BACKGROUND_WIDTH, height=self.BACKGROUND_HEIGHT)
            if self.second_location_front_objects:
                self.load_front_object(self.second_location.name, self.second_location_front_objects)

            self.action.center_x = self.initial_center_x
            self.characters_list = ac.SpriteList()
            self.load_characters(list(self.second_location.characters.values()))
            self.characters_list.draw()
            self.load_location_items(self.second_location.items)

        elif self.frame == self.animation_break:
            self.draw_loading_view()
        elif self.frame == (self.animation_break + 10):
            self.clean_data_and_exit_view()

    def load_front_object(self, location_name, location_front):
        self.front_object_sprite = ac.Sprite(f"{self.BACKGROUND_PATH}/front/{location_name}_front.png",
                                             center_x=location_front.center_x, center_y=location_front.center_y,
                                             image_x=location_front.image_x, image_y=location_front.image_y,
                                             image_width=location_front.width, image_height=location_front.height)
        self.front_objects_list.append(self.front_object_sprite)

    def load_animation(self, title, characters, item=None):
        actions = read_file.read_json_file(f"{self.DATA_PATH}/action_data.json")

        for action in actions:
            if action["action"] == title:
                action_data = self.get_action_data(action)
                file_path = self.get_animation_file(action_data["action_type"], action_data["template"], characters,
                                                    item)
                action_file = pim.open(file_path)
                height, width = self.get_image_size(action["x"], action_file, action_data["frames"])
                self.action_list = ac.SpriteList()
                self.action = ac.AnimatedTimeBasedSprite(file_path, center_x=action[self.CENTER_X_KEY],
                                                         center_y=action[self.CENTER_Y_KEY], image_x=0, image_y=0,
                                                         image_width=width, image_height=height,
                                                         scale=action_data["scale"])

                if action["x"] == 0:
                    for i in range(action_data["frames"]):
                        texture = ac.load_texture(file_path, x=0, y=i * height, width=width, height=height)
                        self.action.frames.append(ac.AnimationKeyframe(i, action_data["duration"], texture))
                else:
                    for i in range(action_data["frames"]):
                        texture = ac.load_texture(file_path, x=i*width, y=0, width=width, height=height)
                        self.action.frames.append(ac.AnimationKeyframe(i, action_data["duration"], texture))

                self.action_list.append(self.action)
                break

    def load_characters(self, characters):
        i = 0

        for character in characters:
            character_image = pim.open(f"{self.CHARACTERS_LIST_PATH}/{character.name}/{character.name}.png")
            width = character_image.width
            height = character_image.height
            center_x = 0.5 * width * self.SCALE + 10 + i
            i += width * self.SCALE + 10
            self.character_sprite = ac.Sprite(character_image.filename, center_x=center_x, center_y=300, image_x=0,
                                              image_y=0, image_width=width, image_height=height, scale=self.SCALE)
            self.characters_list.append(self.character_sprite)
            self.load_character_items(character, center_x, width)

    def load_location_items(self, location_items, action_items=None):
        if action_items and location_items:
            items = location_items + action_items
        elif location_items:
            items = location_items
        elif action_items:
            items = action_items
        else:
            items = []

        i = 0

        for item in items:
            image = pim.open(f"{self.OBJECT_PATH}/{item}.png")
            center_x = 0.5 * image.width * self.ITEM_SCALE + 10 + i
            i += image.width * self.ITEM_SCALE + 10
            self.item_sprite = ac.Sprite(image.filename, center_x=center_x, center_y=100,
                                         image_x=0, image_y=0, image_width=image.width, image_height=image.height,
                                         scale=self.ITEM_SCALE)
            self.items_list.append(self.item_sprite)

    def load_character_items(self, character, center_x, width):
        k = 0

        try:
            for item in character.items:
                image = pim.open(f"{self.OBJECT_PATH}/{item}.png")
                center_x += (0.5 * width * self.SCALE) + (0.5 * image.width * self.ITEM_SCALE) - 10
                center_y = 190 + (k * 50)
                self.character_sprite = ac.Sprite(image.filename, center_x=center_x, center_y=center_y,
                                                  image_x=0, image_y=0, image_width=image.width,
                                                  image_height=image.height, scale=self.ITEM_SCALE)
                self.characters_list.append(self.character_sprite)
                k += 1
        except TypeError:
            print(f"Character {character.name} has no own items")

    def get_action_data(self, action):
        action_data = {
            "action_type": action["type"],
            "duration": action["duration"],
            "frames": action["frames"],
            "repeat": action["repeat"],
            "scale": action["scale"],
            "template": action["template"]
        }

        self.update_center_x = action["move_x"]
        self.animation_break = action_data["repeat"] * action_data["duration"]
        self.initial_center_x = action["center_x"]

        return action_data

    def get_animation_file(self, action_type, template, characters, item=None):
        if action_type == "one_character":
            file_path = PNGFileGenerator().generate_png_one_character(template, characters[0].name.lower())
        elif action_type == "two_characters":
            file_path = PNGFileGenerator().generate_png_two_characters(template, characters[0].name.lower(),
                                                                       characters[0].name.lower())
        elif action_type == "two_characters_one_item":
            file_path = PNGFileGenerator().generate_png_two_characters_one_item(template,
                                                                                characters[0].name.lower(),
                                                                                characters[0].name.lower(), item)

        return file_path

    def get_image_size(self, x, action_file, frames):
        if x == 0:
            height = action_file.height / frames
            width = action_file.width
        else:
            height = action_file.height
            width = action_file.width / frames

        return height, width

    def draw_loading_view(self):
        self.front_objects_list = ac.SpriteList()
        self.characters_list = ac.SpriteList()
        self.items_list = ac.SpriteList()
        self.background = None
        self.action_list = None
        ac.draw_lrtb_rectangle_filled(0, self.SCENE_WIDTH, self.SCENE_HEIGHT, 0, ac.color.BLACK)

    def clean_data_and_exit_view(self):
        self.update_center_x = 0
        self.animation_break = 100
        self.initial_center_x = 0
        ac.exit()
