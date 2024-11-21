import arcade
from InstructionView import InstructionView

class GameOverView(arcade.View):
    """ View to show when game is over """

    def __init__(self, won):
        """ This is run once when we switch to this view """
        super().__init__()
        self.won = won
        #self.texture = arcade.load_texture("game_over.png")

        arcade.set_viewport(0, self.window.width, 0, self.window.height)

        # Create the text for how many spaces remaining
        won_text_x = self.window.width / 2
        won_text_y = self.window.height / 2
        self.won_text = arcade.Text(
            "Congratulations! You won!",
            won_text_x,
            won_text_y,
            arcade.color.WHITE,
            font_size=40,
            anchor_x="center"
        )
        if not won:
            self.won_text.text = "Sorry, you lost."

    def on_draw(self):
        """ Draw this view """
        self.clear()
        # TODO: Add text to screen, maybe background overlaid
        self.won_text.draw()
        arcade.draw_text("Click to advance", self.window.width / 2, self.window.height / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, re-start the game. """
        game_view = InstructionView()
        self.window.show_view(game_view)
    