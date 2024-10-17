import arcade
import player
from ui_elements import GameUI

# Set number of rows and columns for the board grid
ROW_COUNT = 24
COLUMN_COUNT = 24

# Set width and height of each grid cell
WIDTH = 30
HEIGHT = 30

# Set margin between each cell and edges
MARGIN = 2

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Clue Game Board with Piece Movement"

# Board should take up 70% of the screen height (square shape)
BOARD_SIZE = SCREEN_HEIGHT * 0.7

# Movement speed (move by one tile at a time)
MOVEMENT_SPEED = WIDTH + MARGIN


class Room:
    def __init__(self, name, boundaries):
        """
        Create a room with a given name and boundaries.
        Boundaries should be a list of tuples [(row_start, row_end, col_start, col_end)].
        """
        self.name = name
        self.boundaries = boundaries

class Board(arcade.Window):
    def __init__(self, width, height, title):
        """
        Set up the application.
        """
        super().__init__(width, height, title)

        # Load the Clue board image as the background
        self.background_texture = arcade.load_texture("ClueBoard.jpeg")

        # Set the scaling of the board to fit into a square area
        self.board_size = BOARD_SIZE

        # Center the board on the screen
        self.board_center_x = SCREEN_WIDTH // 2
        self.board_center_y = SCREEN_HEIGHT // 2

        # Create the rooms with boundaries
        self.rooms = [
            Room("Conservatory", [(0, 4, 0, 5)]),
            Room("Billiards Room", [(7, 11, 0, 5)]),
            Room("Library", [(14, 16, 0, 0), (14, 16, 6, 6), (13, 17, 1, 5)]),
            Room("Study", [(20, 23, 0, 6)]),
            Room("Hall", [(17, 23, 9, 14)]),
            Room("Lounge", [(18, 23, 17, 23)]),
            Room("Dining Room", [(9, 14, 16, 23), (8, 8, 19, 23)]),
            Room("Kitchen", [(0, 5, 18, 23)]),
            Room("Ball Room", [(1, 6, 8, 15), (0, 0, 10, 12)]),
            Room("Lobby", [(9, 15, 9, 13)])
        ]

        # Define doors for the rooms
        self.doors = [
            (4, 5), (12, 1), (8, 6), (12, 3), (15,7), (19,6), (19,8),
            (16,11), (16,12), (17,17), (15,17), (11,15), (6,19), 
            (4,16), (7,14), (7,9), (4,7)
        ]

        # Create the player piece
        piece_image = "assets/board game pieces/PNG/Pieces (Black)/pieceBlack_border00.png"
        self.player_piece = player.Player(piece_image, 0.5, 8, 8, self.board_size, self.board_center_x, self.board_center_y)

        # List for all sprites (in this case, just the player)
        self.all_sprites = arcade.SpriteList()
        self.all_sprites.append(self.player_piece)

        # Create UI manager for buttons and notesheet
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()

         # Create the GameUI instance
        self.game_ui = GameUI(self.ui_manager)

    def on_draw(self):
        """
        Render the screen.
        """
        # Clear the screen
        self.clear()

        # Draw the Clue board in the center of the window
        arcade.draw_texture_rectangle(self.board_center_x, self.board_center_y,
                                      self.board_size, self.board_size,
                                      self.background_texture)

        # Draw the player's piece on the board
        self.all_sprites.draw()

        # Draw UI elements
        self.ui_manager.draw()

    def on_key_press(self, key, modifiers):
        """
        Handle player movement using arrow keys.
        """
        if key == arcade.key.UP:
            self.player_piece.move(1, 0, self.rooms, self.doors)
        elif key == arcade.key.DOWN:
            self.player_piece.move(-1, 0, self.rooms, self.doors)
        elif key == arcade.key.LEFT:
            self.player_piece.move(0, -1, self.rooms, self.doors)
        elif key == arcade.key.RIGHT:
            self.player_piece.move(0, 1, self.rooms, self.doors)


def main():
    # Initialize the game window
    Board(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
