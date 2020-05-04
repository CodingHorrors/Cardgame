
""" Code to be used when the player has to type in his cards manually """
prompt = "Player {}, what cards do you want to play? Seperate by comma. Leftmost card is on top.\n>"
play_stack = []

"""
Computes one play step. In a step the player is asked to play cards of his choosing.
After he has played his cards (WHITESPACES DON'T MATTER IN HIS INPUT!!) the cards
get removed from his hand and added to the Play stack. This gets repeated for
each player
"""
while True:
    play_p1 = [play_p1 for play_p1 in input(prompt.format("One")).split(",")]
    """I'M A FUCKING GENIUS"""
    for i in play_p1:
        next = play_p1.pop()
        strip_str = next.strip()
        play_p1.insert(0, strip_str)
    """ GREAT SUCCESS FOR MAINLAND CHINA """
    print(play_p1)
    result = all(elem in hand_p1 for elem in play_p1)
    if result:
        str_play_p1 = " , ".join(play_p1)
        print(str_play_p1)
        print("\nPlayer One has played:", str_play_p1, "\n")
        [hand_p1.remove(i) for i in play_p1]
        play_stack[0:0] = play_p1
        debug(hand_p1)
        break
    else:
        print("These are not cards you currently have in your hand. Try again.")

while True:
    play_p2 = [play_p2 for play_p2 in input(prompt.format("Two")).split(",")]
    for i in play_p2:
        next = play_p2.pop()
        strip_str = next.strip()
        play_p2.insert(0, strip_str)
    result = all(elem in hand_p2 for elem in play_p2)
    if result:
        str_play_p2 = " , ".join(play_p2)
        print("\nPlayer Two has played:", str_play_p2, "\n")
        [hand_p2.remove(i) for i in play_p2]
        play_stack[0:0] = play_p2
        debug(hand_p2)
        break
    else:
        print("These are not cards you currently have in your hand. Try again.")

print("The top card of the stack is:", play_stack[0])

"""Finding the indices of all elements"""
indices_p1 = [index for index, value in enumerate(hand_p1)]



"""Code for sorting the deck after card values
solution that would work only when there is already a sorted list available"""
# print(sorted(random_list, key = deck.index))


"""Backup code for function new_display"""
    display_list = []
    display_count = 0
    for i in hand:
        display_elem = "[" + str(display_count) + "] " + i
        display_list.insert(display_count, display_elem)
        display_count += 1
    return display_list, display_count



"""bad starting hand code"""
hand_p1 = random.sample(shuffled_deck, 6)
[shuffled_deck.remove(i) for i in hand_p1]

hand_p2 = random.sample(shuffled_deck, 6)
[shuffled_deck.remove(i) for i in hand_p2]

hand_p3 = random.sample(shuffled_deck, 6)
[shuffled_deck.remove(i) for i in hand_p3]

hand_p4 = random.sample(shuffled_deck, 6)
[shuffled_deck.remove(i) for i in hand_p4]

hand_p5 = random.sample(shuffled_deck, 6)
[shuffled_deck.remove(i) for i in hand_p5]

hand_p6 = random.sample(shuffled_deck, 6)
[shuffled_deck.remove(i) for i in hand_p6]


"""debug for hand display"""
print("Player One has the following cards:", " , ".join(hand_p1), "\n")
print("Player Two has the following cards:", " , ".join(hand_p2), "\n")
print("Player Three has the following cards:", " , ".join(hand_p3), "\n")
print("Player Four has the following cards:", " , ".join(hand_p4), "\n")
          debug
print(len(shuffled_deck))
print(sorted(shuffled_deck, key=keyf), "\n\n")
          debug
