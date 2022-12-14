# Tudor Avarvarei tic-tac-toe game using reinforcement learning
import pickle

import numpy as np
# from matplotlib import pyplot as plt

board = np.array([[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]])

NUMBER_ROWS = 3
NUMBER_COLS = 3


class Game:
    def __init__(self, main_player, helper_player):
        self.main_player = main_player
        self.helper_player = helper_player
        self.board = board.copy()

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
            for m in range(NUMBER_COLS):
                if self.board[i][m] == " ":
                    array_positions.append((i, m))
        return array_positions

    def give_reward(self):
        result = self.check_end()
        if result == 1:
            self.main_player.feed_reward(1)
        elif result == -1:
            self.helper_player.feed_reward(1)
        else:
            self.main_player.feed_reward(0.1)
            self.helper_player.feed_reward(0.5)

    def train(self, games):
        for i in range(games):
            if i % 1000 == 0:
                print("Rounds:", i)
            while self.check_end() is None:
                main_player_action = self.main_player.action(self.check_positions_available(), self.board, "X")
                self.board[main_player_action] = "X"
                self.main_player.turns.append(str(self.board.reshape(NUMBER_COLS * NUMBER_ROWS)))
                if self.check_end() is not None:
                    self.give_reward()
                    self.board = board.copy()
                    self.helper_player.turns = []
                    self.main_player.turns = []
                    break
                else:
                    helper_player_action = self.helper_player.action(self.check_positions_available(), self.board, "O")
                    self.board[helper_player_action] = "O"
                    self.helper_player.turns.append(str(self.board.reshape(NUMBER_COLS * NUMBER_ROWS)))
                    if self.check_end() is not None:
                        self.give_reward()
                        self.board = board.copy()
                        self.helper_player.turns = []
                        self.main_player.turns = []
                        break

    def play(self):
        while self.check_end() is None:
            computer_action = self.main_player.action(self.check_positions_available(), self.board, "X")
            self.board[computer_action] = "X"
            # self.draw_board()
            if self.check_end() is not None:
                if self.check_end() == 1:
                    # print(self.main_player.name, "wins!")
                    return 1
                else:
                    # print("It's a tie!")
                    return 0
            else:
                human_action = self.helper_player.action(self.check_positions_available(), self.board, "O")
                self.board[human_action] = "O"
                if self.check_end() is not None:
                    if self.check_end() == -1:
                        # self.draw_board()
                        # print(self.helper_player.name, "wins!")
                        return -1
                    else:
                        # self.draw_board()
                        # print("It's a tie!")
                        return 0


class Human:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def action(available_positions):
        while True:
            row = int(input("Input action row (0, 1, 2):"))
            column = int(input("Input action column (0, 1, 2):"))
            output = (row, column)
            if output in available_positions:
                return output
            else:
                print("Not a valid position")


class Computer:
    def __init__(self, name, random_rate=0.3, learning_rate=0.2, decay=0.9):
        self.name = name
        self.random_rate = random_rate
        self.learning_rate = learning_rate
        self.decay = decay
        self.states_value = {}
        self.turns = []

    def action(self, available_positions, board_current, sign):
        if np.random.uniform(0, 1) < self.random_rate:
            output = available_positions[np.random.choice(len(available_positions))]
        else:
            value_max = -1000
            for i in available_positions:
                next_board = board_current.copy()
                next_board[i] = sign
                next_board_1d = str(next_board.reshape(NUMBER_COLS*NUMBER_ROWS))
                value = 0 if self.states_value.get(next_board_1d) is None else self.states_value.get(next_board_1d)
                if value > value_max:
                    value_max = value
                    output = i
        return output

    def feed_reward(self, reward):
        for turn in reversed(self.turns):
            if self.states_value.get(turn) is None:
                self.states_value[turn] = 0
            self.states_value[turn] += (reward * self.decay - self.states_value[turn]) * self.learning_rate
            reward = self.states_value[turn]

    def save_policy(self, filename):
        file = open(filename, "wb")
        pickle.dump(self.states_value, file)
        file.close()

    def load_policy(self, filename):
        file = open(filename, "rb")
        self.states_value = pickle.load(file)
        # print(self.states_value)
        file.close()


if __name__ == '__main__':
    # rounds = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]
    rounds = 5000
    # random_rate = np.arange(0, 1, 0.1)
    # learning_rate = np.arange(0.1, 1.1, 0.1)
    # learning_rate = [1.1]
    # decay = np.arange(0.1, 2, 1.8)
    # wins_number = [76, 56, 79, 79, 86, 89, 91, 79, 81, 94, 97, 87, 89]
    all_wins1 = []
    all_wins2 = []
    for k in range(10):
        wins_number1 = []
        wins_number2 = []
        player1 = Computer("Player1")
        player2 = Computer("Player2")
        game = Game(player1, player2)
        game.train(games=rounds)
        player1.save_policy("policy1_reward{}".format(k))

        results1 = []
        for j in range(100):
            computer1 = Computer("Computer", random_rate=0)
            computer1.load_policy("policy1_reward{}".format(k))
            random = Computer("Random", random_rate=1)
            random.load_policy("policy1_reward{}".format(k))
            game1 = Game(computer1, random)
            result1 = game1.play()
            results1.append(result1)

        wins_number1.append(results1.count(1))
        wins_number2.append(results1.count(0))

        all_wins1.append(wins_number1)
        all_wins2.append(wins_number2)

    print(all_wins1)
    print(all_wins2)
    print("Won games:", np.average(all_wins1))
    print("Draw games:", np.average(all_wins2))

    # print(all_wins1)
    # show_average1 = []
    # # show_average2 = []
    # for i in range(len(random_rate)):
    #     show_average1.append(np.average([sub[i] for sub in all_wins1]))
    # show_average2.append(np.average([sub[i] for sub in all_wins2]))
    # plt.plot(decay, show_average1, label="Player 1")
    # # plt.plot(random_rate, show_average2, label="Player 2")
    # # plt.xscale("log")
    # plt.title("Number of wins and draws for multiple runs")
    # plt.xlabel("Decay "r"$\gamma$")
    # plt.ylabel("Number of wins and draws")
    # # plt.legend()
    # plt.show()
    #
    # plt.plot(decay, wins_number1, label="Player 1")
    # # plt.plot(random_rate, wins_number2, label="Player 2")
    # # plt.xscale("log")
    # plt.title("Number of wins and draws for one run")
    # plt.xlabel("Decay "r"$\gamma$")
    # plt.ylabel("Number of wins and draws")
    # # plt.legend()
    # plt.show()
