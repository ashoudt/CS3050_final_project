import time
from player import Player
from board import Board
from deck import Deck
from die import Die
from notesheet import Notesheet
import arcade
import arcade.gui
import os

# Screen dimensions
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 750
SCREEN_TITLE = "Clue Game Board with Piece Movement"

# Font Styling
DEFAULT_FONT_SIZE = 20


'''
pseudocode for main game loop
lines marked with * at the beginning are not necessary to implement for the first deliverable
lines marked with ? are features we may or may not add in to the final product

?player selects how many opponents
set up board
select random character and remove it from the deck
select random weapon and remove it from the deck
select random room and remove it from the deck
deal out cards to the player
*deal out cards to each AI
?have the players roll for turn order
initialize game is over to false
initialize player won to false
initialize player's turn to true
while not game is over
    while player's turn
        if player chooses to move
            ?if they are in a room with a secret passage
                ?ask if they would like to take the secret passage
                ?if yes, break
            *roll the dice
            *give player control of their character to move that many spaces
            *ask them to confirm their move once they have gone exactly that many spaces or entered a room
            (For the first sprint session, just start off letting them move wherever and end their turn when they're ready)
            if yes, take away control
            otherwise, let them keep moving
        if player chooses to make a suggestion and is in a valid room
            let them select a character
            ?pull that character into the room the player is in
            let them select a weapon
            submit their guess
            if the room card, character card, and guess card are in their hand or part of the solution
                tell them no cards were found
            else
                *for each AI in order of their turn
                    *if they have at least one of the three cards, show one to the player
                (For the first sprint session, just show the player a random card that's part of their guess)
        if player chooses to make an accusation and is in the final room
            let them select a person
            let them select a weapon
            let them select a room
            if guess matches the solution
                set player won to true
            set end of game to true
        set player's turn to false
    *if game is over
        *break
    while not player's turn
        *let the AI take their turns
        (For the first sprint session, just set the player's turn to true again)

*display ending message with solution
(For the first sprint session, just tell the player if they won or lost)
'''

class GameView(arcade.View):
    def __init__(self):
        """
        Set up the application.
        """
        super().__init__()
        self.setup()

    def setup(self):
        # Create the board
        self.board = Board()
        self.board_size = self.board.board_size
        self.board_center_x = self.board.board_center_x
        self.board_center_y = self.board.board_center_y
        self.background_texture = self.board.background_texture

        # Keep track of whose turn it currently is
        self.whose_turn = [True, False, False, False]

        # Create the player piece
        piece_image = "assets/board game pieces/PNG/Pieces (Black)/pieceBlack_border00.png"
        self.player_piece = Player(piece_image, 0.4, 4, 7,
                                   self.board_size, self.board_center_x, self.board_center_y)

        # Create the die
        self.die = Die(1.25)
        self.spaces_remaining = 0

        # Create the deck and deal out the cards
        self.deck = Deck()
        self.num_players = 4
        self.deck.deal(self.num_players)
        self.all_decks = self.deck.get_all_cards()
        self.refute_card = None

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
        self.all_sprites.append(self.die)
        self.all_sprites.append(self.player_piece)
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
        self.roll_button.on_click = self.on_roll_click
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

        # Create the text for how many spaces remaining
        spaces_left_text_x = 565
        spaces_left_text_y = 30
        self.spaces_left_text = arcade.Text(
            f"Spaces Left: {self.spaces_remaining}",
            spaces_left_text_x,
            spaces_left_text_y,
            arcade.color.WHITE,
            DEFAULT_FONT_SIZE,
        )

        # Position the buttons 
        self.ui_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                align_x=-100,
                anchor_y="center_y",
                align_y=-335,
                child=self.h_box)
        )

    # A function to flip an AI's card face down after they have refuted your guess
    def on_mouse_press(self, x, y, button, key_modifiers):
        # Check if the user clicked on a face_up refute card
        cards = arcade.get_sprites_at_point((x, y), self.all_sprites)

        # If they did, flip it face down again and reset the refute_card
        if self.refute_card in cards:
            self.refute_card.face_down()
            self.refute_card = None

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
        if not self.roll_disabled:
            if self.spaces_remaining == 0:
                self.die.roll()
                self.spaces_remaining = self.die.value
                self.spaces_left_text.text = f"Spaces Left: {self.spaces_remaining}"
                self.roll_disabled = True

    def on_click_notesheet(self, event):
        """
        Switch to Notesheet view when button is clicked.
        """
        notesheet_view = Notesheet(self)
        self.window.show_view(notesheet_view)

    # A function to flip an AI's card face down after they have refuted your guess
    def on_mouse_press(self, x, y, button, key_modifiers):
        # Check if the user clicked on a face_up refute card
        cards = arcade.get_sprites_at_point((x, y), self.all_sprites)

        # If they did, flip it face down again and reset the refute_card
        if self.refute_card in cards:
            self.refute_card.face_down()
            self.refute_card = None

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

    def on_roll_click(self, event):
        if not self.roll_disabled:
            if self.spaces_remaining == 0:
                self.die.roll()
                self.spaces_remaining = self.die.value
                self.spaces_left_text.text = f"Spaces Left: {self.spaces_remaining}"
                self.roll_disabled = True

    # A function to flip an AI's card face down after they have refuted your guess
    def on_mouse_press(self, x, y, button, key_modifiers):
        # Check if the user clicked on a face_up refute card
        cards = arcade.get_sprites_at_point((x, y), self.all_sprites)

        # If they did, flip it face down again and reset the refute_card
        if self.refute_card in cards:
            self.refute_card.face_down()
            self.refute_card = None

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

    def on_roll_click(self, event):
        if not self.roll_disabled:
            if self.spaces_remaining == 0:
                self.die.roll()
                self.spaces_remaining = self.die.value
                self.spaces_left_text.text = f"Spaces Left: {self.spaces_remaining}"
                self.roll_disabled = True

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

    def next_turn(self):
        if self.whose_turn[0]:
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

    def update_spaces_left(self, last_row, last_col):
        if not self.player_piece.within_a_room(self.board.rooms):
            if self.player_piece.row != last_row or self.player_piece.column != last_col:
                self.spaces_remaining -= 1

    def on_close(self):
        """
        Handle window close
        Reset the notesheet on window close
        """
        save_file = "notesheet_state.json"

        # Disable the UI managert and delete the save file
        self.ui_manager.disable

        # Delete the notesheet save file to reset the state
        if os.path.exists(save_file):
            os.remove(save_file)


