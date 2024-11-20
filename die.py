import arcade
import random

class Die(arcade.Sprite):
    def __init__(self, scale):
        # Initialize die value and set initial image filename
        self.value = random.randint(1,6)
        self.final_value = random.randint(1,6)
        self.image_filename = f"assets/board game pieces/PNG/Dice/dieWhite_border{self.value}.png"
        self.roll_counter = 0
        self.is_rolling = False
        super().__init__(self.image_filename, scale, hit_box_algorithm="None", center_x=675, center_y=125)

    def roll(self):
        """
        Start the rolling animation
        """
        self.is_rolling = True
        self.roll_counter = 0
        self.final_value = random.randint(1, 6)

    def update_animation(self):
        """
        Handle the rolling animation and finalize the roll
        """
        if self.is_rolling:
            if self.roll_counter < 6:
                # Set a random face during the roll animation
                self.value = random.randint(1, 6)
                self.texture = arcade.load_texture(f"assets/board game pieces/PNG/Dice/dieWhite_border{self.value}.png")
                self.roll_counter += 1
            else:
                # Set the final value and texture
                self.value = self.final_value 
                self.texture = arcade.load_texture(f"assets/board game pieces/PNG/Dice/dieWhite_border{self.value}.png")
                self.is_rolling = False  