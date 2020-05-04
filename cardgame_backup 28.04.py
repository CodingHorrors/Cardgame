#Neunerln v 1.0
# © Alexander Wittich

from pathlib import Path
import random
import os
import pandas


"""Exception to limit the amount of players to 6"""
class Over_Max(Exception):
    pass
"""Exception to limit the input number to only cards held in hand"""
class not_in_range(Exception):
    pass
"""Exception if there is no 7 in player's input"""
class no_seven(Exception):
    pass

""" creates the initial deck """
suits = ["Clubs", "Diamonds", "Hearts", "Spades"]

blueprint_deck = [ "Ace", "2", "3", "4", "5", "6", "7",
                   "8", "9", "10", "Jack", "Queen", "King"]
sortvalue = {"Ace": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
             "7": 7, "8": 8, "9": 9, "10": 10, "Jack": 11,
             "Queen": 12, "King": 13}

""" Builds our initial deck. Note, that this is already sorted in the right order """
deck = [i + " of " + j for i in sortvalue for j in suits]


""" Shuffles the deck """
shuffled_deck = random.sample(deck, len(deck))

""" Sorts the deck after card values, starting from aces and ending at kings """
"""solution that always works"""
def keyf(card):
    return sortvalue[card.split()[0]]


""" Defines a function for debugging """
def debug(hand_list, play_stack):

    print("----------------DEBUG----------------")
    for i in hand_list:
        print(i)
        print(len(i))
    d()
    print("This is the current stack:", play_stack)
    print("Len of deck:", len(shuffled_deck))
    print("Len of play_stack:", len(play_stack))
    print("----------------DEBUG----------------")

"""function for readability"""
def d():
    print("\n\n\n")


""" Builds the players starting hands """
def starting_hands(players):
    hand_list = []
    for i in range(players):
        hand = random.sample(shuffled_deck, 6)
        [shuffled_deck.remove(i) for i in hand]
        hand_list.append(hand)
    return hand_list


"""Function that determines what happens when deck is empty and a draw is attempted"""
def empty_deck(cards_left, player_to_draw):

    global skip_next_player
    global change_direction
    global shuffled_deck
    global play_stack

    d()
    if ace_round == True:
        shuffled_deck = random.sample(play_stack, len(play_stack))
        placeholder_deck = []    #creates a new deck because modifying a list while iteration
        play_stack = [i for i in play_stack if "Ace" in i] #functions not as we want it to
        [placeholder_deck.append(i) for i in shuffled_deck if "Ace" not in i]
        shuffled_deck = placeholder_deck
        if cards_left > 0:
            try:
                for card in range(cards_left):
                    card_draw = shuffled_deck.pop(0)
                    player_to_draw.insert(0, card_draw)
            except IndexError:  #if no cards are left to draw
                pass

    else:
        debug(hand_list, play_stack)
        d()
        first_new_card = play_stack.pop(0)
        shuffled_deck = play_stack
        shuffled_deck = random.sample(shuffled_deck, len(shuffled_deck))
        play_stack = []
        play_stack.insert(0, first_new_card)
        if cards_left > 0:
            try:
                for card in range(cards_left):
                    card_draw = shuffled_deck.pop(0)
                    player_to_draw.insert(0, card_draw)
            except IndexError:
                pass
            debug(hand_list, play_stack)

"""Function to display a list of handcards to the player"""
def new_display(hand):

    display_list = []
    display_count = 0
    for i in hand:
        display_elem = "[" + str(display_count) + "] " + i
        display_list.insert(display_count, display_elem)
        display_count += 1
    display_list = ' '.join(display_list)
    return display_list, display_count

"""Function to check if played card matches the value or suit of the top card"""
def validation(card, stack):

    global chosen_suit
    global suit_wish
    global ace_round

    for i in suits:
        if i in card:
            card_suit = i
        if i in stack:
            stack_suit = i
    for i in blueprint_deck:
        if i in card:
            card_value = i
        if i in stack:
            stack_value = i

    if suit_wish == True:
        stack_suit = chosen_suit


    if ace_round == True and card_value != "Ace":
        return False

    if card_suit == stack_suit or card_value == stack_value:
        return True
    elif "10" in card:
        return True

