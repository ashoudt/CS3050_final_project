import arcade

# Set number of rows and columns for the board
ROW_COUNT = 25
COLUMN_COUNT = 25

# Set width and height of each grid cell
WIDTH = 30
HEIGHT = 30

# Set margin between each cell and edges
MARGIN = 2

# Screen dimensions
SCREEN_WIDTH = ((WIDTH + MARGIN) * COLUMN_COUNT + MARGIN) * 1.5
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
SCREEN_TITLE = "Clue Game Board with Piece Movement"

# Calculate board size to take up RESIZE of the screen
RESIZE = 0.75
BOARD_WIDTH = SCREEN_WIDTH * (RESIZE * 0.8) 
BOARD_HEIGHT = SCREEN_HEIGHT * RESIZE

# Calculate scale factor for grid cells to fit into 75% screen area
scale_x = BOARD_WIDTH / ((WIDTH + MARGIN) * COLUMN_COUNT + MARGIN)
scale_y = BOARD_HEIGHT / ((HEIGHT + MARGIN) * ROW_COUNT + MARGIN)

# Use the minimum scale to ensure it fits within the board space
scale = min(scale_x, scale_y)

# Calculate the board position to center it
board_left = (SCREEN_WIDTH - BOARD_WIDTH) / 2
board_bottom = (SCREEN_HEIGHT - BOARD_HEIGHT) / 2

# Movement grid speed (move by one tile at a time)
MOVEMENT_SPEED = int((WIDTH + MARGIN) * scale)

class Board(arcade.Window):
    def __init__(self, width, height, title):
        """
        Set up the application.
        """
        super().__init__(width, height, title)

        # Load the Clue board image as the background
        self.background_texture = arcade.load_texture("ClueBoard.jpeg")

        # Calculate the dimensions of the background texture to fit 75% of the screen
        self.board_width = BOARD_WIDTH
        self.board_height = BOARD_HEIGHT

        # Load the player's piece sprite from the assets folder
        piece_image = "assets/board game pieces/PNG/Pieces (Black)/pieceBlack_border00.png"
        self.player_piece = arcade.Sprite(piece_image, scale)

        # Set the initial position of the piece on a grid tile (center of the board)
        start_row = 1.4
        start_column = 11.3
        self.player_piece.center_x = board_left + start_column * (WIDTH + MARGIN) * scale + (WIDTH / 2 + MARGIN) * scale
        self.player_piece.center_y = board_bottom + start_row * (HEIGHT + MARGIN) * scale + (HEIGHT / 2 + MARGIN) * scale

        # List for all sprites (in this case, just the player)
        self.all_sprites = arcade.SpriteList()
        self.all_sprites.append(self.player_piece)

        # Store the player's current position in terms of grid row and column
        self.player_row = start_row
        self.player_column = start_column

    def on_draw(self):
        """
        Render the screen.
        """
        # Clear the screen
        self.clear()

        # Draw the Clue board background, scaled and centered to 75% of the screen
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      self.board_width, self.board_height,
                                      self.background_texture)

        # Draw the player's piece on the board
        self.all_sprites.draw()

    def on_key_press(self, key, modifiers):
        """
        Handle player movement using arrow keys.
        """
        if key == arcade.key.UP and self.player_row < ROW_COUNT - 1:
            self.player_row += 1
        elif key == arcade.key.DOWN and self.player_row > 0:
            self.player_row -= 1
        elif key == arcade.key.LEFT and self.player_column > 0:
            self.player_column -= 1
        elif key == arcade.key.RIGHT and self.player_column < COLUMN_COUNT - 1:
            self.player_column += 1

        # Update the position of the player's piece based on the new row and column
        self.player_piece.center_x = board_left + self.player_column * (WIDTH + MARGIN) * scale + (WIDTH / 2 + MARGIN) * scale
        self.player_piece.center_y = board_bottom + self.player_row * (HEIGHT + MARGIN) * scale + (HEIGHT / 2 + MARGIN) * scale

    def update(self, delta_time):
        """
        Update method to run logic.
        """
        # TODO: collision detection, etc. here 
        pass

def main():
    # Initialize the game window
    Board(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()

if __name__ == "__main__":
    main()
