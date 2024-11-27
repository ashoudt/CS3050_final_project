import random

import arcade
from board import Board
from notesheet import Notesheet

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

        # Current goal (row, col, room_name)
        self.goal = None
        
        self.spaces_remaining = 0

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
    
    def has_reached_goal(self, board):
        """
        Check if the AI has reached its goal, either by being at the door or inside the room
        """
        # return false is no goal is set
        if self.goal is None:
            return False
        
        # initialize goal components
        goal_row, goal_col, goal_room = self.goal
        
        # check if AI is at the door
        if self.row == goal_row and self.column == goal_col:
            return True

        # check if AI is inside the room
        current_room = board.get_room((self.row, self.column))
        if current_room == goal_room:
            return True
        
        # goal has not been reached
        return False
      
    def get_room(self, rooms):
        """Check if the player is inside a room"""
        for room in rooms:
            for row_start, row_end, col_start, col_end in room.boundaries:
                if row_start <= self.row <= row_end and col_start <= self.column <= col_end:
                    return room.name
        return "N/A"
    
    def move_out_of_room(self, board):
        current_room = self.get_room(self.board.rooms)
        if current_room != "N/A":
            # Find the nearest door to exit the room
            for door in board.doors:
                if door.room_name == current_room:
                    self.move(door.boundaries)
                    break

    def make_ai_suggestion(self, curr_ai):
        # Make sure the AI is within a room AND set that room to their suggestion
        current_room = self.get_room(self.board.rooms)

        # TODO: need to fully implement validating a room once AI movement is implemented (uncomment below)
        # If AI is not currently in a room, then don't make a guess
        if current_room == "N/A":
            print("AI not in a room, can't make a guess")
            return None
        
        # Set the room guess to the current room
        self.room_guess = current_room

        # Look at all the AI's non-marked (blank) suspects and weapons and randomly
        # choose one to guess (set state == suggest)
        # Re-read the .JSON file everytime we make a guess, update notesheet accordingly
        self.ai_notesheet.load_notes()
        current_grid_state = self.ai_notesheet.get_ai_notesheet(curr_ai)

        # Have default values in case there are no more new values to guess of a category
        possible_suspects = ["Mr. Green"]
        possible_weapons = ["Rope"]

        for suspect in current_grid_state["Suspects"]:
            suspect_state = current_grid_state["Suspects"][suspect]
            if str(suspect_state) == "NotesheetBox.BLANK":
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
        # print(f"Suggestion: {self.suspect_guess} in the {self.room_guess} with the {self.weapon_guess}")
        return self.suspect_guess, self.room_guess, self.weapon_guess