""" Function to compute what happens when one of the special cards is played"""
def special_cards(card, hand):


    global skip_next_player
    global change_direction
    global player_range
    global chosen_suit
    global suit_wish
    global ace_round
    global aces_in_stack


    if "7" in card:
        next_inc = 0        #initial values for determination of playorder
        inc_value = 1
        if change_direction == True:
            inc_value = -1
        next_inc += inc_value

        player_that_played =  hand_list.index(hand)

        cards_to_draw = 2

        while True:

            check_7_in_next_player = False

            next_player = player_that_played + next_inc
            """checks if last player or first player is reached and changes the
            next player accordingly to uphold the turn order"""
            if next_player == players:
                next_player = 0
                next_inc = 0
                player_that_played = 0
            elif next_player < 0:
                next_player = player_range[-1]
                next_inc = 0
                player_that_played = player_range[-1]

            next_player_disp = next_player + 1

            for card in hand_list[next_player]:
                if "7" in card:
                    check_7_in_next_player = True

            #CHANGE
            if check_7_in_next_player == True:
                display_list, display_count = new_display(hand_list[next_player])
                played_card = input(f"Player {next_player_disp}, play a 7.\n {display_list}\n>")
                try:
                    int_input = int(played_card)
                    if int_input not in range(display_count):
                        raise not_in_range
                    elif "7" not in hand_list[next_player][int_input]:
                        raise no_seven
                    else:
                        played_card = hand_list[next_player].pop(int_input)
                        play_stack.insert(0, played_card)
                        cards_to_draw += 2
                        next_inc += inc_value



                except ValueError:
                    print("\nThis is not an Integer. Try again.\n")
                except not_in_range:
                    print("""\nThis is not the number of a card you have in your hand.
                             \rTry again.\n""")
                except no_seven:
                    print("This is not a 7. Try again.")

            else:
                print(f"Player {next_player_disp} draws {cards_to_draw} cards.")
                cards_left = cards_to_draw
                for i in range(cards_to_draw):
                    try:
                        card_draw = shuffled_deck.pop(0)
                        hand_list[next_player].insert(0, card_draw)
                        cards_left -= 1
                    except IndexError:
                        print("Index Error occurred. Cards left:", cards_left)
                        empty_deck(cards_left, hand_list[next_player])
                        debug(hand_list, play_stack)
                        break
                break

    elif "8" in card:
        skip_next_player = True

    elif "9" in card:
        if change_direction == True:
            change_direction = False
        else:
            change_direction = True

    elif "10" in card:
        display_list, display_count = new_display(suits)
        while True:
            try:
                chosen_suit = int(input(f"What suit do you want?\n{display_list}\n>"))
                if chosen_suit not in range(display_count):
                    raise not_in_range
                chosen_suit = suits[chosen_suit]
                suit_wish = True
                break
            except ValueError:
                print("This is not an Integer. Try again.")
            except not_in_range:
                print("This is not a valid input. Try again.")

    elif "Ace" in card:
        aces_in_stack = 0       #checks how many aces are currently
        for i in play_stack:    #in the play stack
            if "Ace" in i:
                aces_in_stack += 1
        if ace_round == False:
            input_list = ["No", "Yes"]
            display_list, display_count = new_display(input_list)
            while True:
                try:
                    """input 0 equals False, input 1 equals True"""
                    ace_round = int(input(f"Do you want to start an ace round?\n{display_list}\n>"))
                    if ace_round not in range(display_count):
                        raise not_in_range

                    break
                except ValueError:
                    print("This is not an Integer. Try again.")
                except not_in_range:
                    print("This is not a valid input. Try again.")
        elif ace_round == True and aces_in_stack == 4:
            print("All aces have been played. Ace round is now over.")
            ace_round = False


