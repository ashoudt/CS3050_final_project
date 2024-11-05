import arcade
import arcade.gui
import json
import os
from enum import Enum

# Constants for layout
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 750
GRID_CELL_SIZE = 50
GRID_MARGIN = 10
TEXT_AREA_WIDTH = 450
TEXT_AREA_HEIGHT = 200

# File to save/load notes
SAVE_FILE = "notesheet_state.json"

# Initialize list of names for suspects, weapons, and rooms
SUSPECTS = ["Miss Scarlet", "Colonel Mustard", "Mrs. White", "Mr. Green", "Mrs. Peacock", "Professor Plum"]
WEAPONS = ["Candlestick", "Knife", "Lead Pipe", "Revolver", "Rope", "Wrench"]
ROOMS = ["Kitchen", "Ballroom", "Conservatory", "Dining Room", "Lounge", "Hall", "Study", "Library", "Billiard Room"]


# Different notesheet states
class NotesheetBox(Enum):
    BLANK = 0
    MARKED = 1
    SUGGEST = 2
    ACCUSE = 3

    def next(self):
        items = list(NotesheetBox)
        value = items.index(self)
        if value == len(items) - 1:
            value = 0
        else:
            value += 1
        return items[value]


NOTESHEET_COLORS = {NotesheetBox.BLANK: arcade.color.LIGHT_GRAY,
                    NotesheetBox.MARKED: arcade.color.LIGHT_GREEN,
                    NotesheetBox.SUGGEST: arcade.color.ORANGE,
                    NotesheetBox.ACCUSE: arcade.color.RED}


class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if obj in NotesheetBox:
            return {"__enum__": str(obj)}
        return json.JSONEncoder.default(self, obj)


def as_enum(d):
    if "__enum__" in d:
        name, member = d["__enum__"].split(".")
        return NotesheetBox[member]
    else:
        return d


