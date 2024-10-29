from player import Player
from board import Board
from ui_elements import GameUI
from deck import Deck
from die import Die
import arcade
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


def playerIsActing(action):
    '''
    Test text-based code, will be replaced with buttons

    playerIsActing = ""
    while playerIsActing != "y" and playerIsActing != "n":
        playerIsActing = input(f"Do you wish to {action} this turn? (y/n)\n")
        if playerIsActing != "y" and playerIsActing != "n":
            print("Invalid input")
    if playerIsActing == "y":
        return True
    else:
        return False
    '''


def guess():
    '''
    Test text-based code, the logic is useful but we aren't planning on using text in the final product

    guessedSuspect = ""
    while guessedSuspect not in VALID_SUSPECTS:
        guessedSuspect = input("Guess a suspect: ")
        if guessedSuspect not in VALID_SUSPECTS:
            print("Invalid input")
    guessedWeapon = ""
    while guessedWeapon not in VALID_WEAPONS:
        guessedWeapon = input("Guess a weapon: ")
        if guessedWeapon not in VALID_WEAPONS:
            print("Invalid input")
    guessedRoom = ""
    while guessedRoom not in VALID_ROOMS:
        guessedRoom = input("Guess a room: ")
        if guessedRoom not in VALID_ROOMS:
            print("Invalid input")
    return guessedSuspect, guessedWeapon, guessedRoom
    '''


class Game(arcade.Window):
    def __init__(self, width, height, title):
        """
        Set up the application.
        """
        super().__init__(width, height, title)

        # Create the board
        self.board = Board()
        self.board_size = self.board.board_size
        self.board_center_x = self.board.board_center_x
        self.board_center_y = self.board.board_center_y
        self.background_texture = self.board.background_texture

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
                else:
                    # TODO: Implement logic for more or less than 4 players
                    pass

        # List for all sprites
        self.all_sprites = arcade.SpriteList()
        self.all_sprites.append(self.die)
        self.all_sprites.append(self.player_piece)
        for self.playerDeck in self.all_decks:
            for self.card in self.playerDeck:
                self.all_sprites.append(self.card)

        # Create UI manager for buttons and notesheet
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()

        # Create the GameUI instance
        self.game_ui = GameUI(self.ui_manager)

        # Create the roll button and disabled roll button
        self.roll_button = arcade.gui.UIFlatButton(text="Roll", width=200, style=self.game_ui.default_style)
        # self.roll_button_disabled = arcade.gui.UIFlatButton(text="Roll", width=200, style=self.game_ui.disabled_style)
        self.game_ui.h_box.add(self.roll_button.with_space_around(left=80))
        # self.game_ui.h_box.add(self.roll_button_disabled.with_space_around(right=80))
        self.roll_button.on_click = self.on_roll_click

        self.roll_disabled = False

        # Create the text
        spaces_left_x = 565
        spaces_left_y = 30
        self.spaces_left_text = arcade.Text(
            f"Spaces Left: {self.spaces_remaining}",
            spaces_left_x,
            spaces_left_y,
            arcade.color.WHITE,
            DEFAULT_FONT_SIZE,
        )

    def on_roll_click(self, event):
        if self.spaces_remaining == 0:
            self.die.roll()
            self.spaces_remaining = self.die.value
            self.spaces_left_text.text = f"Spaces Left: {self.spaces_remaining}"

    def on_draw(self):
        """
        Render the screen.
        """
        # Clear the screen
        self.clear()

        # Draw the Clue board in the center of the window
        arcade.draw_texture_rectangle(self.board_center_x, self.board_center_y,
                                      self.board_size, self.board_size,
                                      self.background_texture)

        # Draw the player's piece on the board and the cards
        self.all_sprites.draw()

        # Draw UI elements
        self.ui_manager.draw()

        if self.spaces_remaining != 0:
            self.spaces_left_text.draw()
            self.roll_disabled = True
        else:
            self.roll_disabled = False

    def on_key_press(self, key, modifiers):
        """
        Handle player movement using arrow keys.
        """
        if key == arcade.key.ESCAPE:
            arcade.close_window()
            arcade.exit()

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

    def update_spaces_left(self, last_row, last_col):
        if not self.player_piece.within_a_room(self.board.rooms):
            if self.player_piece.row != last_row or self.player_piece.column != last_col:
                self.spaces_remaining -= 1


    def on_close(self):
        save_file = "notesheet_state.json"
        # Disable the UI managert and delete the save file
        self.ui_manager.disable

        # Delete the notesheet save file to reset the state
        if os.path.exists(save_file):
            os.remove(save_file)

        # Call the parent's on_close method to handle default close behavior
        super().on_close()

def main():
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
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
