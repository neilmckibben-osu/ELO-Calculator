import ast
import os
import operator
ten = 10.00

def main():
    list = dict()
    logs = dict()
    # if logs is empty, can assume list is the same
    if os.stat("logs.txt").st_size != 2:
        log_file = open("logs.txt", "r").read()
        list_file = open('list.txt', 'r').read()
        with open('logs.txt', 'r') as f:
            s = f.read()
            logs = ast.literal_eval(s)
        with open('list.txt', 'r') as f:
            s = f.read()
            list = ast.literal_eval(s)
        print("Here are all the current players: ")
        display_stats(list, logs)
    else:
        print("There are no players at the moment.")

    string_in = input("Would you like to add players? (Y/N): ")

    player_add = True
    while player_add:
        if string_in.upper() in ('Y', 'N'):
            if (string_in.upper() == 'Y'):
                playerAdd = False
                multiple = True
                while (multiple == True):
                    name = input("Enter the name of the player: ")
                    if name not in list:
                        addPlayer(name, list, logs)
                        # check to make sure it's a valid input
                        check = input("Would you like to add more players? (Y/N): ")
                        player_add_two = True
                        while player_add_two:
                            if check.upper() in ('Y', 'N'):
                                player_add_two = False
                                if check.upper() == 'N':
                                    multiple = False
                                    player_add = False
                            else:
                                print("Invalid input - please try again.")
                                check = input("Would you like to add more players? (Y/N): ")
                    else:
                        print("That name is already in the dictionary, please enter a different name.")
            else:
                player_add = False
        else:
            print("Invalid input - please try again.")
            string_in = input("Would you like to add players? (Y/N): ")

    exitStatus = True
    while exitStatus:
        print('List of commands: "remove-player", "odds", "match", "display-stats", "reset-stats"')
        command = input('Enter a command or enter "exit" to quit: ')
        if command.upper() == "EXIT":
            print("Exiting...")
        elif command == 'remove-player':
            remove_name = input("Enter name of player to remove: ")
            if remove_name in list:
                removePlayer(remove_name, list, logs)
            else:
                print("There is not a player with that name in the database!")
        elif command == 'odds':
            if len(list) > 1:
                print("Pick 2 players from the database: ")
                for name in list:
                    print(str(name) + ' ')

                player_one = input("First player's name: ")
                player_two = input("Second player's name: ")
                print(
                    'There is a ' + str(odds(player_one, player_two, list)) + ' chance that ' + player_one + ' will ' +
                    'win against ' + player_two)
            else:
                print("You need more than 2 players for this command!")
        elif command == 'match':
            if len(list) > 1:
                winner = input("Input the winner: ")
                loser = input("Input the loser: ")
                match(winner, loser, list, logs)
                print(winner + "'s new ELO value is " + str(list[winner]) + " and the loser's new ELO value is " + str(
                    list[loser])
                      + ".")
            else:
                print("You need more than 2 players for this command!")
        elif command == 'display-stats':
            if len(list) > 1:
                print("Displaying stats...")
                display_stats(list, logs)
            else:
                print("There is no one playing at the moment.")
        elif command == 'reset-stats':
            print("Wiping logs...")
            clearLogs(logs, list)
            print("Done")
        else:
            print("Input not recognized, please retry. ")

        quit_out = input("Would you like to exit now? (Y/N): ")
        if quit_out.upper() not in ('N', 'Y'):
            quit = True
            while (quit):
                loop_input = input("Invalid input, please enter (Y/N)")
                if loop_input.upper() in ('N', 'Y'):
                    quit = False
        if quit_out.upper() == 'Y':
            exitStatus = False
            print('Goodbye!')
    print("Updating logs...")
    update_logs(logs, list)
    print("Exiting out...")


def sort_values(list):
    sorted_list = reversed(sorted(list.items(), key=operator.itemgetter(1)))
    return sorted_list

