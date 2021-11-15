# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python

import time
import gameTraceOpt

class Game:
    MINIMAX = 0
    ALPHABETA = 1
    HUMAN = 2
    AI = 3

    # n = board size [3...10]
    # s = winning line up size [3...n]
    # b = block size [0...2n]
    # b_coord = block coordinates
    def __init__(self, recommend=True, n=3, s=3, b=0, b_coord=None, d1=None, d2=None, t=None, f=None):
        # Initialize the parameters
        self.n = n
        self.s = s
        self.b = b

        if d1 is None:
            d1 = 3
        if d2 is None:
            d2 = 3
        self.d1 = d1
        self.d2 = d2

        if t is None:
            t = 1.0
        self.t = t
        self.timer_s = time.time()

        if b_coord is None:
            b_coord = []
        self.b_coord = b_coord

        self.f = f

        self.initialize_game()
        self.recommend = recommend

    def initialize_game(self):
        # generate 2-d list board based on n
        self.current_state = []
        for i in range(self.n):
            temp_list = []
            for j in range(self.n):
                temp_list.append('.')
            self.current_state.append(temp_list)

        # mark the block with *
        for i in range(self.b):
            self.current_state[self.b_coord[i][0]][self.b_coord[i][1]] = '*'
        # Player X always plays first
        self.player_turn = 'X'

    def draw_board(self, move_no=""):
        """Responsible for displaying board and return a board string"""
        """
            Parameters
            ----------
                boardGraph : string 
                    containing board graph
        """
        # draw table head - 1
        boardGraph = "\n  "
        for i in range(0, self.n):
            boardGraph += chr(i + 65)
        # draw table head - 2
        boardGraph += "\n +"
        for i in range(0, self.n):
            boardGraph += "-"
        boardGraph += "\n"

        # # print board content
        for x in range(0, self.n):
            boardGraph += "{}|".format(x)
            # print dynamic board content
            for y in range(0, self.n):
                boardGraph += "{}".format(self.current_state[x][y])
            boardGraph += "\n"
        print(boardGraph)
        return boardGraph

    # get the possible winning diagonals as a 2d-list for the current game
    def get_diagonal(self, orientation):
        diff_size_win = self.n - self.s
        if orientation == "slash":
            return [[self.current_state[y - x][x] for x in range(self.n) if 0 <= y - x < self.n] for y in
                    range(2 * self.n - 1) if self.n - 1 + diff_size_win >= y >= self.n - 1 - diff_size_win]
        elif orientation == "backslash":
            return [[self.current_state[y - x][self.n - 1 - x] for x in range(self.n) if 0 <= y - x < self.n] for y in
                    range(2 * self.n - 1) if self.n - 1 + diff_size_win >= y >= self.n - 1 - diff_size_win]

    def is_valid(self, px, py):
        if px < 0 or px > self.n - 1 or py < 0 or py > self.n - 1:
            return False
        elif self.current_state[px][py] != '.':
            return False
        else:
            return True

    # change evaluation with loop
    def is_end(self):
        # Vertical win
        for i in range(0, self.n):
            # extract the vertical line
            vertical = ""
            for j in range(0, self.n):
                vertical += self.current_state[j][i]
            # check for a winner
            if vertical.find('X' * self.s) != -1:
                return 'X'
            elif vertical.find('O' * self.s) != -1:
                return 'O'

        # Horizontal win
        for i in range(0, self.n):
            horizontal = ""
            for j in range(0, self.n):
                horizontal += self.current_state[i][j]
            # check for winner
            if horizontal.find('X' * self.s) != -1:
                return 'X'
            elif horizontal.find('O' * self.s) != -1:
                return 'O'

        # diagonal win
        # first check the slash diagonal for possible winnings
        slash_diag = self.get_diagonal("slash")
        # loop over the list and check
        for i in range(len(slash_diag)):
            line = ""
            for j in range(len(slash_diag[i])):
                line += slash_diag[i][j]
            # check for winner
            if line.find('X' * self.s) != -1:
                return 'X'
            elif line.find('O' * self.s) != -1:
                return 'O'

        # then check the backslash diagonal for possible winnings
        backslash_diag = self.get_diagonal("backslash")
        for i in range(len(backslash_diag)):
            line = ""
            for j in range(len(backslash_diag[i])):
                line += backslash_diag[i][j]
            # check for winner
            if line.find('X' * self.s) != -1:
                return 'X'
            elif line.find('O' * self.s) != -1:
                return 'O'

        # Is whole board full?
        for i in range(0, self.n):
            for j in range(0, self.n):
                # There's an empty field and nobody wins, we continue the game
                if (self.current_state[i][j] == '.'):
                    return None
        # It's a tie!
        return '.'

    def check_end(self):
        self.result = self.is_end()
        # Printing the appropriate message if the game has ended
        if self.result != None:
            if self.result == 'X':
                print('The winner is X!')
            elif self.result == 'O':
                print('The winner is O!')
            elif self.result == '.':
                print("It's a tie!")
            self.initialize_game()
        return self.result

    def input_move(self):
        while True:
            print(F'Player {self.player_turn}, enter your move:')
            px = int(input('enter the x coordinate: '))
            py = int(input('enter the y coordinate: '))
            if self.is_valid(px, py):
                return (px, py)
            else:
                print('The move is not valid! Try again.')

    def switch_player(self):
        if self.player_turn == 'X':
            self.player_turn = 'O'
        elif self.player_turn == 'O':
            self.player_turn = 'X'
        return self.player_turn

    # simple heuristic
    def h1(self):
        # X is for min; O is for max
        score = 0
        # score is dependent of the number of X's or O's in rows, columns, and diagonals.
        # the value added into or subtracted from the score is 2 powered to the number of X's or O's
        # the number of blocks can possibly adjust the score TO DO and TO TEST
        # row evaluation
        for x in range(0, self.n):
            score += (pow(2, self.current_state[x].count('O')) - 1)
            score -= (pow(2, self.current_state[x].count('X')) - 1)

        # if n != s, we do have four diagonals other than the two main diagonal. Otherwise, we only need to consider
        # slash "/"
        list_all_diagonals_1 = self.get_diagonal("slash")
        # backslash "\"
        list_all_diagonals_2 = self.get_diagonal("backslash")
        # Iterate all possible diagonals to calculate the score
        for x in list_all_diagonals_1:
            score += (pow(2, x.count('O')) - 1)
            score -= (pow(2, x.count('X')) - 1)

        for x in list_all_diagonals_2:
            score += (pow(2, x.count('O')) - 1)
            score -= (pow(2, x.count('X')) - 1)

        # column evaluation
        for x in range(0, self.n):
            score += (pow(2, [i[x] for i in self.current_state].count('O')) - 1)
            score -= (pow(2, [i[x] for i in self.current_state].count('X')) - 1)
        # print("h1 score = ", score)

        result = self.is_end()
        if result == 'X':
            score = float('-inf')
        elif result == 'O':
            score = float('inf')
        elif result == '.':
            score = 0

        return score

    # -------------------------------------N-ply look ahead with heuristic(Minimax +
    # alphabet)---------------------------------------
    def minimax_informed(self, depth, max=False):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:
        x = None
        y = None

        elapsed_time = time.time() - self.timer_s

        # time up, return the current selection
        if depth == 0 or (self.t - elapsed_time) <= 0.0:
            if (self.t - elapsed_time) <= 0.0:
                print("out of time")
            return self.h1(), x, y

        # choose the max value on the max side while choose the min value on the min side
        value = float('inf')
        if max:
            value = float('-inf')

        for i in range(0, self.n):
            for j in range(0, self.n):
                if self.current_state[i][j] == '.':
                    if max:
                        self.current_state[i][j] = 'O'
                        (v, _, _) = self.minimax_informed(depth - 1, max=False)
                        if v >= value:
                            value = v
                            x = i
                            y = j
                    else:

                        self.current_state[i][j] = 'X'
                        (v, _, _) = self.minimax_informed(depth - 1, max=True)
                        if v <= value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'
        return value, x, y


    def alphabeta_informed(self, depth, alpha=float('-inf'), beta=float('inf'), max=False):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:
        x = None
        y = None

        elapsed_time = time.time() - self.timer_s

        if depth == 0 or (self.t - elapsed_time) <= 0:
            return self.h1(), x, y

        value = float('inf')
        if max:
            value = float('-inf')

        for i in range(0, self.n):
            for j in range(0, self.n):
                if self.current_state[i][j] == '.':
                    if max:
                        self.current_state[i][j] = 'O'
                        (v, _, _) = self.alphabeta_informed(depth - 1, alpha, beta, max=False)
                        if v >= value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        (v, _, _) = self.alphabeta_informed(depth - 1, alpha, beta, max=True)
                        if v <= value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'
                    if max:
                        if value >= beta:
                            return value, x, y
                        if value > alpha:
                            alpha = value
                    else:
                        if value <= alpha:
                            return value, x, y
                        if value < beta:
                            beta = value
        return value, x, y

    def play(self, algo1=None, algo2=None, player_x=None, player_o=None):
        if algo1 == None:
            algo1 = self.ALPHABETA
        if algo2 == None:
            algo2 = self.ALPHABETA
        if player_x == None:
            player_x = self.HUMAN
        if player_o == None:
            player_o = self.HUMAN
        while True:

            self.draw_board()
            if self.check_end():
                return
            start = time.time()
            self.timer_s = time.time()
            # run algo
            if self.player_turn == 'X':
                if algo1 == Game.MINIMAX:
                    (_, x, y) = self.minimax_informed(max=False, depth=self.d1)
                elif algo1 == Game.ALPHABETA:
                    (_, x, y) = self.alphabeta_informed(max=False, depth=self.d1)

            elif self.player_turn == 'O':
                if algo2 == Game.MINIMAX:
                    (_, x, y) = self.minimax_informed(max=True, depth=self.d2)
                elif algo2 == Game.ALPHABETA:
                    (_, x, y) = self.alphabeta_informed(max=True, depth=self.d2)


            end = time.time()

            if (self.player_turn == 'X' and player_x == self.HUMAN) or (
                    self.player_turn == 'O' and player_o == self.HUMAN):
                if self.recommend:
                    print(F'Evaluation time: {round(end - start, 7)}s')
                    print(F'Recommended move: x = {x}, y = {y}')
                (x, y) = self.input_move()
            if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
                print(F'Evaluation time: {round(end - start, 7)}s')
                print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
            self.current_state[x][y] = self.player_turn
            self.switch_player()


