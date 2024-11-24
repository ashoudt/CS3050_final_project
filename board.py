import arcade
import heapq

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
            Room("Billiard Room", [(7, 11, 0, 5)], True),
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
            Door((4,7), "RIGHT"), Door((16,11), "DOWN")
        ]

        self.player_locations =  {
            "Miss Scarlet": [23, 16],
            "Colonel Mustard": [16, 23],
            "Mrs. White": [23, 7],
            "Mr. Green": [6, 23],
            "Mrs. Peacock": [5, 0],
            "Professor Plum": [18, 0]
        }
    
    def get_room(self, position):
        """
        Check if the given position (row, col) is inside any room.
        Returns the room name if inside a room, otherwise None.
        """
        row, col = position
        for room in self.rooms:
            for boundary in room.boundaries:
                row_start, row_end, col_start, col_end = boundary
                if row_start <= row <= row_end and col_start <= col <= col_end:
                    return room.name  # Position is inside this room
        return None  # Not inside any room


    def can_move(self, current, direction, start, goal):
        """Check if the player can move from the current position in the specified direction."""
        row, col = current
        next_position = {
            "UP": (row + 1, col),
            "DOWN": (row - 1, col),
            "LEFT": (row, col - 1),
            "RIGHT": (row, col + 1),
        }.get(direction)

        opposites = {"UP": "DOWN", 
                     "DOWN": "UP", 
                     "LEFT": "RIGHT", 
                     "RIGHT": "LEFT"}
        
        # Get names of all coordinate rooms
        current_room = self.get_room(current)
        next_room = self.get_room(next_position)
        start_room = self.get_room(start)
        goal_room = self.get_room(goal)

        # Ensure next_position is within the board bounds
        if not (0 <= next_position[0] < ROW_COUNT and 0 <= next_position[1] < COLUMN_COUNT):
            return False  # Out of bounds
        
        # Check for user collision
        for value in self.player_locations.values():
            #_, coordinate = player.items()

            if value == list(next_position):
                return False

        # Check if the move is through a door into a room
        for door in self.doors:
            if (row, col) == door.boundaries and door.entry_direction == direction and next_room == goal_room:
                return True  # Move through a door
            
        # Check if move is through a door, out of a room
        for door in self.doors:
            if (next_position[0], next_position[1]) == door.boundaries and door.entry_direction == opposites[direction]:
                return True  # Move through a door
        
        # Allow movement within a room if it is within a start,goal, or not a room 
        if current_room == next_room and (next_room == start_room or next_room == goal_room or next_room == None):
            return True

        return False  # Move is not valid

    
    def heuristic(self, current, goal):
        """Calculate the Manhattan distance heuristic."""
        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

    def get_neighbors(self, position, start, goal):
        """Return accessible neighbors of the given position based on walls."""
        row, col = position
        neighbors = []

        directions = {
            "UP": (row + 1, col),
            "DOWN": (row - 1, col),
            "LEFT": (row, col - 1),
            "RIGHT": (row, col + 1),
        }

        for direction, (r, c) in directions.items():
            # Ensure within bounds and no rooms block movement
            if 0 <= r < ROW_COUNT and 0 <= c < COLUMN_COUNT and self.can_move(position, direction, start, goal):
                neighbors.append((r, c))

        return neighbors

    def a_star(self, start, goal):
        """Find the shortest path from start to goal using A*."""
        open_list = []
        heapq.heappush(open_list, (0, start))  # (f_cost, position)

        came_from = {}  # To reconstruct path
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while open_list:
            _, current = heapq.heappop(open_list)

            if current == goal:
                return self.reconstruct_path(came_from, current)

            for neighbor in self.get_neighbors(current, start, goal):
                tentative_g_score = g_score[current] + 1  # Cost to move to neighbor (one tile)

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))

        return None  # No path found

    def reconstruct_path(self, came_from, current):
        """Reconstruct the path from start to goal."""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path