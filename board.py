import arcade

# Set number of rows and columns for the board
ROW_COUNT = 25
COLUMN_COUNT = 25

# Set width and height of each grid
WIDTH = 30
HEIGHT = 30

# This sets the margin between each cell and on the edges of the screen.
MARGIN = 2

# Screen dimensions
SCREEN_WIDTH = ((WIDTH + MARGIN) * COLUMN_COUNT + MARGIN) * 1.6
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
SCREEN_TITLE = "Array Backed Grid Buffered Example"

# Calculate board size 
BOARD_WIDTH = SCREEN_WIDTH * 0.75
BOARD_HEIGHT = SCREEN_HEIGHT * 0.75

# Calculate scale factor for grid cells to fit into 60% screen area
scale_x = BOARD_WIDTH / ((WIDTH + MARGIN) * COLUMN_COUNT + MARGIN)
scale_y = BOARD_HEIGHT / ((HEIGHT + MARGIN) * ROW_COUNT + MARGIN)

# Use the minimum scale to ensure it fits within the board space
scale = min(scale_x, scale_y)

# Calculate the board position to center it
board_left = (SCREEN_WIDTH - BOARD_WIDTH) / 2
board_bottom = (SCREEN_HEIGHT - BOARD_HEIGHT) / 2


class Board(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Set up the application.
        """
        super().__init__(width, height, title)

        # Set the background color of the window
        self.background_color = arcade.color.BLACK

        # One dimensional list of all sprites in the two-dimensional sprite list
        self.grid_sprite_list = arcade.SpriteList()

        # This will be a two-dimensional grid of sprites to mirror the two
        # dimensional grid of numbers. This points to the SAME sprites that are
        # in grid_sprite_list, just in a 2d manner.
        self.grid_sprites = []

        # Create a list of solid-color sprites to represent each grid location
        for row in range(ROW_COUNT):
            self.grid_sprites.append([])
            for column in range(COLUMN_COUNT):
                x = board_left + column * (WIDTH + MARGIN) * scale + (WIDTH / 2 + MARGIN) * scale
                y = board_bottom + row * (HEIGHT + MARGIN) * scale + (HEIGHT / 2 + MARGIN) * scale
                sprite = arcade.SpriteSolidColor(int(WIDTH * scale), int(HEIGHT * scale), arcade.color.WHITE)
                sprite.center_x = x
                sprite.center_y = y
                self.grid_sprite_list.append(sprite)
                self.grid_sprites[row].append(sprite)

    def on_draw(self):
        """
        Render the screen.
        """
        # We should always start by clearing the window pixels
        self.clear()

        # Batch draw the grid sprites
        self.grid_sprite_list.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """

        # Adjust for the board offset
        x -= board_left
        y -= board_bottom

        # Convert the clicked mouse position into grid coordinates
        column = int(x // ((WIDTH + MARGIN) * scale))
        row = int(y // ((HEIGHT + MARGIN) * scale))

        print(f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column})")

        # Make sure we are on-grid. It is possible to click in the upper right
        # corner in the margin and go to a grid location that doesn't exist
        if row >= ROW_COUNT or column >= COLUMN_COUNT or row < 0 or column < 0:
            return

        # Flip the color of the sprite
        if self.grid_sprites[row][column].color == arcade.color.WHITE:
            self.grid_sprites[row][column].color = arcade.color.GREEN
        else:
            self.grid_sprites[row][column].color = arcade.color.WHITE


def main():
    Board(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