def addPlayer(name, list, logs):
    list[name] = 1500.00
    logs[name] = [0, 0, 0, 32]


def removePlayer(name, list, logs):
    del list[name]
    del logs[name]


def odds(player_one, player_two, list):
    elo_one = list[player_one]
    elo_two = list[player_two]
    difference = elo_two-elo_one
    probability = (1.00 / (1.00 + (ten ** ((difference)/400))))

    return probability


def match(winner, loser, list, logs):
    calc(winner, loser, 1, list, logs)


def calc(player_one, player_two, win, list, logs):
    elo_one = list[player_one]
    elo_two = list[player_two]
    trans_one = ten ** (elo_one/400)
    trans_two = ten ** (elo_two/400)
    expected_one = (trans_one/(trans_one+trans_two))
    expected_two = (trans_two/(trans_one+trans_two))
    # if win is 1, player_one wins, 1/2 is a tie, 1 player2 wins
    result_one = win
    result_two = 0

    k_value_one = logs[player_one][3]
    k_value_two = logs[player_two][3]
    (new_elo_one) = (elo_one + k_value_one*(result_one - expected_one))
    new_elo_two = (elo_two + k_value_two*(result_two - expected_two))
    decimal_new_elo_one = float("{0:.2f}".format(new_elo_one))
    decimal_new_elo_two = float("{0:.2f}".format(new_elo_two))
    # update list
    list[player_one] = float(decimal_new_elo_one)
    list[player_two] = float(decimal_new_elo_two)

    # updates logs
    if result_one == 1:
        record_one = logs[player_one]
        record_one[0] = record_one[0] + 1
        logs[player_one] = record_one
        record_two = logs[player_two]
        record_two[2] = record_two[2] + 1
        logs[player_two] = record_two
    elif result_one == 0:
        record_one = logs[player_one]
        record_one[2] = record_one[2] + 1
        logs[player_one] = record_one
        record_two = logs[player_two]
        record_two[0] = record_two[0] + 1
        logs[player_one] = record_two
    else:
        record_one = logs[player_one]
        record_one[1] = record_one[1]+1
        logs[player_one] = record_one
        record_two = logs[player_two]
        record_two[1] = record_two[1] + 1
        logs[player_one] = record_two

    elo_check = [elo_one, elo_two]

    # updates k-values
    for x in elo_check:
        if x > 2400:
            if elo_one > 2400:
                record_one = logs[player_one]
                record_one[3] = 16
                logs[player_one] = record_one
            else:
                record_two = logs[player_two]
                record_two[3] = 16
                logs[player_two] = record_two
        elif 2400 > x > 2100:
            if 2400 > elo_one > 2100:
                record_one = logs[player_one]
                record_one[3] = 24
                logs[player_one] = record_one
            else:
                record_two = logs[player_two]
                record_two[3] = 24
                logs[player_two] = record_two

        else:
            if elo_one < 2100:
                record_one = logs[player_one]
                record_one[3] = 32
                logs[player_one] = record_one
            else:
                record_two = logs[player_two]
                record_two[3] = 32
                logs[player_two] = record_two

def display_stats(list, logs):
    list = sort_values(list)
    rank = 1
    for name in list:
        print(str(rank)+') '+name[0]+" has an ELO of "+(str(name[1]))+ ", and has a record of "+str(logs[name[0]][0])+" wins, "+
              str(logs[name[0]][1])+" ties, and "+str(logs[name[0]][2])+" losses.")
        rank += 1



def update_logs(logs, list):
    log_file = open("logs.txt", "w")
    list_file = open("list.txt", "w")
    log_file.write(str(logs))
    list_file.write(str(list))
    log_file.close()
    list_file.close()


def clearLogs(logs, list):
    log_file = open('logs.txt', 'r+')
    list_file = open('list.txt', 'r+')
    log_file.close()
    list_file.close()
    logs.clear()
    list.clear()



main()