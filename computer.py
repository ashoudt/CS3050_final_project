import random

import arcade
from board import Board
from notesheet import Notesheet

# Set number of rows and columns for the board grid
ROW_COUNT = 24
COLUMN_COUNT = 24

class Computer(arcade.Sprite):
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

        # Create variables for suggestion/accusations
        self.suspect_guess = ""
        self.weapon_guess = ""
        self.room_guess = ""

        # Create a board and note sheet to keep track of AI's known values
        self.board = Board()
        self.ai_notesheet = Notesheet(self, "N/A", False)

        self.ready_to_accuse = False


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

    
    def move(self, d_row, d_column, rooms, doors, key):
        """Move the player by a row or column delta, but check room boundaries and door access."""
        new_row = self.row + d_row
        new_column = self.column + d_column

        # Set opposites for leaving a room
        opposites = {"UP": "DOWN", 
                     "DOWN": "UP", 
                     "LEFT": "RIGHT", 
                     "RIGHT": "LEFT"}

        # Check if the player is attempting to enter or exit a room through a non-door point
        current_in_room, current_room = self.check_room_collision(self.row, self.column, rooms)
        new_in_room, new_room = self.check_room_collision(new_row, new_column, rooms)

        # Leaving room case
        if current_in_room and not new_in_room:
            for door in doors:
                opposite_direction = opposites[door.entry_direction]
                expected_key = getattr(arcade.key, opposite_direction, None)
                if (new_row, new_column) == door.boundaries and key == expected_key:
                    self.row = new_row
                    self.column = new_column
                    self.update_position()
                    break
            print(f"LEAVE ROOM ROW: {self.row}, COL: {self.column}\n")
            return

        # Entering room case
        if not current_in_room and new_in_room:
            for door in doors:
                expected_key = getattr(arcade.key, door.entry_direction.upper(), None)
                if (self.row, self.column) == door.boundaries and key == expected_key:
                    self.row = new_row
                    self.column = new_column
                    self.update_position()
                    break
            print(f"IN ROOM ROW: {self.row}, COL: {self.column}\n")
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

    def within_a_room(self, rooms):
        """Check if the player is inside a room"""
        for room in rooms:
            for row_start, row_end, col_start, col_end in room.boundaries:
                if row_start <= self.row <= row_end and col_start <= self.column <= col_end:
                    return True
        return False

    def get_room(self, rooms):
        """Check if the player is inside a room"""
        for room in rooms:
            for row_start, row_end, col_start, col_end in room.boundaries:
                if row_start <= self.row <= row_end and col_start <= self.column <= col_end:
                    return room.name
        return "N/A"

    # TODO: Create function for AI to GUESS weapon and person (get_room for room, CALL FROM DRIVER)
    def make_ai_suggestion(self, curr_ai):
        # Make sure the AI is within a room AND set that room to their suggestion
        current_room = self.get_room(self.board.rooms)

        # TODO: need to confirm that validating a room works once AI movement is implemented
        # If AI is not currently in a room, then don't make a guess
        # if current_room == "N/A":
        #     print("ai not in a room, can't make a guess")
        #     return "Not in a room, can't make a guess"

        self.room_guess = current_room

        # Look at all the AI's non-marked (blank) suspects and weapons and randomly
        # choose one to guess (set state == suggest)
        # Re-read the .JSON file everytime we make a guess, update notesheet accordingly
        self.ai_notesheet.load_notes()
        current_grid_state = self.ai_notesheet.get_ai_notesheet(curr_ai)
        # print(current_grid_state["Suspects"])

        # TODO: delete this once validating a room works
        possible_rooms = ["Conservatory"]
        for room in current_grid_state["Rooms"]:
            suspect_state = current_grid_state["Rooms"][room]
            if str(suspect_state) == "NotesheetBox.BLANK":
                possible_rooms.append(room)
        random.shuffle(possible_rooms)
        self.room_guess = possible_rooms[0]
        # TODO: end of section to delete

        # Have default values in case there are no more new values to guess of a category
        possible_suspects = ["Mr. Green"]
        possible_weapons = ["Rope"]

        for suspect in current_grid_state["Suspects"]:
            suspect_state = current_grid_state["Suspects"][suspect]
            # print(suspect_state)
            # print(current_grid_state["Suspects"][suspect])
            if str(suspect_state) == "NotesheetBox.BLANK":
                # self.suspect_guess = suspect
                possible_suspects.append(suspect)

        for weapon in current_grid_state["Weapons"]:
            suspect_state = current_grid_state["Weapons"][weapon]
            if str(suspect_state) == "NotesheetBox.BLANK":
                possible_weapons.append(weapon)

        # Shuffle the un-marked values and choose one
        random.shuffle(possible_suspects)
        random.shuffle(possible_weapons)
        self.suspect_guess = possible_suspects[0]
        self.weapon_guess = possible_weapons[0]

        # Make the suggestion and return those cards (so driver can call deck functions)
        print(f"Suggestion: {self.suspect_guess} in the {self.room_guess} with the {self.weapon_guess}")
        return self.suspect_guess, self.room_guess, self.weapon_guess

    # TODO: Create function for AI to ACCUSE (once they have made a guess that isn't refuted)
    # Also need to get the AI to move towards the middle area once they know they can accuse
    # def make_ai_accusation(self, curr_ai):