class InstructionView(arcade.View):

    def on_show_view(self):
        # Set the background color and reset the viewport
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        """ Draw the instruction screen """
        self.clear()

        # Title
        arcade.draw_text("Instructions", self.window.width / 2, self.window.height - 60,
                         arcade.color.WHITE, font_size=40, anchor_x="center")

        # Instructions text
        instructions = [
            "Objective: Deduce the murderer, weapon, and room of the crime.",
            "",
            "Gameplay:",
            "1. Roll the die to move around the board using your arrow keys.",
            "2. Enter rooms to make suggestions (murderer, weapon, room).",
            "3. Other players must disprove your suggestion if possible.",
            "4. Use clues to narrow down suspects, weapons, and rooms.",
            "",
            "Winning:",
            "When confident, make an accusation. If correct, you win!",
            "If incorrect, you’re out of the game.",
            "",
            "Click anywhere to start the game."
        ]

        # Draw each line of instructions
        start_y = self.window.height - 120
        for i, line in enumerate(instructions):
            arcade.draw_text(line, self.window.width / 2, start_y - i * 25,
                             arcade.color.LIGHT_GRAY, font_size=16, anchor_x="center")

        # Footer
        arcade.draw_text("Click to start", self.window.width / 2, 30,
                         arcade.color.WHITE, font_size=18, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ Start the game when the mouse is pressed """
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)



class GameOverView(arcade.View):
    """ View to show when game is over """

    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()
        #self.texture = arcade.load_texture("game_over.png")

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        # TODO: Add text to screen, maybe background overlaid
        arcade.draw_text("Game Over Screen", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", self.window.width / 2, self.window.height / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, re-start the game. """
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)
    

class InstructionView(arcade.View):

    def on_show_view(self):
        # Set the background color and reset the viewport
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        """ Draw the instruction screen """
        self.clear()

        # Title
        arcade.draw_text("Instructions", self.window.width / 2, self.window.height - 60,
                         arcade.color.WHITE, font_size=40, anchor_x="center")

        # Instructions text
        instructions = [
            "Objective: Deduce the murderer, weapon, and room of the crime.",
            "",
            "Gameplay:",
            "1. Roll the die to move around the board using your arrow keys.",
            "2. Enter rooms to make suggestions (murderer, weapon, room).",
            "3. Other players must disprove your suggestion if possible.",
            "4. Use clues to narrow down suspects, weapons, and rooms.",
            "",
            "Winning:",
            "When confident, make an accusation. If correct, you win!",
            "If incorrect, you’re out of the game.",
            "",
            "Click anywhere to start the game."
        ]

        # Draw each line of instructions
        start_y = self.window.height - 120
        for i, line in enumerate(instructions):
            arcade.draw_text(line, self.window.width / 2, start_y - i * 25,
                             arcade.color.LIGHT_GRAY, font_size=16, anchor_x="center")

        # Footer
        arcade.draw_text("Click to start", self.window.width / 2, 30,
                         arcade.color.WHITE, font_size=18, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ Start the game when the mouse is pressed """
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)



class GameOverView(arcade.View):
    """ View to show when game is over """

    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()
        #self.texture = arcade.load_texture("game_over.png")

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        # TODO: Add text to screen, maybe background overlaid
        arcade.draw_text("Game Over Screen", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", self.window.width / 2, self.window.height / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, re-start the game. """
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)
    

def main():
    """ Main function """

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = InstructionView()
    window.show_view(start_view)
    arcade.run()

    game_over = False
    player_won = False
    players_turn = True
    while not game_over:
        while players_turn:
            #if move button is pressed
                #give the player control
                # if player not in a room
                #disable suggestion and accusation buttons
            #if suggestion button is pressed
                #guessedSuspect, guessedWeapon, guessedRoom = guess()
                #if guessedSuspect not in decks and guessedWeapon not in dealtCards and guessedRoom not in dealtCards:
                    #print("No one can give you any new information")
                #else
                    #if guessedSuspect in dealtCards:
                        #print("Someone else has", guessedSuspect)
                    #elif guessedWeapon in dealtCards:
                        #print("Someone else has", guessedWeapon)
                    #elif guessedRoom in dealtCards:
                        #print("Someone else has", guessedRoom)

            # if player in the final room
            #if playerIsActing("make an accusation"):
                #guessedSuspect, guessedWeapon, guessedRoom = guess()
                #if solution == [guessedSuspect, guessedWeapon, guessedRoom]:
                    #PLAYER_WON = True
                #GAME_IS_OVER = True
            players_turn = False
        while not players_turn:
            players_turn = True
    if player_won:
        print("Congrats, you won!")
    else:
        print("Sorry, you lost")


if __name__ == "__main__":
    main()
