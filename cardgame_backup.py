import random
import textwrap

"""Exception to limit the amount of players to 6"""
class Over_Max(Exception):
    pass
"""Exception to limit the input number to only cards held in hand"""
class not_in_range(Exception):
    pass
"""Exception if there is no 7 in player's input"""
class no_seven(Exception):
    pass

""" Defines our inital variables """
suits = ["Clubs", "Diamonds", "Hearts", "Spades"]

blueprint_deck = [ "Ace", "2", "3", "4", "5", "6", "7",
                   "8", "9", "10", "Jack", "Queen", "King"]
sortvalue = {"Ace": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
             "7": 7, "8": 8, "9": 9, "10": 10, "Jack": 11,
             "Queen": 12, "King": 13}

""" Builds our initial deck. Note, that this is already sorted in the right order """
deck = [i + " of " + j for i in sortvalue for j in suits]




# print(deck, "\n\n")

""" Shuffles the deck """
shuffled_deck = random.sample(deck, len(deck))
for i in range(25):
    shuffled_deck.remove(shuffled_deck[i])
#print(shuffled_deck, "\n\n")


""" Sorts the deck after card values, starting from aces and ending at kings """
"""solution that always works"""
def keyf(card):
    return sortvalue[card.split()[0]]

#print(sorted(shuffled_deck, key=keyf), "\n\n")



""" Defines a function for debugging """
def debug(hand_list, play_stack):
    print("----------------DEBUG----------------")
    d()
    for i in hand_list:
        print(i)
        print(len(i))
        d()
    d()
    print("This is the current stack:", play_stack)
    print("Len of deck:", len(shuffled_deck))
    print("Len of play_stack:", len(play_stack))
    print("----------------DEBUG----------------")

def d():
    print("\n\n\n")


""" Builds the players starting hands """
def starting_hands(players):
    hand_list = []
    for i in range(players):
        hand = random.sample(shuffled_deck, 4)
        [shuffled_deck.remove(i) for i in hand]
        hand_list.append(hand)
        hand.append(f"7 of Diamonds of player {i}")
        hand.append(f"8 of Diamonds of player {i}")
    return hand_list

def empty_stack(cards_left, player_to_draw):
    new_deck = random.sample(play_stack, len(play_stack))
    print("new deck in func empty_stack:",new_deck)
    print("len of new deck:",len(new_deck))
    d()
    new_play_stack = []
    first_new_card = new_deck.pop(0)
    new_play_stack.insert(0, first_new_card)
    print(new_play_stack)
    if cards_left > 0:
        for card in range(cards_left):
            card_draw = new_deck.pop(0)
            player_to_draw.insert(0, card_draw)
    print("new deck in func empty_stack:",new_deck)
    print("len of new deck:",len(new_deck))
    return new_deck, new_play_stack



"""Function to display a list of handcards to the player"""
def new_display(hand):

    display_list = []
    display_count = 0
    for i in hand:
        display_elem = "[" + str(display_count) + "] " + i
        display_list.insert(display_count, display_elem)
        display_count += 1
    return display_list, display_count

"""Function to check if played card matches the value or suit of the top card"""
def validation(card, stack):
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
    if card_suit == stack_suit or card_value == stack_value:
        return True

