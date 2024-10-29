import arcade
import random

class Die(arcade.Sprite):
    def __init__(self, scale):
        self.value = 1

        # Set asset based on card value
        self.image_filename = f"assets/board game pieces/PNG/Dice/dieWhite_border{self.value}.png"

        # Call the parent class from Python Arcade
        # super().__init__(self.image_filename, scale, hit_box_algorithm="None")
        super().__init__(self.image_filename, scale, hit_box_algorithm="None", center_x=675, center_y=125)

    def roll(self):
        self.value = random.randint(1, 6)
        self.texture = arcade.load_texture(f"assets/board game pieces/PNG/Dice/dieWhite_border{self.value}.png")