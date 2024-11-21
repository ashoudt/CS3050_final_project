import arcade
from PlayerSelectionView import PlayerSelectionView

class InstructionView(arcade.View):

    def on_show_view(self):
        # Set the background color and reset the viewport
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        """ Draw the instruction screen """
        self.clear()

        # Title
        arcade.draw_text("Instructions", self.window.width / 2, self.window.height - 60,
                         arcade.color.WHITE, font_size=40, anchor_x="center")

        # Instructions text
        instructions = [
            "Objective: Deduce the murderer, weapon, and room of the crime.",
            "",
            "Gameplay:",
            "1. Roll the die to move around the board using your arrow keys.",
            "2. Enter rooms to make suggestions (murderer, weapon, room).",
            "3. Other players must disprove your suggestion if possible.",
            "4. Use clues to narrow down suspects, weapons, and rooms.",
            "",
            "Winning:",
            "When confident, make an accusation. If correct, you win!",
            "If incorrect, you’re out of the game.",
            "",
            "Click anywhere to start the game."
        ]

        # Draw each line of instructions
        start_y = self.window.height - 120
        for i, line in enumerate(instructions):
            arcade.draw_text(line, self.window.width / 2, start_y - i * 25,
                             arcade.color.LIGHT_GRAY, font_size=16, anchor_x="center")

        # Footer
        arcade.draw_text("Click to start", self.window.width / 2, 30,
                         arcade.color.WHITE, font_size=18, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ Start the game when the mouse is pressed """
        game_view = PlayerSelectionView()
        self.window.show_view(game_view)