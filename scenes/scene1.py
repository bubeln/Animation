import arcade as ac


class Scene1(ac.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.background = None
        self.set_location(1, 25)
        self.character_list = ac.SpriteList()
        self.objects_list = ac.SpriteList()
        self.front_object_list = ac.SpriteList()
        self.sign_sprite = None
        self.front_object_sprite = None
        self.main_character_sprite = None

    def setup(self):
        self.background = ac.load_texture("../graphics/backgrounds/back/Forest_back.png", width=1004, height=754)
        self.front_object_sprite = ac.Sprite("../graphics/backgrounds/front/Forest_front.png", center_x=500,
                                             center_y=55, image_x=0, image_y=0, image_width=1005, image_height=182)
        self.front_object_list.append(self.front_object_sprite)

        self.sign_sprite = ac.Sprite("./../graphics/objects/sign.png", center_x=950, center_y=95, image_x=0, image_y=0,
                                     image_width=988, image_height=1066, scale=0.1, hit_box_algorithm="Detailed")
        self.objects_list.append(self.sign_sprite)

        self.main_character_sprite = ac.AnimatedTimeBasedSprite("./../graphics/characters/main_hero/main_hero_walk_r.png",
                                                                center_x=50, center_y=190, image_x=0, image_y=0,
                                                                image_width=300, image_height=600, scale=0.5)

        for i in range(6):
            texture = ac.load_texture("./../graphics/characters/main_hero/main_hero_walk_r.png", i*302, 0, 302, 600)
            self.main_character_sprite.frames.append(ac.AnimationKeyframe(i, 100, texture))

        self.character_list.append(self.main_character_sprite)

    def on_draw(self):
        ac.start_render()
        ac.draw_lrwh_rectangle_textured(0, 0, 1000, 720, self.background)
        self.objects_list.draw()
        self.character_list.draw()
        self.front_object_list.draw()

    def on_update(self, delta_time):
        self.main_character_sprite.center_x += 1
        self.character_list.update_animation()

        try:
            character_sign_collision = ac.check_for_collision(self.main_character_sprite, self.sign_sprite)

            if character_sign_collision:

                self.objects_list.remove(self.sign_sprite)
                self.front_object_list.remove(self.front_object_sprite)
                self.front_object_sprite = ac.Sprite("../graphics/backgrounds/front/Tavern_front.png", center_x=500,
                                                     center_y=50, image_x=0, image_y=0, image_width=1010,
                                                     image_height=163)
                self.front_object_list.append(self.front_object_sprite)

                self.background = ac.load_texture("../graphics/backgrounds/back/Tavern_back.png", width=1013, height=758)
                ac.draw_lrwh_rectangle_textured(0, 0, 1000, 720, self.background)

                self.main_character_sprite.center_x = 80
        except ValueError:
            pass


def main():
    window = Scene1(1000, 720, "Scene no. 1")
    window.setup()
    ac.run()


if __name__ == "__main__":
    main()
