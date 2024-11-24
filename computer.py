import arcade

# Set number of rows and columns for the board grid
ROW_COUNT = 24
COLUMN_COUNT = 24

class Computer(arcade.Sprite):
    def __init__(self, piece_image, character_name, scale, start_row, start_column, board_size, board_center_x, board_center_y):
        """
        Initialize the player piece.
        """
        super().__init__(piece_image, scale)

        self.board_size = board_size
        self.board_center_x = board_center_x
        self.board_center_y = board_center_y

        self.character_name = character_name

        # Initial position
        self.row = start_row
        self.column = start_column
        
        self.spaces_remaining = 0

        # Update initial position
        self.update_position()

    def update_position(self):
        """
        Update the player's position based on grid coordinates.
        """
        # Calculate the size of each cell based on the board size
        cell_width = self.board_size / COLUMN_COUNT
        cell_height = self.board_size / ROW_COUNT

        # Calculate the bottom-left corner of the board in the window
        board_bottom_left_x = self.board_center_x - (self.board_size // 2)
        board_bottom_left_y = self.board_center_y - (self.board_size // 2)

        # Update player piece position based on the grid location (row, column)
        self.center_x = board_bottom_left_x + (cell_width * self.column) + (cell_width / 2)
        self.center_y = board_bottom_left_y + (cell_height * self.row) + (cell_height / 2)

    
    def move(self, coordinate):
       
       self.row, self.column = coordinate

       self.update_position()

    def within_a_room(self, rooms):
        """Check if the player is inside a room"""
        for room in rooms:
            for row_start, row_end, col_start, col_end in room.boundaries:
                if row_start <= self.row <= row_end and col_start <= self.column <= col_end:
                    return True
        return False