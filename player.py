import arcade

# Set number of rows and columns for the board grid
ROW_COUNT = 24
COLUMN_COUNT = 24

class Player(arcade.Sprite):
    def __init__(self, piece_image, scale, start_row, start_column, board_size, board_center_x, board_center_y):
        """
        Initialize the player piece.
        """
        super().__init__(piece_image, scale)

        self.board_size = board_size
        self.board_center_x = board_center_x
        self.board_center_y = board_center_y

        # Initial position
        self.row = start_row
        self.column = start_column

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

    
    def move(self, d_row, d_column, rooms, doors):
        """Move the player by a row or column delta, but check room boundaries and door access."""
        new_row = self.row + d_row
        new_column = self.column + d_column

        # Check if the new position is at a door
        if (new_row, new_column) in doors:
            self.row = new_row
            self.column = new_column
            self.update_position()
            print(f"DOOR ROW: {self.row}, COL: {self.column}\n")
            return

        # Check if the player is attempting to enter or exit a room through a non-door point
        current_in_room, current_room = self.check_room_collision(self.row, self.column, rooms)
        new_in_room, new_room = self.check_room_collision(new_row, new_column, rooms)

        if current_in_room and not new_in_room or not current_in_room and new_in_room:
            # Allow movement only through doors when changing from room to outside or vice versa
            if (new_row, new_column) in doors or (self.row, self.column) in doors:
                self.row = new_row
                self.column = new_column
                self.update_position()
            print(f"ROOM ROW: {self.row}, COL: {self.column}\n")
            return

        # Free movement within the same space (either inside a room or outside)
        if current_in_room == new_in_room and current_room == new_room:
            self.row = new_row
            self.column = new_column
            print(f"ROAM ROW: {self.row}, COL: {self.column}\n")
            self.update_position()

    def check_room_collision(self, new_row, new_column, rooms):
        """Check if the player is attempting to move into a wall or within room boundaries."""
        for room in rooms:
            for row_start, row_end, col_start, col_end in room.boundaries:
                if row_start <= new_row <= row_end and col_start <= new_column <= col_end:
                    return True, room  # Valid move within a room
        return False, None  # Invalid move through a wall