class Notesheet(arcade.View):
    def __init__(self, game_view):
        """
        Initialize the Notesheet view and grid states
        Load saved notesheet if available
        """
        super().__init__()

        # Store previous view for returning
        self.game_view = game_view

        self.grid_state = {
            "Suspects": {suspect: NotesheetBox.BLANK for suspect in SUSPECTS},
            "Weapons": {weapon: NotesheetBox.BLANK for weapon in WEAPONS},
            "Rooms": {room: NotesheetBox.BLANK for room in ROOMS},
        }
        self.input_notes = "" # Store text area content
        self.setup()
        self.load_notes() # Load notes on initialization

    def setup(self):
        """
        Set up the UI components
        """
        # UI Manager for buttons and text area
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Text area for notes
        self.text_area = arcade.gui.UIInputText(
            x=50, 
            y=SCREEN_HEIGHT // 2 - 275, 
            width=TEXT_AREA_WIDTH, 
            height=TEXT_AREA_HEIGHT, 
            text=" "
        )
        self.manager.add(self.text_area)

        # Suggetion button
        self.suggest_button = arcade.gui.UIFlatButton(text="Suggest", width=100)
        self.suggest_button.on_click = self.on_suggest_click
        self.manager.add(arcade.gui.UIAnchorWidget(
            anchor_x="center_x",
            align_x=-180,
            align_y=-SCREEN_HEIGHT // 2 + 50,
            child=self.suggest_button
        ))

        # Accusation button
        self.accuse_button = arcade.gui.UIFlatButton(text="Accuse", width=100)
        self.accuse_button.on_click = self.on_accuse_click
        self.manager.add(arcade.gui.UIAnchorWidget(
            anchor_x="center_x",
            align_y=-SCREEN_HEIGHT // 2 + 50,
            child=self.accuse_button
        ))

        # Return to Game button
        self.return_button = arcade.gui.UIFlatButton(text="Back", width=100)
        self.return_button.on_click = self.on_return_click
        self.manager.add(arcade.gui.UIAnchorWidget(
            anchor_x="center_x",
            align_x=180,
            align_y=-SCREEN_HEIGHT // 2 + 50,
            child=self.return_button
        ))

    def draw_grid_section(self, title, items, start_x, start_y):
        """
        Draw a section of the notesheet grid with a title, list of items,
        and toggleable boxes, which indicate whether each item is marked
        """
        # Draw section title
        arcade.draw_text(title, start_x, start_y, arcade.color.BLACK, 16, anchor_x="left")
        y_offset = start_y - 30
        for item in items:
            # Draw item name
            arcade.draw_text(item, start_x, y_offset, arcade.color.BLACK, 12, anchor_x="left")

            # Draw grid cell (toggle box) and fill based on state
            cell_x = start_x + 150
            cell_y = y_offset + 10
            color = NOTESHEET_COLORS[self.grid_state[title][item]]
            arcade.draw_rectangle_filled(cell_x, cell_y, GRID_CELL_SIZE, GRID_CELL_SIZE, color)
            arcade.draw_rectangle_outline(cell_x, cell_y, GRID_CELL_SIZE, GRID_CELL_SIZE, arcade.color.BLACK)

            y_offset -= GRID_CELL_SIZE + GRID_MARGIN

    def on_draw(self):
        """
        Render the Notesheet view
        """
        arcade.start_render()
        arcade.set_background_color(arcade.color.ANTIQUE_BRASS)

        # Draw the title at the top of the view
        arcade.draw_text(
            text="Notesheet",
            start_x=50,
            start_y=SCREEN_HEIGHT - 25,
            color=arcade.color.BLACK,
            font_size=16,
            anchor_x="center"
        )

        # Draw Suspects, Weapons, and Rooms sections
        self.draw_grid_section("Suspects", SUSPECTS, 50, SCREEN_HEIGHT - 50)
        self.draw_grid_section("Weapons", WEAPONS, 300, SCREEN_HEIGHT - 50)
        self.draw_grid_section("Rooms", ROOMS, 550, SCREEN_HEIGHT - 50)
        
        # Draw a border around the text area
        text_area_x = 50 + TEXT_AREA_WIDTH // 2
        text_area_y = (SCREEN_HEIGHT // 2 - 275) + TEXT_AREA_HEIGHT // 2
        border_padding = 5
        arcade.draw_rectangle_outline(
            center_x=text_area_x,
            center_y=text_area_y,
            width=TEXT_AREA_WIDTH + border_padding,
            height=TEXT_AREA_HEIGHT + border_padding,
            color=arcade.color.BLACK,
            border_width=2  
        )

    # Draw label above the text area
        arcade.draw_text(
            text="Enter notes here:",
            start_x=50,  
            start_y=SCREEN_HEIGHT // 2 - 60,
            color=arcade.color.BLACK,
            font_size=12
        )
        
        # Draw manager elements
        self.manager.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Handle clicks within the grid cells and toggles the state of the
        clicked cell
        """
        # Check if the click is within any grid cell and toggle its state
        for section, items in self.grid_state.items():
            start_x, start_y = self.get_grid_start_position(section)
            for index, item in enumerate(items):
                cell_x = start_x + 150
                cell_y = start_y - 30 - index * (GRID_CELL_SIZE + GRID_MARGIN) + 10
                if (cell_x - GRID_CELL_SIZE / 2 < x < cell_x + GRID_CELL_SIZE / 2 and
                    cell_y - GRID_CELL_SIZE / 2 < y < cell_y + GRID_CELL_SIZE / 2):
                    # Toggle the state of the grid cell
                    self.grid_state[section][item] = self.grid_state[section][item].next()

    def get_grid_start_position(self, section):
        """
        Return the starting x and y coordinates for a specific grid section
        (Suspects, Weapons, or Rooms)
        """
        # Define start positions for each section based on title
        if section == "Suspects":
            return 50, SCREEN_HEIGHT - 50
        elif section == "Weapons":
            return 300, SCREEN_HEIGHT - 50
        elif section == "Rooms":
            return 550, SCREEN_HEIGHT - 50

    def on_suggest_click(self, event):
        """
        Handle the click event for suggestions

        PLACEHOLDER
        """
        suspect = None
        weapon = None
        room = None
        valid_guess = True
        for section, items in self.grid_state.items():
            for card, value in items.items():
                if value.name == 'SUGGEST':
                    if section == 'Suspects':
                        if suspect is None:
                            suspect = card
                        else:
                            valid_guess = False
                    elif section == 'Weapons':
                        if weapon is None:
                            weapon = card
                        else:
                            valid_guess = False
                    else:
                        if room is None:
                            room = card
                        else:
                            valid_guess = False
        if suspect is None or weapon is None or room is None:
            valid_guess = False
        if valid_guess:
            print(f'Suggestion: {suspect} in the {room} with the {weapon}')


    def on_accuse_click(self, event):
        """
        Handle the click event for accusations

        PLACEHOLDER
        """
        suspect = None
        weapon = None
        room = None
        valid_guess = True
        for section, items in self.grid_state.items():
            for card, value in items.items():
                if value.name == 'ACCUSE':
                    if section == 'Suspects':
                        if suspect is None:
                            suspect = card
                        else:
                            valid_guess = False
                    elif section == 'Weapons':
                        if weapon is None:
                            weapon = card
                        else:
                            valid_guess = False
                    else:
                        if room is None:
                            room = card
                        else:
                            valid_guess = False
        if suspect is None or weapon is None or room is None:
            valid_guess = False
        if valid_guess:
            print(f'Accusation: {suspect} in the {room} with the {weapon}')

    def on_return_click(self, event):
        """
        Handle the return button click to save notes and go back 
        to the game view.
        """
        if self.game_view:
            # Save the notes
            self.save_notes()
            self.window.show_view(self.game_view)


    def save_notes(self):
        """
        Save the current notesheet state to a JSON file.
        """
        # Update custom notes from the text area
        self.custom_notes = self.text_area.text

        # Create a dictionary for saving
        notes_data = {
            "grid_state": self.grid_state,
            "custom_notes": self.custom_notes
        }

        # Write to the JSON file
        with open(SAVE_FILE, "w") as f:
            json.dump(notes_data, f, cls=EnumEncoder)

    def load_notes(self):
        """
        Load the notesheet state from a JSON file, if it exists.
        """
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r") as f:
                notes_data = json.load(f, object_hook=as_enum)
                self.grid_state = notes_data.get("grid_state", self.grid_state)
                self.custom_notes = notes_data.get("custom_notes", "")
                
                # Set the loaded notes in the text area
                self.text_area.text = self.custom_notes


    def on_close(self):
        """
        Disable UI manager
        """
        self.manager.disable()
