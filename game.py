import random
import copy

# The main game constants. Modify these to change the game.
BOMB_NUMBER = 50
BOARD_LENGTH = 20

# The code below creates the board list. Covered block is "X ". Bomb is "B ". Empty block is ". ".
# "! " is a marked block meaning the player thinks there is a bomb at that location. Blocks with numbers
# show how many bombs are around.
shown_board = []
for board_row in range(0, BOARD_LENGTH):
    if board_row > len(shown_board) - 1:
        shown_board.append([])
    for column in range(0, BOARD_LENGTH + 1):
        shown_board[board_row].append("X ")
    shown_board[board_row][-1] = "\n"


def range_finder(coord):
    # A range finder function was needed because looking at adjacent blocks returns index error when near
    # edges of the board.
    if coord == 0:
        return range(coord, coord+2)
    elif coord == BOARD_LENGTH - 1:
        return range(coord-1, coord+1)
    return range(coord-1, coord+2)


class Game:
    def __init__(self):
        # Hidden board is the real list of board where we hold the information. The player aims to reveal the hidden
        # board without revealing any bombs.
        self.hidden_board = copy.deepcopy(shown_board)
        self.game_is_on: True
        for i in range(0, BOMB_NUMBER):
            self.plant_bomb()
        self.set_numbers()
        self.propagation_list = []
        self.mark_count = 0

    def plant_bomb(self):
        # Plants bombs at random at the initialization of the game.
        x = random.randint(0, BOARD_LENGTH - 1)
        y = random.randint(0, BOARD_LENGTH - 1)
        if self.hidden_board[x][y] == "B ":
            self.plant_bomb()
        self.hidden_board[x][y] = "B "

    def set_numbers(self):
        # After the bombs planted this function runs to look at adjacent blocks to determine what number to put.
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
        # When player chooses to reveal a block this function runs. Empty blocks propagate to adjacent empty blocks
        # to chain reveal. When a bomb is revealed the game ends(return False).
        self.reveal(player_input[0], player_input[1])
        while len(self.propagation_list) > 0:
            for item in self.propagation_list:
                self.reveal(item[0], item[1])
                self.propagation_list.remove(item)
        if self.hidden_board[player_input[0]][player_input[1]] == "B ":
            return False
        return True
    
    def reveal(self, x, y):
        # This does the actual revealing and propagation list appending. player_reveal_move uses this function
        shown_board[x][y] = self.hidden_board[x][y]
        if self.hidden_board[x][y] == ". ":
            for row in range_finder(x):
                for colum in range_finder(y):
                    if shown_board[row][colum] != self.hidden_board[row][colum] \
                                        and self.hidden_board[row][colum] == ". ":
                        self.propagation_list.append([row, colum])
                    shown_board[row][colum] = self.hidden_board[row][colum]

    def mark_bomb(self, player_input):
        # The function to mark blocks. If the number of marks is the same as number of bombs this function
        # checks for win condition. If every block with mark has a bomb underneath and no other type of block
        # has any mark then the player has won.
        shown_board[player_input[0]][player_input[1]] = "! "
        self.mark_count += 1
        if self.mark_count == BOMB_NUMBER:
            for r in range(0, BOARD_LENGTH):
                for c in range(0, BOARD_LENGTH):
                    if shown_board[r][c] == "! " and self.hidden_board[r][c] != "B ":
                        return True

    def unmark(self, player_input):
        shown_board[player_input[0]][player_input[1]] = "X "
