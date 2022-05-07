from game import Game, shown_board


def print_board(board):
    # Turns the list of the board into a string to print it.
    board_string = ""
    for r in board:
        for c in r:
            board_string += c
    print(board_string)


def take_coordinates():
    # Takes input from the player, formats it, returns a list as an output.
    player_input = input("Please enter the coordinates as 'x, y': ")
    input_list = player_input.split(",")
    for i in range(0, 2):
        input_list[i] = int(input_list[i].strip())
    return input_list


my_game = Game()
game_is_on = True
while game_is_on:
    # The main game loop.
    print_board(shown_board)
    player_choice = input("Type 'reveal' to reveal a block, 'mark' to mark a block as bombed, 'unmark' to erase a mark")
    if player_choice == "reveal":
        game_is_on = my_game.player_reveal_move(take_coordinates())
    elif player_choice == "mark":
        game_is_on = my_game.mark_bomb(take_coordinates())
        if not game_is_on:
            print("Congratulations! You have won!")
    elif player_choice == "unmark":
        my_game.unmark(take_coordinates())
    else:
        print("Entered unknown command.")
# The final print of the board.
print_board(my_game.hidden_board)
