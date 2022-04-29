import arcade as ac
from data.common_variables import CommonVariables


class SceneController(ac.Window, CommonVariables):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.set_location(1, 25)
        self.j = 0
        self.action_characters = None
        self.background = None
        self.character_sprite = None
        self.front_object_sprite = None
        self.item_sprite = None
        self.second_location_front = None
        self.second_location = None
        self.text = ""
        self.characters_list = ac.SpriteList()
        self.front_objects_list = ac.SpriteList()
        self.objects_list = ac.SpriteList()

    #TODO display characters' items
    def setup(self, location_front, location, characters, title, items=None, second_location_front=None,
              second_location=None):
        self.j = 0
        self.background = ac.load_texture(f"{self.BACKGROUND_PATH}/back/{location.name}_back.png",
                                          width=self.BACKGROUND_WIDTH, height=self.BACKGROUND_HEIGHT)
        self.text = title

        if second_location:
            self.second_location_front = second_location_front
            self.second_location = second_location
            self.action_characters = characters

        if location_front:
            self.load_front_object(location.name, location_front)

        self.load_characters(characters + list(location.characters.values()))
        self.load_items(items)

    def load_front_object(self, location_name, location_front):
        self.front_object_sprite = ac.Sprite(f"{self.BACKGROUND_PATH}/front/{location_name}_front.png",
                                             center_x=location_front.center_x, center_y=location_front.center_y,
                                             image_x=location_front.image_x, image_y=location_front.image_y,
                                             image_width=location_front.width, image_height=location_front.height)
        self.front_objects_list.append(self.front_object_sprite)

    def load_characters(self, characters):
        i = 0

        for character in characters:
             #TODO load AnimatedTimeBasedSprite and moves
            if character.name == "Sheep":
                width = 1446
                height = 1060
            else:
                width = self.CHARACTER_WIDTH
                height = self.CHARACTER_HEIGHT

            center_x = (i + 0.6) * self.CHARACTER_WIDTH * self.SCALE + (20 * i)
            self.character_sprite = ac.Sprite(f"{self.CHARACTER_PATH}/{character.name}/{character.name}.png",
                                              center_x=center_x, center_y=300, image_x=0, image_y=0,
                                              image_width=width, image_height=height, scale=self.SCALE)
            self.characters_list.append(self.character_sprite)
            i += 1

    def load_items(self, items):
        i = 0

        for item in items:
            width = item.width
            height = item.height
            center_x = (i + 0.6) * width * self.ITEM_SCALE + (70 * i)
            self.item_sprite = ac.Sprite(f"{self.OBJECT_PATH}/{item.name}.png", center_x=center_x, center_y=100,
                                         image_x=0, image_y=0, image_width=width, image_height=height,
                                         scale=self.ITEM_SCALE)
            self.objects_list.append(self.item_sprite)
            i += 1

    def on_draw(self):
        ac.start_render()
        if self.background is None:
            ac.draw_lrtb_rectangle_filled(0, self.SCENE_WIDTH, self.SCENE_HEIGHT, 0, ac.color.BLACK)
            ac.draw_text("Loading", 200, 200, font_size=15)
        else:
            ac.draw_lrwh_rectangle_textured(0, 0, self.SCENE_WIDTH, self.SCENE_HEIGHT, self.background)
            ac.draw_text(self.text, 300, 600, font_size=15)
        self.characters_list.draw()
        self.objects_list.draw()
        self.front_objects_list.draw()
        ac.finish_render()

    #TODO add moving characters
    def on_update(self, delta_time):
        self.j += 1

        if self.j == 50 and "Location change" in self.text:
            self.front_objects_list = ac.SpriteList()
            self.background = ac.load_texture(f"{self.BACKGROUND_PATH}/back/{self.second_location.name}_back.png",
                                              width=self.BACKGROUND_WIDTH, height=self.BACKGROUND_HEIGHT)
            if self.second_location_front:
                self.load_front_object(self.second_location.name, self.second_location_front)

            self.characters_list = ac.SpriteList()
            self.load_characters(self.action_characters + list(self.second_location.characters.values()))
            self.characters_list.draw()

        elif self.j == 100:
            self.front_objects_list = ac.SpriteList()
            self.characters_list = ac.SpriteList()
            self.objects_list = ac.SpriteList()
            self.background = None
            ac.draw_lrtb_rectangle_filled(0, self.SCENE_WIDTH, self.SCENE_HEIGHT, 0, ac.color.BLACK)

        elif self.j == 110:
            ac.exit()