"""Function that computes one full turn"""
def turn(player, hand):

    global suit_wish
    global ace_round
    global aces_in_stack

    display_list, display_count = new_display(hand)

    input_number = None
    played = False
    int_input = None
    #CHANGE
    while True:
        prompt = """Player {}, type in the number of the card you want to play.
                \rType draw to draw a card.\nYour hand:\n{}\n>""".format(player, display_list)

        print("\nThe top card of the stack is: ", play_stack[0], "\n")

        if suit_wish == True:
            print("The suit of the top card is:", chosen_suit)

        if ace_round == True:
            prompt = """Ace round is currently in effect. Player {}, play an ace or draw a card.
             \rNumber of aces on the stack: {}\nYour hand:\n{}\n>""".format(player, aces_in_stack, display_list)

        input_number = input(prompt)

        d()
        try:
            int_input = int(input_number)
            if int_input not in range(display_count):
                raise not_in_range
        except ValueError:
            if input_number == "draw":
                validation_list = []
                for i in hand:
                    validation_elem =  validation(i, play_stack[0])
                    validation_list.append(validation_elem)
                if True not in validation_list:
                    try:
                        card_draw = shuffled_deck.pop(0)
                        hand.insert(0, card_draw)
                        break
                    except IndexError:
                        empty_deck(1, hand)
                        break
                else:
                    print("""You have one or more playable cards in your hand.
                            \rDrawing is only allowed if you're unable to make a play.""")

            else:
                print("""\nThis is not an Integer. Try again.
                     \rType draw to draw a card.\n""")
            d()
        except not_in_range:
            print("""\nThis is not the number of a card you have in your hand.
                     \rTry again. Type draw to draw a card.\n""")
            d()

        if int_input in range(display_count):
            for i in range(display_count):
                if i == int_input:
                    card = hand[i]
                    validated = validation(card, play_stack[0])

                    if validated:

                        validated_card = hand.pop(int_input)
                        play_stack.insert(0, validated_card)
                        played = True
                        suit_wish = False
                        special_cards(card, hand)

                    else:
                        print("That's an illegal move.")
                        d()

        if played == True:
            break


""" Initial Variables"""
valid_input_players = False
current_player = 0
aces_in_stack = 0
ace_round = False
skip_next_player = False
change_direction = False
suit_wish = False

"""determines how many people are playing by user input"""
while not valid_input_players:
    maximum_players = 6 + 1 # +1 since range would end at 5 otherwise
    try:
        players = int(input("How many players? (Maximum 6)\n>"))
        if players not in range(1, maximum_players):
            raise Over_Max
        valid_input_players = True
    except ValueError:
        print("Not a number, try again.")
    except Over_Max:
        print("Input must be between 1 and 6.")
player_range = range(players)
print("PLAYER RANGE:", player_range)
"""creates a list of hands"""
hand_list = starting_hands(players)


"""generates the first card on the stack"""
play_stack = []
first_card = shuffled_deck.pop(0)
play_stack.insert(0, first_card)

"""start of the main computation"""
while True:

    hand = hand_list[current_player]
    print(hand)
    cur_player_display = current_player #changing ordinal to cardinal number
    cur_player_display += 1             #for display to user

    turn(cur_player_display, hand)
    print("----------------------------------")
    print(play_stack)
    print("-----------------------------------")
    d()

    if not hand:
        print(f"""Player {cur_player_display} has no cards left in his hand.
                 \rPlayer {cur_player_display} wins!""")
        exit()

    if change_direction == False:
        inc = 1
    if change_direction == True:
        inc = -1

    if skip_next_player == True:
        current_player += inc
        skip_next_player = False

    current_player += inc

    if current_player == players:   # executes when second to last player plays 8
        current_player = player_range[0]
    elif current_player == players + 1:  #executes when last player plays 8
        current_player = player_range[1]
    elif current_player == -1:          #same as above in reverse
        current_player = player_range[-1]
    elif current_player == -2:
        current_player = player_range[-2]
