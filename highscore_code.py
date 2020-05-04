from pathlib import Path
import csv
import os
import pandas

def new_display(hand):

    display_list = []
    display_count = 0
    for i in hand:
        display_elem = "[" + str(display_count) + "] " + i
        display_list.insert(display_count, display_elem)
        display_count += 1
    display_list = ' '.join(display_list)
    return display_list, display_count


p = r"C:\Users\Alex\Documents\Programming\ProjectCardgame\score.csv"


if not Path(p).is_file():
    open(p, mode='w+', newline='')
else:
    print("ass")
start_game = False
while not start_game:

    print("Welcome to Mau Mau. Please select one of the following options:")
    main_menu = input("[0] Start a new game [1] Highscore Settings [2] Exit\n>")

    if main_menu == "0":
        valid_input_players = False
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

        """creates a list of hands"""
        hand_list = starting_hands(players)


        print("Do you want to enable score tracking for this round?")
        while True:
            track_selection = input("[0] No [1] Yes\n>")
            if track_selection == "0":
                break
            elif track_selection == "1":
                with open(p, mode='r', newline='') as score_file:
                    score_object = pandas.read_csv(score_file, index_col=0)
                    name_list_temp = score_object["Name"].tolist()
                if len(name_list_temp) < players:
                    print("Not enough names detected to track score.",
                          "Game will start without tracking.")
                    break
                else:
                    player_list = []
                    for i in range(1, players + 1 ): #change to kardinal numbers
                        while True:
                            display_name_list, display_count = new_display(name_list_temp)
                            name_of_player = int(input(f"Name of Player {i}:\n{display_name_list}\n>"))
                            if name_of_player in range(display_count):
                                player_list.append(name_list_temp[name_of_player])
                                name_list_temp.remove(name_list_temp[name_of_player])
                                break
                            else:
                                print("Not a valid input.")
                    print(player_list)
                    start_game = True
                    break

            else:
                print("Not a valid input.")

    elif main_menu == "1":
        while True:
            setting_selection = input("[0] View Highscores [1] Add names "
                                      "[2] Delete Names [3] Reset Everything "
                                      "[4] Go back\n>")
            if setting_selection == "0":
                with open(p, mode='r', newline='') as score_file:
                    if os.path.getsize(p) == 0:
                        print("No Scores detected.")
                        continue
                    score_read = pandas.read_csv(score_file, index_col=0)
                    if score_read.empty == True:
                        print("No scores detected.")
                    else:
                        print(score_read)

            elif setting_selection == "1":
                new_names = input("Add one or multiple new names, seperated by ,\n>")
                new_names = new_names.replace(" ","").split(",")
                print(new_names)
                with open(p, mode='a+', newline='') as score_file:
                    data = 0
                    if os.path.getsize(p) == 0:
                        score_panda = pandas.DataFrame(data=data,
                                       index= new_names,
                                       columns= ["Score"])
                        score_panda.to_csv(score_file)
                        print(score_file)
                    else:
                        append_frame = pandas.DataFrame(data=data,
                                       index= new_names,
                                       columns= ["Score"])
                        score_file.seek(0)
                        init_panda = pandas.read_csv(score_file, index_col=0)
                        new_frame = init_panda.append(append_frame, ignore_index=False)
                        with open(p, mode='w', newline='') as new_score_file:
                            new_frame.to_csv(new_score_file)
                        print(new_frame)

            elif setting_selection == "2":
                finished = False
                with open(p, mode='a+', newline='') as score_file:
                    while not finished:
                        score_file.seek(0)
                        try:
                            score_read = pandas.read_csv(score_file, index_col=0)
                        except pandas.errors.EmptyDataError:
                            print("No names detected. Add names first.")
                            break

                        name_list = score_read.index.tolist()
                        print(name_list)
                        if not name_list:
                            print("No Names detected. Add names first.")
                            break
                        name_list_disp, display_count = new_display(name_list)
                        try:
                            del_choice = int(input("Select Name to delete it. Type 999 "
                                                    f"to finish.\n{name_list_disp}\n>"))
                        except ValueError:
                            print("Not an integer.")
                        if del_choice in range(display_count):
                            del_choice = name_list[del_choice]
                            new_frame = score_read.drop(del_choice, axis=0)
                            with open(p, mode='w', newline='') as new_score_file:
                                new_frame.to_csv(new_score_file)
                            print(new_frame)
                        elif del_choice == 999:
                            finished = True
                        else:
                            print("Not a valid input.")


            elif setting_selection == "3":
                confirm_list = ["No", "Yes"]
                disp_con, display_count = new_display(confirm_list)
                while True:
                    try:
                        confirm = int(input(f"Are you sure?\n{disp_con}\n>"))
                        if confirm == True:
                            with open(p, mode='w', newline='') as score_file:
                                break    #truncates the file by opening it in 'w'
                        elif confirm == False:
                            break
                        else:
                            print("Not a valid input.")
                    except ValueError:
                        print("Type in a valid integer.")

            elif setting_selection == "4":
                break

    elif main_menu == "2":
        exit()
       #break command to break out of outermost loop and start the game
