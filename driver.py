from player import Player
from board import Board
from deck import Deck
from die import Die
from notesheet import Notesheet
from computer import Computer
import random
import arcade
import arcade.gui
import os

# Screen dimensions
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 750
SCREEN_TITLE = "Clue Game Board with Piece Movement"

# Font Styling
DEFAULT_FONT_SIZE = 20


class GameView(arcade.View):
    def __init__(self):
        """
        Set up the application.
        """
        super().__init__()
        self.setup()

    def setup(self):
        self.window.suspect = None
        self.window.weapon = None
        self.window.room = None
        self.window.guess_method = None

        # Create the board
        self.board = Board()
        self.board_size = self.board.board_size
        self.board_center_x = self.board.board_center_x
        self.board_center_y = self.board.board_center_y
        self.background_texture = self.board.background_texture

        # Keep track of whose turn it currently is
        self.whose_turn = [True, False, False, False]
        self.ai_turn_completed = False  

        # Create the player piece
        piece_scale = 0.4
        player_selection = {
            "Miss Scarlet": ["assets/board game pieces/PNG/Pieces (Red)/pieceRed_border00.png", 23, 16],
            "Colonel Mustard": ["assets/board game pieces/PNG/Pieces (Yellow)/pieceYellow_border18.png", 16, 23],
            "Mrs. White": ["assets/board game pieces/PNG/Pieces (White)/pieceWhite_border00.png", 23, 7],
            "Mr. Green": ["assets/board game pieces/PNG/Pieces (Green)/pieceGreen_border00.png", 6, 23],
            "Mrs. Peacock": ["assets/board game pieces/PNG/Pieces (Blue)/pieceBlue_border01.png", 5, 0],
            "Professor Plum": ["assets/board game pieces/PNG/Pieces (Purple)/piecePurple_border00.png", 18, 0]
        }

        # Get selected players sprite and starting coordinates
        piece_image, starting_x, starting_y = player_selection[self.window.character_name]
        self.player_piece = Player(piece_image, piece_scale, starting_x, starting_y,
                                   self.board_size, self.board_center_x, self.board_center_y)
        del player_selection[self.window.character_name]
        
        # Create ai 1
        ai_card_1_name, ai_card_1_info = random.choice(list(player_selection.items()))
        piece_image, starting_x, starting_y = ai_card_1_info
        self.ai_1 = Computer(piece_image, piece_scale, starting_x, starting_y,
                                   self.board_size, self.board_center_x, self.board_center_y)
        del player_selection[ai_card_1_name]

        # Create ai 2
        ai_card_2_name, ai_card_2_info = random.choice(list(player_selection.items()))
        piece_image, starting_x, starting_y = ai_card_2_info
        self.ai_2 = Computer(piece_image, piece_scale, starting_x, starting_y,
                                   self.board_size, self.board_center_x, self.board_center_y)
        del player_selection[ai_card_2_name]

        # Create ai 3
        ai_card_3_name, ai_card_3_info = random.choice(list(player_selection.items()))
        piece_image, starting_x, starting_y = ai_card_3_info
        self.ai_3 = Computer(piece_image, piece_scale, starting_x, starting_y,
                                   self.board_size, self.board_center_x, self.board_center_y)
        del player_selection[ai_card_3_name]

        # Create a die for each player
        self.die = Die(1.25)
        self.spaces_remaining = 0
        
        # Create the deck and deal out the cards
        self.deck = Deck()
        self.num_players = 4
        self.deck.deal(self.num_players)
        self.all_decks = self.deck.get_all_cards()
        self.refute_card = None
        self.killer = self.deck.get_killer()

        self.card_padding_from_board = 20
        self.card_padding_from_cards = 20
        self.card_padding_from_edge = 20

        # Position cards on the screen
        for deck in self.all_decks:
            num_player_cards_set = 0

            # Horizontal position for each AI card is the same, the board's padding
            # plus the board size plus the padding from the board
            horizontal_pos = self.board.padding + self.board.board_size + self.card_padding_from_board

            # Vertical position for each player card is the same, the screen height minus the board's padding
            # minus the board size minus the padding from the board
            vertical_pos = SCREEN_HEIGHT - self.board.padding - self.board.board_size - self.card_padding_from_board

            for card in deck:
                # Player's cards, horizontal position is the padding from the edge plus half the card's width since
                # we're calculating the card's center. Added to this is the spacing for a card's width and padding times
                # the number of cards seen, so they'll space themselves out. Vertical positioning is the position
                # discussed earlier plus half the card height
                if deck == self.all_decks[0]:
                    card.position = (self.card_padding_from_edge + card.card_width // 2 + num_player_cards_set * (card.card_width + self.card_padding_from_cards),
                                     vertical_pos - card.card_height // 2)
                    num_player_cards_set += 1
                # First AI player cards, horizontal position is the position discussed earlier plus half the card width
                # since we're calculating the center of each card. Vertical position is the screen height
                # (since origin is in the bottom), minus half the card height and the padding from the edge
                elif deck == self.all_decks[1]:
                    card.position = (horizontal_pos + card.card_width // 2,
                                     SCREEN_HEIGHT - card.card_height // 2 - self.card_padding_from_edge)
                # Move down a card by adding in the card height and padding between cards
                elif deck == self.all_decks[2]:
                    card.position = (horizontal_pos + card.card_width // 2,
                                     SCREEN_HEIGHT - card.card_height // 2 - self.card_padding_from_edge - card.card_height - self.card_padding_from_cards)
                # Move down 2 cards by adding in 2 card heights and padding between 2 cards
                elif deck == self.all_decks[3]:
                    card.position = (horizontal_pos + card.card_width // 2,
                                     SCREEN_HEIGHT - card.card_height // 2 - self.card_padding_from_edge - 2 * card.card_height - 2 * self.card_padding_from_cards)
                # Move down 3 cards by adding in 3 card heights and padding between 3 cards
                elif deck == self.all_decks[4]:
                    card.position = (horizontal_pos + card.card_width // 2,
                                     SCREEN_HEIGHT - card.card_height // 2 - self.card_padding_from_edge - 3 * card.card_height - 3 * self.card_padding_from_cards)
                # Move down 4 cards by adding in 4 card heights and padding between 4 cards
                elif deck == self.all_decks[5]:
                    card.position = (horizontal_pos + card.card_width // 2,
                                     SCREEN_HEIGHT - card.card_height // 2 - self.card_padding_from_edge - 4 * card.card_height - 4 * self.card_padding_from_cards)

        # List for all sprites
        self.all_sprites = arcade.SpriteList()
        self.all_sprites.append(self.player_piece)
        self.all_sprites.extend([self.ai_1, self.ai_2, self.ai_3])

        # Append each die individually to self.all_sprites
        self.all_sprites.append(self.die)
        for player_deck in self.all_decks:
            for card in player_deck:
                self.all_sprites.append(card)

        # Create UI manager for buttons and notesheet
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()

        # Render buttons
        self.default_style = {
            "font_name": ("calibri", "arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": None,
            "bg_color": arcade.color.RASPBERRY,
        }

        # Create a button layout
        self.h_box = arcade.gui.UIBoxLayout(vertical=False)

        # Create the notesheet button
        self.notesheet_button = arcade.gui.UIFlatButton(text="Notesheet", width=200, style=self.default_style)
        self.h_box.add(self.notesheet_button.with_space_around(right=60))
        self.notesheet_button.on_click = self.on_click_notesheet

        # Create the roll button
        self.roll_button = arcade.gui.UIFlatButton(text="Roll", width=200, style=self.default_style)
        self.h_box.add(self.roll_button.with_space_around(left=80))
        self.roll_button.on_click = self.on_click_roll
        self.roll_disabled = False

        # Create the text for the disabled roll "button"
        disabled_roll_text_x = 426
        disabled_roll_text_y = 31
        self.disabled_roll_text = arcade.Text(
            "Roll",
            disabled_roll_text_x,
            disabled_roll_text_y,
            arcade.color.WHITE,
            font_size=15,
            font_name=("calibri", "arial")
        )

        self.guessed_this_turn = False

        # Create the text for how many spaces remaining
        spaces_left_text_x = 565
        spaces_left_text_y = 30
        self.spaces_left_text = arcade.Text(
            f"Spaces Left: {self.spaces_remaining}",
            spaces_left_text_x,
            spaces_left_text_y,
            arcade.color.WHITE,
            DEFAULT_FONT_SIZE
        )

        # Create the text for when no one can help you
        no_help_text_x = 220
        no_help_text_y = 45
        self.no_help_text = arcade.Text(
            "No one can\nhelp you",
            no_help_text_x,
            no_help_text_y,
            arcade.color.WHITE,
            font_size=14,
            multiline=True,
            width=150,
        )
        self.show_no_help = False

        # Position the buttons 
        self.ui_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                align_x=-100,
                anchor_y="center_y",
                align_y=-335,
                child=self.h_box)
        )

    def on_show_view(self):
        from GameOverView import GameOverView

        self.ui_manager.enable()
        if self.whose_turn[0] == True:
            try:
                if self.window.suspect is not None and self.window.weapon is not None and self.window.room is not None:
                    self.spaces_remaining = 0
                    self.suspect = self.window.suspect
                    self.weapon = self.window.weapon
                    self.room = self.window.room
                    guess_members = [self.suspect, self.weapon, self.room]
                    if self.window.guess_method == 0:
                        flipped = False
                        for deck in self.all_decks:
                            if flipped:
                                break
                            for card in deck:
                                if card.value in guess_members and card not in self.all_decks[0]:
                                    self.refute_card = card
                                    self.flip_refute_card(card)
                                    self.refute_card = card
                                    flipped = True
                                    break
                        if flipped:
                            self.show_no_help = False
                        else:
                            self.show_no_help = True
                    elif self.window.guess_method == 1:
                        won = True
                        killer_values = []
                        for answer in self.killer:
                            killer_values.append(answer.value)
                        for guess in guess_members:
                            if guess not in killer_values:
                                won = False
                        game_over_view = GameOverView(won)
                        self.window.show_view(game_over_view)
            except AttributeError:
                pass

    # A function to flip an AI's card face down after they have refuted your guess
    def on_mouse_press(self, x, y, button, key_modifiers):
        # Check if the user clicked on a face_up refute card
        cards = arcade.get_sprites_at_point((x, y), self.all_sprites)

        # If they did, flip it face down again and reset the refute_card
        if self.refute_card in cards:
            self.refute_card.face_down()
            self.refute_card = None
            self.next_turn()

    def flip_refute_card(self, card):
        # Flip card upright
        card.face_up()

        # Move card to back of the sprites list
        self.all_sprites.remove(card)
        self.all_sprites.append(card)

        # TODO: check that sleep works once the game loop is implemented
        # time.sleep(10)

        # wait 10 seconds, then flip the card back over
        # card.face_down()

        # Example of calling flip_refute_card (goes with the refute_guess example [in deck.py])
        # self.flip_refute_card(refute_card)

    def on_click_roll(self, event):
        if not self.roll_disabled and self.whose_turn[0]:
            if self.spaces_remaining == 0:
                current_die = self.die
                current_die.roll()
                self.spaces_remaining = current_die.value
                self.spaces_left_text.text = f"Spaces Left: {self.spaces_remaining}"
                self.roll_disabled = True

    def roll_die_for_current_player(self):
        """
        Roll the die for the current player. Use specific logic for each AI player.
        """
        current_player_index = self.whose_turn.index(True)

        if current_player_index == 0:
            # Enable roll button 
            self.roll_disabled = False

        # AI Player 1
        elif current_player_index == 1:
            if not self.ai_turn_completed and self.spaces_remaining == 0:
                self.roll_disabled = True  
                self.die.roll()
                self.spaces_remaining = self.die.value
                print(f"AI Player 1 rolled a {self.spaces_remaining}")

        # AI Player 2   
        elif current_player_index == 2:
            if not self.ai_turn_completed and self.spaces_remaining == 0:
                self.roll_disabled = True
                self.die.roll()
                self.spaces_remaining = self.die.value
                print(f"AI Player 2 rolled a {self.spaces_remaining}")

        # AI Player 3
        elif current_player_index == 3:
            if not self.ai_turn_completed and self.spaces_remaining == 0:
                self.roll_disabled = True
                self.die.roll()
                self.spaces_remaining = self.die.value
                print(f"AI Player 3 rolled a {self.spaces_remaining}")


    def on_click_notesheet(self, event):
        """
        Switch to Notesheet view when button is clicked.
        """
        self.ui_manager.disable()
        if self.refute_card:
            notesheet_view = Notesheet(self, self.player_piece.get_room(self.board.rooms), False)
        else:
            notesheet_view = Notesheet(self, self.player_piece.get_room(self.board.rooms), self.whose_turn[0])
        self.window.show_view(notesheet_view)

    def on_draw(self):
        """
        Render the screen.
        """
        # Clear the screen
        self.clear()
        arcade.set_background_color(arcade.color.BLACK)


        # Draw the Clue board in the center of the window
        arcade.draw_texture_rectangle(self.board_center_x, self.board_center_y,
                                      self.board_size, self.board_size,
                                      self.background_texture)

        # Draw the player's piece on the board and the cards
        self.all_sprites.draw()

        # Draw UI elements
        self.ui_manager.draw()

        # If roll is disabled, draw over it
        if self.roll_disabled:
            arcade.draw_rectangle_filled(self.roll_button.center_x, self.roll_button.center_y,
                                     200, 50, arcade.color.GRAY)
            self.disabled_roll_text.draw()

        if self.spaces_remaining != 0:
            self.spaces_left_text.draw()


        card_width = 81
        card_height = 93
        padding_from_card = 10
        triangle_x1 = self.board.padding + self.board.board_size + self.card_padding_from_board + card_width + padding_from_card
        triangle_y1 = SCREEN_HEIGHT - self.card_padding_from_edge - card_height // 2
        triangle_x2 = triangle_x1 + 15
        triangle_y2 = triangle_y1 + 15
        triangle_x3 = triangle_x1 + 15
        triangle_y3 = triangle_y1 - 15
        if self.whose_turn[0]:
            pass
            # if self.spaces_remaining == 0:
                # self.roll_disabled = False
        else:
            offset_factor = 1
            for i in range(0, len(self.whose_turn)):
                if self.whose_turn[i]:
                    offset_factor = i - 1
            vertical_offset = offset_factor * (card_height + self.card_padding_from_cards)
            arcade.draw_triangle_filled(triangle_x1, triangle_y1 - vertical_offset,
                                        triangle_x2, triangle_y2 - vertical_offset,
                                        triangle_x3, triangle_y3 - vertical_offset,
                                        arcade.color.GREEN)

        if self.show_no_help:
            self.no_help_text.draw()

    def on_key_press(self, key, modifiers):
        """
        Handle player movement using arrow keys.
        """
        if key == arcade.key.ESCAPE:
            
            arcade.close_window()
            arcade.exit()

        elif key == arcade.key.ENTER:
            self.next_turn()

        if self.spaces_remaining > 0:
            last_row = self.player_piece.row
            last_col = self.player_piece.column
            if key == arcade.key.UP:
                self.player_piece.move(1, 0, self.board.rooms, self.board.doors, key)
                self.update_spaces_left(last_row, last_col)
                self.spaces_left_text.text = f"Spaces Left: {self.spaces_remaining}"
            elif key == arcade.key.DOWN:
                self.player_piece.move(-1, 0, self.board.rooms, self.board.doors, key)
                self.update_spaces_left(last_row, last_col)
                self.spaces_left_text.text = f"Spaces Left: {self.spaces_remaining}"
            elif key == arcade.key.LEFT:
                self.player_piece.move(0, -1, self.board.rooms, self.board.doors, key)
                self.update_spaces_left(last_row, last_col)
                self.spaces_left_text.text = f"Spaces Left: {self.spaces_remaining}"
            elif key == arcade.key.RIGHT:
                self.player_piece.move(0, 1, self.board.rooms, self.board.doors, key)
                self.update_spaces_left(last_row, last_col)
                self.spaces_left_text.text = f"Spaces Left: {self.spaces_remaining}"
            if self.spaces_remaining == 0:
                self.next_turn()

    def next_turn(self):
        if self.whose_turn[0]:
            self.spaces_remaining = 0
            self.show_no_help = False
            self.roll_disabled = True
            if self.refute_card:
                self.refute_card.face_down()
                self.refute_card = None
            self.whose_turn[0] = False
            self.whose_turn[1] = True
        elif self.whose_turn[1]:
            self.whose_turn[1] = False
            self.whose_turn[2] = True
        elif self.whose_turn[2]:
            self.whose_turn[2] = False
            self.whose_turn[3] = True
        elif self.whose_turn[3]:
            self.whose_turn[3] = False
            self.whose_turn[0] = True
            self.roll_disabled = False

        # Reset spaces for the next player
        self.spaces_remaining = 0 
        # Reset AI turn state
        self.ai_turn_completed = False
        # Handle dice roll for the next player
        self.roll_die_for_current_player()  

    def update_spaces_left(self, last_row, last_col):
        if not self.player_piece.within_a_room(self.board.rooms):
            if self.player_piece.row != last_row or self.player_piece.column != last_col:
                self.spaces_remaining -= 1

    def on_update(self, delta_time):
        """
        Update animations and handle AI rolls.
        """
        self.die.update_animation()

        # Automatically handle AI players' rolls if it's not the user's turn
        if not self.whose_turn[0]: 
            self.roll_die_for_current_player()
            
            # If the AI has rolled, proceed to the next turn
            if self.ai_turn_completed:
                self.next_turn()

    def on_close(self):
        """
        Handle window close
        Reset the notesheet on window close
        """
        save_file = "notesheet_state.json"

        # Disable the UI manager and delete the save file
        self.ui_manager.disable()

        # Delete the notesheet save file to reset the state
        if os.path.exists(save_file):
            os.remove(save_file)

def main():
    """ Main function """
    from InstructionView import InstructionView

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = InstructionView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