def user_input_board_config():
    # input for board size
    while True:
        n = int(input("Please enter the board size (3-10): "))
        if n < 3 or n > 10:
            print("Please re-enter, the board size can only be 3 minimum or 10 maximum: ")
        else:
            break

    # input for winning line-up size
    while True:
        s = int(input(F"Please enter the winning line-up size (3-{n}): "))
        if s < 3 or s > n:
            print(F"Please re-enter, the winning line-up can only be 3 minimum or {n} maximum: ")
        else:
            break

    # input for block number
    while True:
        b = int(input(F"Please enter the block number (0-{2 * n}): "))
        if b < 0 or b > 2 * n:
            print(F"Please re-enter, the block number can only be 0 minimum or {2 * n} maximum: ")
        else:
            break

    b_coord = []
    for i in range(b):
        has_duplicate = True
        x = 0
        y = 0
        while has_duplicate:
            has_duplicate = False
            # input x coord
            while True:
                x = int(input(F"Please enter the {i + 1}/{b} x-coordinate for the block (0 - {n - 1}): "))
                if x < 0 or x >= n:
                    print(F"Please re-enter, the x-coordinate for the block can only be 0 minimum or {n - 1} maximum: ")
                else:
                    break

            # input y coord
            while True:
                _y = input(F"Please enter the {i + 1}/{b} y-coordinate for the block (A - {chr(n - 1 + 65)}): ")
                y = ord(_y) - 65
                if y < 0 or y >= n:
                    print(
                        F"Please re-enter, the y-coordinate for the block can only be A minimum or {chr(n - 1 + 65)} maximum")
                else:
                    break

            # find duplicates
            for j in range(len(b_coord)):
                if x == b_coord[j][0] and y == b_coord[j][1]:
                    print("The coordinate you entered already exist, please re-enter!")
                    has_duplicate = True
                    break

        # append the x and y to b_coord
        b_coord.append([x, y])


    # play mode
    player1 = input("Please enter player1 mode (AI or HUMAN): ")
    player1 = Game.AI if player1 == "AI" else Game.HUMAN

    player2 = input("Please enter player2 mode (AI or HUMAN): ")
    player2 = Game.AI if player2 == "AI" else Game.HUMAN

    # d1 and d2
    d1 = None
    d2 = None
    algo1 = None
    algo2 = None
    if player1 == Game.AI:
        algo1 = input("Please enter the algorithm for AI-1 (MINIMAX or ALPHA-BETA): ")
        algo1 = Game.MINIMAX if algo1 == "MINIMAX" else Game.ALPHABETA
        d1 = int(input("Please enter AI-1 max depth: "))

    if player2 == Game.AI:
        algo2 = input("Please enter the algorithm for AI-2 (MINIMAX or ALPHA-BETA): ")
        algo2 = Game.MINIMAX if algo2 == "MINIMAX" else Game.ALPHABETA
        d2 = int(input("Please enter AI-2 max depth: "))

    # max time allowed and game mode
    if player1 == Game.AI or player2 == Game.AI:
        t = float(input("Please enter max time allowed for AI"))



    return n, s, b, b_coord, player1, player2, d1, d2, algo1, algo2, t


