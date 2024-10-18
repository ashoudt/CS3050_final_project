# Define functions to maintain a deck of cards
import random
import arcade

# ***Define our constants (size of assets/values)***
CARD_WIDTH = 108
CARD_HEIGHT = 124

TOTAL_CARDS = 21
TOTAL_GAME_CARDS = 18  # removed the 3 murderer cards

SUSPECT_CARD_VALUES = ["Mrs Peacock", "Mrs White", "Miss Scarlet", "Prof Plum", "Col Mustard", "Mr Green"]
WEAPON_CARD_VALUES = ["Candlestick", "Wrench", "Rope", "Lead Pipe", "Knife", "Revolver"]
ROOM_CARD_VALUES = ["Conservatory", "Dining Room", "Library", "Billiard Room", "Lounge", "Kitchen", "Ball Room",
                    "Study", "Hall"]

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900

CARD_BACK_IMAGE = r"assets/clue cards/cardBack.png"


# A Card Class that keeps track of what type of card it is
# (suspect, weapon, or room), what value that card holds, and the image
class Card(arcade.Sprite):
    def __init__(self, card_type, value, scale=1):
        self.card_type = card_type
        self.value = value

        # Set asset based on card value
        self.image_filename = f"assets/clue cards/{self.value.lower().replace(' ', '')}.png"
        self.is_face_up = False  # Show the back of the card for non-player cards

        # Call the parent class from Python Arcade
        # super().__init__(self.image_filename, scale, hit_box_algorithm="None")
        super().__init__(CARD_BACK_IMAGE, scale, hit_box_algorithm="None")

    # Show the back of the card
    def face_down(self):
        self.texture = arcade.load_texture(CARD_BACK_IMAGE)
        self.is_face_up = False

    # Show the front of the card
    def face_up(self):
        self.texture = arcade.load_texture(self.image_filename)
        self.is_face_up = True


# A Deck Class that creates the decks for the AIs and the Player
class Deck:
    def __init__(self):

        self.held_cards = []
        self.all_cards = []
        self.all_decks = []
        self.killer_cards = []
        self.all_sprites = arcade.SpriteList()

    # Function to set up/deal cards
    def deal(self, num_players):
        # Create all the cards in the game
        for i in range(6):
            suspect_card = Card("Suspect", SUSPECT_CARD_VALUES[i], 1)
            self.all_cards.append(suspect_card)
            self.all_sprites.append(suspect_card)
            weapon_card = Card("Weapon", WEAPON_CARD_VALUES[i], 1)
            self.all_cards.append(weapon_card)
        for i in range(9):
            room_card = Card("Room", ROOM_CARD_VALUES[i], 1)
            self.all_cards.append(room_card)

        # Shuffle the cards
        random.shuffle(self.all_cards)

        # Choose 3 cards (one of each type) for the killer
        self.choose_killer(self.all_cards, self.killer_cards)

        # Put cards into piles based on the number of players
        deck_size = int(TOTAL_GAME_CARDS / num_players)  # Game cards excludes the three killer cards
        extra_cards = TOTAL_GAME_CARDS - (deck_size * num_players)
        temp_deck = []

        for player in range(num_players):
            for index in range(deck_size):
                temp_deck.append(self.all_cards.pop())

            # Add any extra cards to the deck
            if extra_cards != 0:
                temp_deck.append(self.all_cards.pop())
                extra_cards -= 1

            self.all_decks.append(temp_deck)
            temp_deck = []

        # Shuffle decks so the first players don't always get the extra cards
        random.shuffle(self.all_decks)

        # Flip over the player's cards
        for card in self.all_decks[0]:
            card.face_up()

        # TODO: Assign decks to NPCs and Player

        # Print cards in each deck (for testing purposes)
        print("KILLER\n****")
        for card in self.killer_cards:
            print(card.value)
        print("****")
        print("\nDECK SIZE:", deck_size)
        for deck in self.all_decks:
            print("****")
            for card in deck:
                print(card.value)

    # Function to add 3 cards (one of each type) to the envelope in the middle of the board
    def choose_killer(self, all_cards, killer_cards):
        suspect = False
        weapon = False
        room = False
        for card in all_cards:
            if card.card_type == "Suspect" and not suspect:
                killer_cards.append(card)
                all_cards.remove(card)
                suspect = True
            elif card.card_type == "Weapon" and not weapon:
                killer_cards.append(card)
                all_cards.remove(card)
                weapon = True
            elif card.card_type == "Room" and not room:
                killer_cards.append(card)
                all_cards.remove(card)
                room = True

    def get_all_cards(self):
        return self.all_decks


# TODO: Delete this class once below visuals are implemented in driver!
class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        # Set up the application
        super().__init__(width, height, title)

        # Draw the board
        self.background_texture = arcade.load_texture("ClueBoard.jpeg")
        self.board_size = 630
        self.board_center_x = 600
        self.board_center_y = 450

        # Draw the cards
        num_players = 4
        deck = Deck()
        deck.deal(num_players)
        self.all_decks = deck.get_all_cards()

        padding = 300  # padding for horizontal edges of the screen
        vertical_padding = 150  # padding for vertical  edges of the screen

        # Position cards on the screen
        for deck in self.all_decks:
            card_space = (SCREEN_WIDTH - (padding * 2)) / len(deck)  # divide remaining space among cards
            current_card_space = 0  # number of cards already on this part of the screen

            # Position for cards on the screen (padding + # cards on screen + center of next card space)
            changing_pos = int(padding + current_card_space + (card_space / 2))
            vertical_changing_pos = int(vertical_padding + current_card_space + (card_space / 2))

            # Distance from the outer edge of the screen
            static_pos = 100

            for card in deck:
                # BOTTOM HORIZONTAL (Player)
                if deck == self.all_decks[0]:
                    card.position = changing_pos, static_pos
                # LEFT VERTICAL
                elif deck == self.all_decks[1]:
                    card.position = static_pos, vertical_changing_pos
                # RIGHT VERTICAL
                elif deck == self.all_decks[2]:
                    card.position = SCREEN_WIDTH - static_pos, vertical_changing_pos
                # TOP HORIZONTAL
                elif deck == self.all_decks[3]:
                    card.position = changing_pos, SCREEN_HEIGHT - static_pos
                # STACK IN CORNER
                else:
                    # TODO: Print a pile in the corners (once final screen size is determined)
                    print("card stack")

                changing_pos += card_space
                vertical_changing_pos += card_space

    def on_draw(self):
        # Clear the screen
        self.clear()

        # Draw the board
        arcade.draw_texture_rectangle(self.board_center_x, self.board_center_y,
                                      self.board_size, self.board_size,
                                      self.background_texture)

        # Draw the cards
        for deck in self.all_decks:
            for card in deck:
                card.draw()


# Main (for testing purposes)
def main():
    # Create a screen to test card visuals
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, "Card Test")
    arcade.run()


if __name__ == "__main__":
    main()
