# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python

import time
import gameTraceOpt
import Heuristics


class Game:
    MINIMAX = 0
    ALPHABETA = 1
    HUMAN = 2
    AI = 3
    list_of_winner = []

    # n = board size [3...10]
    # s = winning line up size [3...n]
    # b = block size [0...2n]
    # b_coord = block coordinates
    def __init__(self, recommend=True, n=3, s=3, b=0, b_coord=None, d1=None, d2=None, t=None, f=None, h_swap=None):
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

        if h_swap is None:
            h_swap = False
        self.h_swap = h_swap

        self.f = f

        # for end game trace
        self.avg_depth = []
        self.avg_rec_depth = []

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

    def draw_board(self):
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

    # -------------------------------------N-ply look ahead with heuristic(Minimax +
    # alphabet)---------------------------------------
    def minimax_informed(self, depth, current_depth, max=False):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:
        x = None
        y = None
        elapsed_time = time.time() - self.timer_s

        result = self.is_end()
        if result == 'X':
            return float('-inf'), x, y, current_depth
        elif result == 'O':
            return float('inf'), x, y, current_depth
        elif result == '.':
            return 0, x, y, current_depth

        # time up, return the current selection
        if depth == 0 or (self.t - elapsed_time) <= 0.0:
            self.eval_count += 1
            self.depth_of_nodes.append(current_depth)
            self.avg_depth_of_nodes.append(current_depth)
            if not self.h_swap:
                return Heuristics.h1(self) if self.player_turn == 'X' else Heuristics.h2(self), x, y, current_depth
            else:
                return Heuristics.h2(self) if self.player_turn == 'X' else Heuristics.h1(self), x, y, current_depth

        # choose the max value on the max side while choose the min value on the min side
        value = float('inf')
        if max:
            value = float('-inf')

        num_children = 0
        sum_children_depth = 0

        for i in range(0, self.n):
            for j in range(0, self.n):
                if self.current_state[i][j] == '.':
                    if max:
                        self.current_state[i][j] = 'O'
                        (v, _, _, d) = self.minimax_informed(depth - 1, current_depth + 1, max=False)
                        if v >= value:
                            value = v
                            x = i
                            y = j
                        num_children += 1
                        sum_children_depth += d
                    else:

                        self.current_state[i][j] = 'X'
                        (v, _, _, d) = self.minimax_informed(depth - 1, current_depth + 1, max=True)
                        if v <= value:
                            value = v
                            x = i
                            y = j
                        num_children += 1
                        sum_children_depth += d

                    self.current_state[i][j] = '.'
        return value, x, y, float(sum_children_depth) / (1 if num_children == 0 else num_children)

    def alphabeta_informed(self, depth, current_depth, alpha=float('-inf'), beta=float('inf'), max=False):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:
        x = None
        y = None

        elapsed_time = time.time() - self.timer_s

        result = self.is_end()
        if result == 'X':
            return float('-inf'), x, y, current_depth
        elif result == 'O':
            return float('inf'), x, y, current_depth
        elif result == '.':
            return 0, x, y, current_depth

        if depth == 0 or (self.t - elapsed_time) <= 0:
            self.eval_count += 1
            self.depth_of_nodes.append(current_depth)
            # Fixme avg_depth_of_nodes is completely same as depth_of_nodes isn't it?
            self.avg_depth_of_nodes.append(current_depth)
            if not self.h_swap:
                return Heuristics.h1(self) if self.player_turn == 'X' else Heuristics.h2(self), x, y, current_depth
            else:
                return Heuristics.h2(self) if self.player_turn == 'X' else Heuristics.h1(self), x, y, current_depth

        value = float('inf')
        if max:
            value = float('-inf')

        num_children = 0
        sum_children_depth = 0

        for i in range(0, self.n):
            for j in range(0, self.n):
                if self.current_state[i][j] == '.':
                    if max:
                        self.current_state[i][j] = 'O'
                        (v, _, _, d) = self.alphabeta_informed(depth - 1, current_depth + 1, alpha, beta, max=False)
                        if v >= value:
                            value = v
                            x = i
                            y = j
                        num_children += 1
                        sum_children_depth += d
                    else:
                        self.current_state[i][j] = 'X'
                        (v, _, _, d) = self.alphabeta_informed(depth - 1, current_depth + 1, alpha, beta, max=True)
                        if v <= value:
                            value = v
                            x = i
                            y = j
                        num_children += 1
                        sum_children_depth += d

                    self.current_state[i][j] = '.'
                    if max:
                        if value >= beta:
                            return value, x, y, float(sum_children_depth) / (1 if num_children == 0 else num_children)
                        if value > alpha:
                            alpha = value
                    else:
                        if value <= alpha:
                            return value, x, y, float(sum_children_depth) / (1 if num_children == 0 else num_children)
                        if value < beta:
                            beta = value

        return value, x, y, float(sum_children_depth) / (1 if num_children == 0 else num_children)

    def play(self, algo1=None, algo2=None, player_x=None, player_o=None):
        if algo1 == None:
            algo1 = self.ALPHABETA
        if algo2 == None:
            algo2 = self.ALPHABETA
        if player_x == None:
            player_x = self.HUMAN
        if player_o == None:
            player_o = self.HUMAN

        self.move_count = 0
        self.total_eval_time = 0
        self.total_eval_count = 0
        self.avg_depth_of_nodes = []
        self.avg_ard_list = []
        # Num of heuristic evaluations
        self.eval_count = 0
        # depth of nodes
        self.depth_of_nodes = []


        while True:
            isGameEnd = self.check_end()
            if isGameEnd:
                # end game trace
                if isGameEnd == "X":
                    if algo1 == Game.MINIMAX:
                        self.list_of_winner.append("h1") if not self.h_swap else self.list_of_winner.append("h2")
                    else:
                        self.list_of_winner.append("h2") if not self.h_swap else self.list_of_winner.append("h1")
                if isGameEnd == "O":
                    if algo2 == Game.ALPHABETA:
                        self.list_of_winner.append("h2") if not self.h_swap else self.list_of_winner.append("h1")
                    else:
                        self.list_of_winner.append("h1") if not self.h_swap else self.list_of_winner.append("h2")
                # Todo: need to create a bunch of variable to collect sh*t for the avg_avg_avg_stuff
                gameTraceOpt.endGameTrace(self.f, isGameEnd, self.total_eval_time, self.total_eval_count,
                                          self.avg_depth_of_nodes, self.avg_ard_list, self.move_count)
                return
            # meta data initialization
            start = time.time()
            self.timer_s = time.time()

            # run algo
            if self.player_turn == 'X':
                if algo1 == Game.MINIMAX:
                    (_, x, y, ard) = self.minimax_informed(max=False, depth=self.d1, current_depth=0)
                elif algo1 == Game.ALPHABETA:
                    (_, x, y, ard) = self.alphabeta_informed(max=False, depth=self.d1, current_depth=0)

            elif self.player_turn == 'O':
                if algo2 == Game.MINIMAX:
                    (_, x, y, ard) = self.minimax_informed(max=True, depth=self.d2, current_depth=0)
                elif algo2 == Game.ALPHABETA:
                    (_, x, y, ard) = self.alphabeta_informed(max=True, depth=self.d2, current_depth=0)

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
            # update global meta
            self.move_count += 1
            self.total_eval_time += end - start
            self.total_eval_count += self.eval_count
            self.avg_ard_list.append(ard)
            gameTraceOpt.inGameTrace(self.f, self.player_turn, [x, chr(y + 65)], self.draw_board(), end - start,
                                     self.eval_count, self.depth_of_nodes, ard, self.move_count)

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
    # user input
    # _n, _s, _b, _b_coord, _player1, _player2, _d1, _d2, _algo1, _algo2, _t = user_input_board_config()

    # automatic
    _n = 5
    _s = 3
    _b = 0
    _b_coord = []
    _d1 = 3
    _d2 = 3
    _t = 100
    _r = 2
    _algo1 = Game.MINIMAX
    _algo2 = Game.ALPHABETA
    _player1 = Game.AI
    _player2 = Game.AI
    _h_swap = False

    """single run"""
    # start writing
    fileFormat = "gameTrace-{}{}{}{}.txt".format(_n, _b, _s, _t)
    fWriter = open(fileFormat, "w")

    # 1. The parameters of the game: the values of n, b, s, t
    fWriter.write(
        "Game parameters: [Size n = {}, Blocs b = {}, winSize s = {}, Overtime t = {}]\n".format(_n, _b, _s, _t))
    # 2. The position of the blocs
    fWriter.write("Position of each blocs: {}\n\r".format(_b_coord))
    # 3. player info
    fWriter.write("Player 1: {}, d={}, a={}, {}\n".format(_player1, _d1, _algo1, "h1"))
    fWriter.write("Player 2: {}, d={}, a={}, {}\n\r".format(_player2, _d2, _algo2, "h2"))

    g = Game(n=_n, s=_s, b=_b, b_coord=_b_coord, d1=_d1, d2=_d2, t=_t, f=fWriter, h_swap=_h_swap)
    # 4. initial config of board
    fWriter.write("4. Initial configuration of the board.{}\n".format(g.draw_board()))
    g.play(algo1=_algo1, algo2=_algo2, player_x=_player1, player_o=_player2)
    fWriter.close()

    """2 x r run"""
    # writing
    fileFormat = "scoredBoard.txt"
    fWriter = open(fileFormat, "w")

    # 1. The parameters of the game: the values of n, b, s, t
    fWriter.write(
        "Game parameters: [Size n = {}, Blocs b = {}, winSize s = {}, Overtime t = {}]\n".format(_n, _b, _s, _t))
    # 2. player info
    fWriter.write("Player 1: d={}, a={}, {}\n".format(_d1, _algo1, "h1"))
    fWriter.write("Player 2: d={}, a={}, {}\n\r".format(_d2, _algo2, "h2"))
    # 3. The number of games played (the value of 2xr)
    fWriter.write("The number of games played: {}\n\r".format(2 * _r))
    # 4. The number and percentage of wins for heuristic el and for heuristic e2
    g = Game(n=_n, s=_s, b=_b, b_coord=_b_coord, d1=_d1, d2=_d2, t=_t, f=fWriter, h_swap=_h_swap)
    g.list_of_winner = []
    for i in range(0, _r):
        g.play(algo1=_algo1, algo2=_algo2, player_x=_player1, player_o=_player2)
    for i in range(0, _r):
        g.play(algo1=_algo1, algo2=_algo2, player_x=_player2, player_o=_player1)
    winningStat = {x: g.list_of_winner.count(x) for x in sorted(set(g.list_of_winner))}
    totalWinCount = len(g.list_of_winner)
    h1Win = winningStat['h1'] if 'h1' in winningStat else 0
    h2Win = winningStat['h2'] if 'h2' in winningStat else 0
    fWriter.write("Total wins for heuristic e1: {}, ({}%) ({})\n".format(h1Win, 100*(h1Win / totalWinCount), 'simple'))
    fWriter.write("Total wins for heuristic e2: {}, ({}%) ({})\n\r".format(h2Win,
                                                                           100*(h2Win / totalWinCount), 'complicate'))

    # 5. total game trace:
    # note that every parameter was averaged over 2 x r
    # gameTraceOpt.endGameTrace(self.f, isGameEnd, self.total_eval_time, self.total_eval_count,
    #                                       self.avg_depth_of_nodes, self.avg_ard_list, self.move_count)


if __name__ == "__main__":
    main()
