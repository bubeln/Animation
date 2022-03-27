import arcade as ac
from helpers.common_variables import CommonVariables


class SceneController(ac.Window, CommonVariables):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.set_location(1, 25)
        self.j = 0
        self.background = None
        self.character_sprite = None
        self.front_object_sprite = None
        self.item_sprite = None
        self.second_location = None
        self.second_location_name = None
        self.text = ""
        self.characters_list = ac.SpriteList()
        self.front_objects_list = ac.SpriteList()
        self.objects_list = ac.SpriteList()

    #TODO add items to setup
    #TODO display location items and characters without characters taking action
    def setup(self, location, location_name, characters, title, second_location=None, second_location_name=None):
        self.j = 0
        self.background = ac.load_texture(f"{self.BACKGROUND_PATH}/back/{location_name}_back.png",
                                          width=self.BACKGROUND_WIDTH, height=self.BACKGROUND_HEIGHT)
        self.text = title

        if second_location_name:
            self.second_location = second_location
            self.second_location_name = second_location_name

        if location:
            self.load_front_object(location_name, location)

        self.load_characters(characters)

    def load_front_object(self, location_name, location):
        self.front_object_sprite = ac.Sprite(f"{self.BACKGROUND_PATH}/front/{location_name}_front.png",
                                             center_x=location.center_x, center_y=location.center_y,
                                             image_x=location.image_x, image_y=location.image_y,
                                             image_width=location.width, image_height=location.height)
        self.front_objects_list.append(self.front_object_sprite)

    def load_characters(self, characters):
        for character in characters:
            #TODO load AnimatedTimeBasedSprite and moves
            if character.name == "Sheep":
                width = 1446
                height = 1060
            else:
                width = self.CHARACTER_WIDTH
                height = self.CHARACTER_HEIGHT
            self.character_sprite = ac.Sprite(f"{self.CHARACTER_PATH}/{character.name}/{character.name}.png",
                                              center_x=50, center_y=190, image_x=0, image_y=0,
                                              image_width=width, image_height=height, scale=0.1)
            self.characters_list.append(self.character_sprite)

    def on_draw(self):
        ac.start_render()
        if self.background is None:
            ac.draw_lrtb_rectangle_filled(0, self.SCENE_WIDTH, self.SCENE_HEIGHT, 0, ac.color.BLACK)
            ac.draw_text("Loading", 200, 200, font_size=15)
        else:
            ac.draw_lrwh_rectangle_textured(0, 0, self.SCENE_WIDTH, self.SCENE_HEIGHT, self.background)
            ac.draw_text(self.text, 200, 200, font_size=15)
        self.characters_list.draw()
        self.front_objects_list.draw()
        ac.finish_render()

    #TODO add moving characters
    def on_update(self, delta_time):
        self.j += 1

        if self.j == 50 and "Location change" in self.text:
            self.front_objects_list = ac.SpriteList()
            self.background = ac.load_texture(f"{self.BACKGROUND_PATH}/back/{self.second_location_name}_back.png",
                                              width=self.BACKGROUND_WIDTH, height=self.BACKGROUND_HEIGHT)
            if self.second_location:
                self.load_front_object(self.second_location_name, self.second_location)

        elif self.j == 100:
            self.front_objects_list = ac.SpriteList()
            self.characters_list = ac.SpriteList()
            self.background = None
            ac.draw_lrtb_rectangle_filled(0, self.SCENE_WIDTH, self.SCENE_HEIGHT, 0, ac.color.BLACK)

        elif self.j == 110:
            ac.exit()
