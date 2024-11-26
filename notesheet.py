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
AI_SAVE_FILE = "ai_notesheet_state.json"

# Initialize list of names for suspects, weapons, and rooms
SUSPECTS = ["Miss Scarlet", "Colonel Mustard", "Mrs. White", "Mr. Green", "Mrs. Peacock", "Professor Plum"]
WEAPONS = ["Candlestick", "Knife", "Lead Pipe", "Revolver", "Rope", "Wrench"]
ROOMS = ["Kitchen", "Ball Room", "Conservatory", "Dining Room", "Lounge", "Hall", "Study", "Library", "Billiard Room"]


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


'''
Done with help from Stack Overflow:
https://stackoverflow.com/questions/24481852/serialising-an-enum-member-to-json/24482806#24482806
'''
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
    def __init__(self, game_view, player_room, players_turn):
        """
        Initialize the Notesheet view and grid states
        Load saved notesheet if available
        """
        super().__init__()

        # Store previous view for returning
        self.game_view = game_view

        self.player_room = player_room

        self.players_turn = players_turn

        self.grid_state = {
            "Suspects": {suspect: NotesheetBox.BLANK for suspect in SUSPECTS},
            "Weapons": {weapon: NotesheetBox.BLANK for weapon in WEAPONS},
            "Rooms": {room: NotesheetBox.BLANK for room in ROOMS},
        }

        # TODO: AI notesheet (need for all three!!)
        self.ai_grid_state_1 = {
            "Suspects": {suspect: NotesheetBox.BLANK for suspect in SUSPECTS},
            "Weapons": {weapon: NotesheetBox.BLANK for weapon in WEAPONS},
            "Rooms": {room: NotesheetBox.BLANK for room in ROOMS},
        }
        self.ai_grid_state_2 = {
            "Suspects": {suspect: NotesheetBox.BLANK for suspect in SUSPECTS},
            "Weapons": {weapon: NotesheetBox.BLANK for weapon in WEAPONS},
            "Rooms": {room: NotesheetBox.BLANK for room in ROOMS},
        }
        self.ai_grid_state_3 = {
            "Suspects": {suspect: NotesheetBox.BLANK for suspect in SUSPECTS},
            "Weapons": {weapon: NotesheetBox.BLANK for weapon in WEAPONS},
            "Rooms": {room: NotesheetBox.BLANK for room in ROOMS},
        }
        print("DEFINING AI Notesheet!!!!")
        print(self.ai_grid_state_1)
        print()

        self.input_notes = "" # Store text area content
        self.setup()
        # self.load_notes() # Load notes on initialization

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

        # Suggestion button
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

        popup_text_x = SCREEN_HEIGHT / 2
        popup_text_y = SCREEN_WIDTH / 2
        self.popup_text = arcade.Text(
            "Invalid Guess",
            popup_text_x,
            popup_text_y,
            arcade.color.WHITE,
            font_size=14,
            multiline=True,
            width=200,
            anchor_x="center",
            anchor_y="center"
        )
        self.popup_enabled = False

    def on_show_view(self):
        self.window.suspect = None
        self.window.weapon = None
        self.window.room = None

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

        if self.players_turn:
            self.accuse_button.on_click = self.on_accuse_click
            self.suggest_button.on_click = self.on_suggest_click
        else:
            self.accuse_button.on_click = self.on_other_turn_click
            self.suggest_button.on_click = self.on_other_turn_click

        if self.popup_enabled:
            self.manager.disable()
            arcade.draw_rectangle_filled(SCREEN_HEIGHT / 2, SCREEN_WIDTH / 2,
                                        250, 100, arcade.color.BLACK)
            self.popup_text.draw()
        else:
            self.manager.enable()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Handle clicks within the grid cells and toggles the state of the
        clicked cell
        """
        if self.popup_enabled:
            self.popup_enabled = False
        else:
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
        self.validate_guess('SUGGEST')

    def on_accuse_click(self, event):
        self.validate_guess('ACCUSE')

    def on_other_turn_click(self, event):
        self.popup_enabled = True
        self.popup_text.text = "It's not your turn\n(Click to continue)"

    def validate_guess(self, method):
        guess = ['Suspects', 'Weapons', 'Rooms']
        valid_guess = True
        for section, items in self.grid_state.items():
            for card, value in items.items():
                if value.name == method:
                    if section in guess:
                        guess[guess.index(section)] = card
                    else:
                        valid_guess = False
                        self.popup_text.text = f"Too many {section.lower()} selected\n(Click to continue)"
        if 'Suspects' in guess or 'Weapons' in guess or 'Rooms' in guess:
            valid_guess = False
            self.popup_text.text = f"Didn't select one item from each category\n(Click to continue)"
        if method == 'SUGGEST' and guess[2] != self.player_room:
            valid_guess = False
            self.popup_text.text = f"Not in the room you're suggesting\n(Click to continue)"
        if method == 'ACCUSE' and self.player_room != 'Lobby':
            valid_guess = False
            self.popup_text.text = f"Not in the Lobby for an accusation\n(Click to continue)"
        if valid_guess:
            self.window.suspect = guess[0]
            self.window.weapon = guess[1]
            self.window.room = guess[2]
            if method == 'SUGGEST':
                self.window.guess_method = 0
            elif method == 'ACCUSE':
                self.window.guess_method = 1
            if self.game_view:
                # Save the notes
                self.save_notes()
                self.manager.disable()
                self.window.show_view(self.game_view)
        else:
            self.popup_enabled = True

    def on_return_click(self, event):
        """
        Handle the return button click to save notes and go back 
        to the game view.
        """
        
        # Disable the entire UI manager
        self.manager.disable()
        if self.game_view:
            # Save the notes
            self.save_notes()
            self.manager.disable()
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

        # TODO: add all ais here? (then find vals based on # after grid_state??)
        ai_notes_data = {
            "grid_state_1": self.ai_grid_state_1,
            "grid_state_2": self.ai_grid_state_2,
            "grid_state_3": self.ai_grid_state_3
        }

        # Write to the JSON file
        with open(SAVE_FILE, "w") as f:
            json.dump(notes_data, f, cls=EnumEncoder)

        # TODO: Write to AI JSON file (use for loop w/ diff lines for multiple ai dicts)
        print("saving to file...")
        with open(AI_SAVE_FILE, "w") as f2:
            json.dump(ai_notes_data, f2, cls=EnumEncoder)

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

        # TODO: Do the same thing for the AI note sheets (use for loop for diff ais??)
        if os.path.exists(AI_SAVE_FILE):
            with open(AI_SAVE_FILE, "r") as f2:
                notes_data = json.load(f2, object_hook=as_enum)
                self.ai_grid_state_1 = notes_data.get("grid_state_1", self.ai_grid_state_1)
                self.ai_grid_state_2 = notes_data.get("grid_state_2", self.ai_grid_state_2)
                self.ai_grid_state_3 = notes_data.get("grid_state_3", self.ai_grid_state_3)

    # TODO: When initializing ai cards mark the cards in the AI's notesheet (+ create notesheet)
    def set_ai_cards(self, deck1, deck2, deck3):
        print("\n1")
        for card in deck1:
            print(card.value)
            self.ai_grid_state_1[card.card_type][card.value] = self.ai_grid_state_1[card.card_type][card.value].MARKED
        print("\n2")
        for card in deck2:
            print(card.value)
            self.ai_grid_state_2[card.card_type][card.value] = self.ai_grid_state_2[card.card_type][card.value].MARKED
        print("\n3")
        for card in deck3:
            print(card.value)
            self.ai_grid_state_3[card.card_type][card.value] = self.ai_grid_state_3[card.card_type][card.value].MARKED

    # TODO: DELETE THESE 2 funcs??
    def update_players_turn(self, player_turn):
        """
        Say whether it's the player's turn, called when note sheet is opened
        """
        self.players_turn = player_turn

    def update_player_room(self, player_room):
        """
        Update the room the player is in, called when note sheet is opened
        """
        self.player_room = player_room

    def update_notesheet(self, player_turn, player_room):
        """
        Update the player's current room, current turn, and load the json file
        """
        self.players_turn = player_turn
        self.player_room = player_room
        self.load_notes()

    def get_ai_notesheet(self, ai_num):
        """
        Return specified AI note sheet data
        """
        if ai_num == 1:
            return self.ai_grid_state_1
        elif ai_num == 2:
            return self.ai_grid_state_2
        elif ai_num == 3:
            return self.ai_grid_state_3
        else:
            print("can't return ai note sheet because ai num isn't valid (1-3)")

    def update_refute_card(self, refute_card, ai_num):
        """
        When an AI's guess is refuted, update it here
        """
        if ai_num == 1:
            self.ai_grid_state_1[refute_card.card_type][refute_card.value] = \
                self.ai_grid_state_1[refute_card.card_type][refute_card.value].MARKED
        elif ai_num == 2:
            self.ai_grid_state_2[refute_card.card_type][refute_card.value] = \
                self.ai_grid_state_2[refute_card.card_type][refute_card.value].MARKED
        elif ai_num == 3:
            print(f"refute card: {refute_card.value}")
            self.ai_grid_state_3[refute_card.card_type][refute_card.value] = \
                self.ai_grid_state_3[refute_card.card_type][refute_card.value].MARKED
        else:
            print("can't update ai note sheet because ai num isn't valid (1-3)")
        self.save_notes()

    def update_accusation(self, accuse_cards, ai_num):
        """
        When an AI's made an un-refuted guess, mark those cards as ACCUSE
        """
        # TODO: Remove print
        print("update accuse")
        print(accuse_cards)
        if ai_num == 1:
            self.ai_grid_state_1["Suspects"][accuse_cards[0]] = \
                self.ai_grid_state_1["Suspects"][accuse_cards[0]].ACCUSE
            self.ai_grid_state_1["Rooms"][accuse_cards[1]] = \
                self.ai_grid_state_1["Rooms"][accuse_cards[1]].ACCUSE
            self.ai_grid_state_1["Weapons"][accuse_cards[2]] = \
                self.ai_grid_state_1["Weapons"][accuse_cards[2]].ACCUSE
        elif ai_num == 2:
            self.ai_grid_state_2["Suspects"][accuse_cards[0]] = \
                self.ai_grid_state_2["Suspects"][accuse_cards[0]].ACCUSE
            self.ai_grid_state_2["Rooms"][accuse_cards[1]] = \
                self.ai_grid_state_2["Rooms"][accuse_cards[1]].ACCUSE
            self.ai_grid_state_2["Weapons"][accuse_cards[2]] = \
                self.ai_grid_state_2["Weapons"][accuse_cards[2]].ACCUSE
        elif ai_num == 3:
            self.ai_grid_state_3["Suspects"][accuse_cards[0]] = \
                self.ai_grid_state_3["Suspects"][accuse_cards[0]].ACCUSE
            self.ai_grid_state_3["Rooms"][accuse_cards[1]] = \
                self.ai_grid_state_3["Rooms"][accuse_cards[1]].ACCUSE
            self.ai_grid_state_3["Weapons"][accuse_cards[2]] = \
                self.ai_grid_state_3["Weapons"][accuse_cards[2]].ACCUSE
        else:
            print("can't set accusation cards because ai num isn't valid (1-3)")
        self.save_notes()

    def show_ai_suggestion(self, guess):
        """
        Create a pop-up showing the user the AI's guess
        """
        self.manager.disable()
        arcade.draw_rectangle_filled(SCREEN_HEIGHT / 2, SCREEN_WIDTH / 2,
                                        250, 100, arcade.color.BLACK)
        self.popup_text.text = f"Suggestion: {guess[0]} in the {guess[1]} with the {guess[2]}\n(Click to continue)"
        self.popup_text.draw()
        self.popup_enabled = True
        # self.validate_guess("SUGGEST")
