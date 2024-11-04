import arcade

# Set number of rows and columns for the board grid
ROW_COUNT = 24
COLUMN_COUNT = 24

# Set width and height of each grid cell
WIDTH = 30
HEIGHT = 30

# Set margin between each cell and edges
MARGIN = 2

# Screen dimensions
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 750

# Board should take up 70% of the screen height (square shape)
BOARD_SIZE = SCREEN_HEIGHT * 0.7

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

class Door:
    def __init__(self, boundaries, entry_direction):
        """
        Create a door with a row, col, and direction of entry
        Boundaries are in format (row, col)
        """
        self.boundaries = boundaries
        self.entry_direction = entry_direction


class Board():
    def __init__(self):
        """
        Set up the board
        """
        super().__init__()

        # Load the Clue board image as the background
        self.background_texture = arcade.load_texture("assets/ClueBoard.jpeg")

        # Set the scaling of the board to fit into a square area
        self.board_size = BOARD_SIZE

        # Center the board in the top left corner of the screen, with 20 pixels of padding away from the edges
        self.padding = 20
        self.board_center_x = self.padding + self.board_size // 2
        # Subtract the padding and board size // 2 from screen height because the origin is at the bottom of the screen
        self.board_center_y = SCREEN_HEIGHT - self.padding - self.board_size // 2

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
            Door((4, 5), "LEFT"), Door((12, 1), "DOWN"), Door((8, 6), "LEFT"), Door((12, 3), "UP"),
            Door((15,7), "LEFT"), Door((19,6), "UP"), Door((19,8), "RIGHT"), Door((16,11), "UP"), 
            Door((16,12), "UP"), Door((17,17), "UP"), Door((15,17), "DOWN"), Door((11,15), "RIGHT"), 
            Door((6,19), "DOWN"), Door((4,16), "LEFT"), Door((7,14), "DOWN"), Door((7,9), "DOWN"), 
            Door((4,7), "RIGHT")
        ]