""" Function to compute what happens when one of the special cards is played"""
def special_cards(card, hand, shuffled_deck, play_stack):
    """BUG BUG BUG: Same player who played the last 7, drew the cards"""
    skip_next_player = False
    if "7" in card:
        next_inc = 1 #increment to track current player, increases with each 7 played
        cards_to_draw = 2
        player_that_played =  hand_list.index(hand)


        while True:

            check_7_in_next_player = False

            try:
                next_player_index = player_that_played + next_inc
                hand_list[next_player_index]
                next_player_disp = next_player_index + 1

            except IndexError:
                next_inc = 0
                next_player_index = 0
                next_player_disp = 1
                player_that_played = 0



            for card in hand_list[next_player_index]:
                if "7" in card:
                    check_7_in_next_player = True




            if check_7_in_next_player == True:
                display_list, display_count = new_display(hand_list[next_player_index])
                played_card = input(f"Player {next_player_disp}, play a 7.\n {display_list}\n>")
                try:
                    int_input = int(played_card)
                    if int_input not in range(display_count):
                        raise not_in_range
                    elif "7" not in hand_list[next_player_index][int_input]:
                        raise no_seven
                    else:
                        played_card = hand_list[next_player_index].pop(int_input)
                        play_stack.insert(0, played_card)
                        next_inc += 1
                        cards_to_draw += 2



                except ValueError:
                    print("\nThis is not an Integer. Try again.\n")
                except not_in_range:
                    print("""\nThis is not the number of a card you have in your hand.
                             \rTry again.\n""")
                except no_seven:
                    print("This is not a 7. Try again.")

            else:
                print(check_7_in_next_player)
                print(f"Player {next_player_disp} draws {cards_to_draw} cards.")
                cards_left = cards_to_draw

                for i in range(cards_to_draw):
                    try:
                        card_draw = shuffled_deck.pop(0)
                        hand_list[next_player_index].insert(0, card_draw)
                        cards_left -= 1
                    except IndexError:
                        shuffled_deck, play_stack = empty_stack(cards_left, hand_list[next_player_index])
                        debug(hand_list, play_stack)
                        return skip_next_player, shuffled_deck, play_stack

    elif "8" in card:
        skip_next_player = True
        return skip_next_player, shuffled_deck, play_stack

    else:
        return skip_next_player, shuffled_deck, play_stack


"""Function that computes one full turn"""
def turn(player, hand, shuffled_deck, play_stack):

    display_list, display_count = new_display(hand)
    skip_next_player = False
    input_number = None
    played = False
    while True:
        prompt = """Player {}, type in the number of the card you want to play.
                \rType draw to draw a card.\nYour Hand:\n{}\n""".format(player, display_list)

        print("\nThe top card of the stack is: ", play_stack[0], "\n")

        int_input = "ass"
        input_number = input(prompt)

        d()

        try:
            int_input = int(input_number)
            if int_input not in range(display_count):
                raise not_in_range
        except ValueError:
            if input_number == "draw":
                card_draw = shuffled_deck.pop(0)
                hand.insert(0, card_draw)
                return skip_next_player, shuffled_deck, play_stack
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
                    validated = True#validation(card, play_stack[0])
                    if validated:

                        validated_card = hand.pop(int_input)
                        play_stack.insert(0, validated_card)
                        played = True
                        skip_next_player, shuffled_deck, play_stack = special_cards(card, hand, shuffled_deck, play_stack)
                    else:
                        print("That's an illegal move.")
                        d()

        if played == True:
            return skip_next_player, shuffled_deck, play_stack

"""generates the first card on the stack"""
"""POSSIBLE BUG: First card on the stack was the same as a card in hand"""


play_stack = []
first_card = shuffled_deck.pop(0)
play_stack.insert(0, first_card)


valid = False
while not valid:
    maximum_players = 6 + 1 # +1 since range would end at 5 otherwise
    try:
        players = int(input("How many players? (Maximum 6)\n>"))
        if players not in range(maximum_players) or players == 0:
            raise Over_Max
        valid = True
    except ValueError:
        print("Not a number, try again.")
    except Over_Max:
        print("Input must be between 1 and 6.")


hand_list = starting_hands(players)

for i in hand_list:
    print(i)
    print(len(i))
    d()

player_range = range(players) #+ 1 because range stops players-1. weird bug.

skip = False
while True:


    for j in player_range:
        if skip == True:
            skip = False
            continue
        current_player = j
        for i in hand_list:
            if hand_list.index(i) == current_player:
                cur_player_display = current_player
                cur_player_display += 1
                skip_next_player, shuffled_deck, play_stack = turn(cur_player_display, i, shuffled_deck, play_stack)
                print("----------------------------------")
                print(play_stack)
                print("-----------------------------------")
                debug(hand_list, play_stack)
            elif not i:
                print(f"""Player {cur_player_display} has no cards left in his hand.
                      \rPlayer {cur_player_display} wins!""")
                exit()

        if skip_next_player == True:
            skip = True