def main():
    # automatic
    _n = 5
    _s = 4
    _b = 2
    _b_coord = [[0,2], [1,1]]
    _d1 = 5
    _d2 = 5
    _t = 10
    _algo1 = Game.MINIMAX
    _algo2 = Game.ALPHABETA
    _player1 = Game.AI
    _player2 = Game.AI
    # user input
    # _n, _s, _b, _b_coord, _player1, _player2, _d1, _d2, _algo1, _algo2, _t = user_input_board_config()

    # start writing
    fileFormat = "gameTrace-{}{}{}{}.txt".format(_n, _b, _s, _t)
    fWriter = open(fileFormat, "w")

    # 1. The parameters of the game: the values of n, b, s, t
    fWriter.write("Game parameters: [Size n = {}, Blocs b = {}, winSize s = {}, Overtime t = {}]\n".format(_n, _b, _s, _t))
    # 2. The position of the blocs
    fWriter.write("Position of each blocs: {}\n\r".format(_b_coord))
    # 3. player info
    fWriter.write("Player 1: {}, d={}, a={}, {}\n".format(_player1, _d1, _algo1, "nmb"))
    fWriter.write("Player 2: {}, d={}, a={}, {}\n\r".format(_player2, _d2, _algo2, "cnm"))


    g = Game(n=_n, s=_s, b=_b, b_coord=_b_coord, d1=_d1, d2=_d2, t=_t, f=fWriter)
    # 4. initial config of board
    fWriter.write("4. Initial configuration of the board.{}\n".format(g.draw_board()))

    g.play(algo1=_algo1, algo2=_algo2, player_x=_player1, player_o=_player2)


    fWriter.close()
if __name__ == "__main__":
    main()
