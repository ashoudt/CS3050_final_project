import arcade
import player
from ui_elements import GameUI
from deck import Deck

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
SCREEN_HEIGHT = 750
SCREEN_TITLE = "Clue Game Board with Piece Movement"

# Board should take up 65% of the screen height (square shape)
BOARD_SIZE = SCREEN_HEIGHT * 0.65

# Movement speed (move by one tile at a time)
MOVEMENT_SPEED = WIDTH + MARGIN


class Room:
    def __init__(self, name, boundaries, accessible):
        """
        Create a room with a given name and boundaries.
        Boundaries should be a list of tuples [(row_start, row_end, col_start, col_end)].
        """
        self.name = name
        self.boundaries = boundaries
        self.accessible = accessible

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
            Room("Conservatory", [(0, 3, 0, 5), (4,4,1,4)], True),
            Room("Billiards Room", [(7, 11, 0, 5)], True),
            Room("Library", [(14, 16, 0, 0), (14, 16, 6, 6), (13, 17, 1, 5)], True),
            Room("Study", [(20, 22, 0, 6), (23, 23, 0, 5)], True),
            Room("Hall", [(17, 22, 9, 14), (23, 23, 10, 13)], True),
            Room("Lounge", [(18, 23, 17, 23)], True),
            Room("Dining Room", [(9, 14, 16, 23), (8, 8, 20, 23)], True),
            Room("Kitchen", [(0, 4, 18, 23), (5, 5, 18, 22)], True),
            Room("Ball Room", [(1, 6, 8, 15), (0, 0, 10, 13)], True),
            Room("Lobby", [(9, 15, 9, 13)], True),
            Room("Outside", [(0, 0, 6, 6), (6, 6, 0, 0), (5, 5, -1, -1), (4, 4, 0, 0), (12, 12, 0, 0), (13, 13, 0, 0),
                             (17, 17, 0, 0), (19, 19, 0, 0), (23, 23, 6, 6), (23, 23, 8, 8), (23, 23, 9, 9),
                             (23, 23, 14, 14), (23, 23, 15, 15), (23, 23, 17, 17), (17, 17, 23, 23), (15, 15, 23, 23),
                             (7, 7, 23, 23), (5, 5, 23, 23), (0, 0, 17, 17), (16, 16, 24, 24), (18, 18, -1, -1),
                             (24, 24, 7, 7), (24, 24, 16, 16), (6, 6, 24, 24), (-1, -1, 7, 16)], 
                             False)
        ]

        # Define doors for the rooms
        self.doors = [
            (4, 5), (12, 1), (8, 6), (12, 3), (15,7), (19,6), (19,8),
            (16,11), (16,12), (17,17), (15,17), (11,15), (6,19), 
            (4,16), (7,14), (7,9), (4,7)
        ]

        # Create the player piece
        piece_image = "assets/board game pieces/PNG/Pieces (Black)/pieceBlack_border00.png"
        self.player_piece = player.Player(piece_image, 0.4, 0, 7, self.board_size, self.board_center_x, self.board_center_y)


        #Create the deck and deal out the cards
        self.deck = Deck()
        self.num_players = 4
        self.deck.deal(self.num_players)
        self.all_decks = self.deck.get_all_cards()

        self.card_horizontal_padding = 300  # padding for horizontal edges of the screen
        self.card_vertical_padding = 150  # padding for vertical  edges of the screen

        # Position cards on the screen
        for deck in self.all_decks:
            card_space = (SCREEN_WIDTH - (self.card_horizontal_padding * 2)) / len(deck)  # divide remaining space among cards
            current_card_space = 0  # number of cards already on this part of the screen

            # Position for cards on the screen (padding + # cards on screen + center of next card space)
            changing_pos = int(self.card_horizontal_padding + current_card_space + (card_space / 2))
            vertical_changing_pos = int(self.card_vertical_padding + current_card_space + (card_space / 2))

            # Distance from the outer edge of the screen
            static_pos = 60
            # Currently have more horizontal space than vertical
            horizontal_offset = 40

            for card in deck:
                # BOTTOM HORIZONTAL (Player)
                if deck == self.all_decks[0]:
                    card.position = changing_pos, static_pos
                # LEFT VERTICAL
                elif deck == self.all_decks[1]:
                    card.position = static_pos + horizontal_offset, vertical_changing_pos
                # RIGHT VERTICAL
                elif deck == self.all_decks[2]:
                    card.position = SCREEN_WIDTH - static_pos - horizontal_offset, vertical_changing_pos
                # TOP HORIZONTAL
                elif deck == self.all_decks[3]:
                    card.position = changing_pos, SCREEN_HEIGHT - static_pos
                # STACK IN CORNER
                else:
                    # TODO: Print a pile in the corners (once final screen size is determined)
                    pass
                changing_pos += card_space
                vertical_changing_pos += card_space

        # List for all sprites (in this case, just the player and cards)
        self.all_sprites = arcade.SpriteList()
        self.all_sprites.append(self.player_piece)
        for self.playerDeck in self.all_decks:
            for self.card in self.playerDeck:
                self.all_sprites.append(self.card)


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

        # Draw the player's piece on the board and the cards
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

    def get_decks(self):
        return self.all_decks

    def get_killer(self):
        return self.deck.get_killer()