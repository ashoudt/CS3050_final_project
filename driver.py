from board import Board
import arcade
# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750
SCREEN_TITLE = "Clue Game Board with Piece Movement"

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


def main():
    board = Board(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    decks = board.get_decks()
    killer_cards = board.get_killer()
    arcade.run()
    GAME_IS_OVER = False
    PLAYER_WON = False
    PLAYERS_TURN = True
    while not GAME_IS_OVER:
        while PLAYERS_TURN:
            '''
            Not all of this code is still accurate, but it's a template for how the game should operate
            '''
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
            PLAYERS_TURN = False
        while not PLAYERS_TURN:
            PLAYERS_TURN = True
    if PLAYER_WON:
        print("Congrats, you won!")
    else:
        print("Sorry, you lost")


if __name__ == "__main__":
    main()
