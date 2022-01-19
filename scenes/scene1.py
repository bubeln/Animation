import arcade as ac


class Scene1(ac.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.background = None
        self.set_location(1, 25)
        self.character_list = ac.SpriteList()
        self.main_character_sprite = None

    def setup(self):
        self.background = ac.load_texture("./../graphics/backgrounds/Forest.png", width=400, height=300)
        self.main_character_sprite = ac.AnimatedTimeBasedSprite("./../graphics/characters/main_hero/main_hero_walk_r.png",
                                                                center_x=50, center_y=170, image_x=0, image_y=0,
                                                                image_width=300, image_height=600, scale=0.4)

        for i in range(6):
            texture = ac.load_texture("./../graphics/characters/main_hero/main_hero_walk_r.png", i*302, 0, 302, 600)
            self.main_character_sprite.frames.append(ac.AnimationKeyframe(i, 100, texture))

        self.character_list.append(self.main_character_sprite)

    def on_draw(self):
        ac.start_render()
        ac.draw_lrwh_rectangle_textured(0, 0, 800, 600, self.background)
        self.character_list.draw()

    def on_update(self, delta_time):
        self.main_character_sprite.center_x += 1
        self.character_list.update_animation()


def main():
    window = Scene1(800, 600, "Scene no. 1")
    window.setup()
    ac.run()


if __name__ == "__main__":
    main()
