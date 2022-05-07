import random
import copy

BOMB_NUMBER = 50
BOARD_LENGTH = 20
shown_board = []
for board_row in range(0, BOARD_LENGTH):
    if board_row > len(shown_board) - 1:
        shown_board.append([])
    for column in range(0, BOARD_LENGTH + 1):
        shown_board[board_row].append("X ")
    shown_board[board_row][-1] = "\n"


def range_finder(coord):
    if coord == 0:
        return range(coord, coord+2)
    elif coord == BOARD_LENGTH - 1:
        return range(coord-1, coord+1)
    return range(coord-1, coord+2)


class Game:
    def __init__(self):
        self.hidden_board = copy.deepcopy(shown_board)
        self.game_is_on: True
        for i in range(0, BOMB_NUMBER):
            self.plant_bomb()
        self.set_numbers()
        self.propagation_list = []
        self.mark_count = 0

    def plant_bomb(self):
        x = random.randint(0, BOARD_LENGTH - 1)
        y = random.randint(0, BOARD_LENGTH - 1)
        if self.hidden_board[x][y] == "B ":
            self.plant_bomb()
        self.hidden_board[x][y] = "B "

    def set_numbers(self):
        for r in range(0, BOARD_LENGTH):
            for c in range(0, BOARD_LENGTH):
                if self.hidden_board[r][c] != "B ":
                    bomb_count = 0
                    for bomb_r in range_finder(r):
                        for bomb_c in range_finder(c):
                            if self.hidden_board[bomb_r][bomb_c] == "B ":
                                bomb_count += 1
                    if bomb_count != 0:
                        self.hidden_board[r][c] = f"{bomb_count} "
                    else:
                        self.hidden_board[r][c] = ". "

    def player_reveal_move(self, player_input):
        self.reveal(player_input[0], player_input[1])
        while len(self.propagation_list) > 0:
            for item in self.propagation_list:
                self.reveal(item[0], item[1])
                self.propagation_list.remove(item)
        if self.hidden_board[player_input[0]][player_input[1]] == "B ":
            return False
        return True
    
    def reveal(self, x, y):
        shown_board[x][y] = self.hidden_board[x][y]
        if self.hidden_board[x][y] == ". ":
            for row in range_finder(x):
                for colum in range_finder(y):
                    if shown_board[row][colum] != self.hidden_board[row][colum] \
                                        and self.hidden_board[row][colum] == ". ":
                        self.propagation_list.append([row, colum])
                    shown_board[row][colum] = self.hidden_board[row][colum]

    def mark_bomb(self, player_input):
        shown_board[player_input[0]][player_input[1]] = "! "
        self.mark_count += 1
        if self.mark_count == BOMB_NUMBER:
            for r in range(0, BOARD_LENGTH):
                for c in range(0, BOARD_LENGTH):
                    if shown_board[r][c] == "! " and self.hidden_board[r][c] != "B ":
                        return True

    def unmark(self, player_input):
        shown_board[player_input[0]][player_input[1]] = ". "
