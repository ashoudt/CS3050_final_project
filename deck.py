# Define functions to maintain a deck of cards
import random
import arcade

# ***Define our constants (size of assets/values)***
CARD_WIDTH = 108
CARD_HEIGHT = 124
CARD_SCALE = 0.75

TOTAL_CARDS = 21
TOTAL_GAME_CARDS = 18  # removed the 3 murderer cards

SUSPECT_CARD_VALUES = ["Mrs Peacock", "Mrs White", "Miss Scarlet", "Prof Plum", "Col Mustard", "Mr Green"]
WEAPON_CARD_VALUES = ["Candlestick", "Wrench", "Rope", "Lead Pipe", "Knife", "Revolver"]
ROOM_CARD_VALUES = ["Conservatory", "Dining Room", "Library", "Billiard Room", "Lounge", "Kitchen", "Ball Room",
                    "Study", "Hall"]

CARD_BACK_IMAGE = r"assets/clue cards/cardBack.png"


# A Card Class that keeps track of what type of card it is
# (suspect, weapon, or room), what value that card holds, and the image
class Card(arcade.Sprite):
    def __init__(self, card_type, value, scale):
        self.card_type = card_type
        self.value = value

        self.card_width = CARD_WIDTH * scale
        self.card_height = CARD_HEIGHT * scale

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
            suspect_card = Card("Suspect", SUSPECT_CARD_VALUES[i], CARD_SCALE)
            self.all_cards.append(suspect_card)
            self.all_sprites.append(suspect_card)
            weapon_card = Card("Weapon", WEAPON_CARD_VALUES[i], CARD_SCALE)
            self.all_cards.append(weapon_card)
        for i in range(9):
            room_card = Card("Room", ROOM_CARD_VALUES[i], CARD_SCALE)
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
        #print("KILLER\n****")
        #for card in self.killer_cards:
            #print(card.value)
        #print("****")
        #print("\nDECK SIZE:", deck_size)
        #for deck in self.all_decks:
            #print("****")
            #for card in deck:
                #print(card.value)

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

    def get_killer(self):
        return self.killer_cards