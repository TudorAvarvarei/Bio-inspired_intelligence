# Tudor Avarvarei tic-tac-toe game using reinforcement learning


board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]

NUMBER_ROWS = 3
NUMBER_COLS = 3

class Game:
    def __init__(self):
        self.board = board

    def draw_board(self):
        print("_____________")
        print("| %c | %c | %c |" % (self.board[0][0], self.board[0][1], self.board[0][2]))
        print("_____________")
        print("| %c | %c | %c |" % (self.board[1][0], self.board[1][1], self.board[1][2]))
        print("_____________")
        print("| %c | %c | %c |" % (self.board[2][0], self.board[2][1], self.board[2][2]))
        print("_____________")


    def check_end(self):
        for i in range(NUMBER_ROWS):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] == "X":
                return 1
            elif self.board[i][0] == self.board[i][1] == self.board[i][2] == "O":
                return -1

        for i in range(NUMBER_COLS):
            if self.board[0][i] == self.board[1][i] == self.board[2][i] == "X":
                return 1
            elif self.board[0][i] == self.board[1][i] == self.board[2][i] == "O":
                return -1

        if self.board[0][0] == self.board[1][1] == self.board[2][2] == "X":
            return 1

        if self.board[0][0] == self.board[1][1] == self.board[2][2] == "O":
            return -1

        if self.board[0][2] == self.board[1][1] == self.board[2][0] == "X":
            return 1

        if self.board[0][2] == self.board[1][1] == self.board[2][0] == "O":
            return -1

        if len(self.check_positions_available()) == 0:
            return 0

        return None


    def check_positions_available(self):
        array_positions = []
        for i in range(NUMBER_ROWS):
            for j in range(NUMBER_COLS):
                if self.board[i][j] == " ":
                    array_positions.append((i, j))
        return array_positions

    def give_reward(self):
        result = self.check_end()


class Human:
    def __init__(self, name):
        self.board = board
        self.name = name


    def action(self, available_positions):
        while True:
            row = int(input("Input action row (0, 1, 2):"))
            column = int(input("Input action column (0, 1, 2):"))
            action = (row, column)
            if action in available_positions:
                return action
            else:
                print("Not a valid position")


class Computer:
    def __init__(self):
        self.board = board

        


def main():
    result = Game.check_end()

    if result == None:
        print("Game not finished")
    elif result == 0:
        print("DRAW")
    elif result == 1:
        print("Player 1 wins")
    else:
        print("Player 2 wins")


if __name__ == '__main__':
    Game.draw_board()
    main()
