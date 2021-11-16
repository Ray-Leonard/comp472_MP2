# simple heuristcs
from copy import deepcopy

def h1(game):
    result = game.is_end()
    if result == 'X':
        return float('-inf')
    elif result == 'O':
        return float('inf')
    elif result == '.':
        return 0
    # X is for min; O is for max
    score = 0
    # score is dependent of the number of X's or O's in rows, columns, and diagonals.
    # the value added into or subtracted from the score is 2 powered to the number of X's or O's
    # the number of blocks can possibly adjust the score TO DO and TO TEST
    # row evaluation
    for x in range(0, game.n):
        score += (1 / (game.current_state[x].count('*') + 1)) * (pow(game.n, 2) / game.s) * game.current_state[x].count(
            'O')
        score -= (1 / (game.current_state[x].count('*') + 1)) * (pow(game.n, 2) / game.s) * game.current_state[x].count(
            'X')

    # if n != s, we do have four diagonals other than the two main diagonal. Otherwise, we only need to consider
    # slash "/"
    list_all_diagonals_1 = game.get_diagonal("slash")
    # backslash "\"
    list_all_diagonals_2 = game.get_diagonal("backslash")
    # Iterate all possible diagonals to calculate the score
    for x in list_all_diagonals_1:
        score += (1 / (x.count('*') + 1)) * (pow(game.n, 2) / game.s) * x.count('O')
        score -= (1 / (x.count('*') + 1)) * (pow(game.n, 2) / game.s) * x.count('X')

    for x in list_all_diagonals_2:
        score += (1 / (x.count('*') + 1)) * (pow(game.n, 2) / game.s) * x.count('O')
        score -= (1 / (x.count('*') + 1)) * (pow(game.n, 2) / game.s) * x.count('X')

    # column evaluation
    for x in range(0, game.n):
        column = [i[x] for i in game.current_state]
        score += (1 / (column.count('*') + 1)) * (pow(game.n, 2) / game.s) * column.count('O')
        score -= (1 / (column.count('*') + 1)) * (pow(game.n, 2) / game.s) * column.count('X')
    return score


# complicated heuristics
# return the number of possible winning rows,columns diagnols of max -the number possible winning rows, columns, diagnols of min
def h2(game):
    result = game.is_end()
    if result == 'X':
        return float('-inf')
    elif result == 'O':
        return float('inf')
    elif result == '.':
        return 0

    counter_max = 0
    counter_min = 0
    consecutive_min = False
    consecutive_max = False
    total_list_max = []
    total_list_min = []
    # rows plus columns evaluation
    for x in range(game.n):
        # initialize the parameters for the next evaluation
        list_max = []
        list_min = []
        consecutive_min = False
        consecutive_max = False
        total_list_max = []
        total_list_min = []
        # row evaluation
        for j in game.current_state[x]:
            # calculate the number of consecutive X or O
            if j == 'O':
                list_max.append('O')
                consecutive_max = True
                if consecutive_min:
                    total_list_min.append(deepcopy(list_min))
                    list_min = []
                    consecutive_min = False

            elif j == 'X':
                list_min.append('X')
                consecutive_min = True
                if consecutive_max:
                    total_list_max.append(deepcopy(list_max))
                    list_max = []
                    consecutive_max = False
            # when it encounters the block, end counting the number of consecutive X or O
            elif j == '*':
                if consecutive_max:
                    total_list_max.append(deepcopy(list_max))
                    list_max = []
                    consecutive_max = False
                if consecutive_min:
                    total_list_min.append(deepcopy(list_min))
                    list_min = []
                    consecutive_min = False
            elif j == '.':
                list_min.append('.')
                list_max.append('.')

        # several strategies
        # two ends with "." MAX
        for i in total_list_max:
            counter_max += 5 * i.count('O')
            if i[0] == '.' and i[-1] == '.' and i.count('O') == game.s - 1:
                counter_max += 1000
            if i[0] == '.' and i[-1] == '.' and i.count('.') > 2 and i.count('O') == game.s - 2:
                counter_max += 500
            if (i[0] == '.' or i[-1] == '.') and 1 <= i.count('O') <= game.s - 2:
                counter_max += 100 * i.count('O')
            # possible winning ways
            if i.count('.') + i.count('O') >= game.s:
                counter = 0
                cons = False
                for j in i:
                    if not cons and i == '.':
                        counter += 1
                        cons = True
                    else:
                        cons = False

                    if counter == 0:
                        counter_max += 0
                    elif counter == 1:
                        counter_max += 10
                    elif counter == 2:
                        counter_max += 50
                    else:
                        counter_max += 100
        for i in total_list_min:
            counter_min += 5 * i.count('X')
            if i[0] == '.' and i[-1] == '.' and i.count('X') == game.s - 1:
                counter_min += 1000
            if i[0] == '.' and i[-1] == '.' and i.count('.') > 2 and i.count('X') == game.s - 2:
                counter_min += 500
            if (i[0] == '.' or i[-1] == '.') and 1 <= i.count('X') <= game.s - 2:
                counter_min += 100 * i.count('X')
            # possible winning ways
            if i.count('.') + i.count('X') >= game.s:
                counter = 0
                cons = False
                for j in i:
                    if not cons and i == '.':
                        counter += 1
                        cons = True
                    else:
                        cons = False

                    if counter == 0:
                        counter_min += 0
                    elif counter == 1:
                        counter_min += 10
                    elif counter == 2:
                        counter_min += 50
                    else:
                        counter_min += 100
        # initialize the parameters for the next evaluation
        list_max = []
        list_min = []
        consecutive_min = False
        consecutive_max = False
        total_list_max = []
        total_list_min = []
        # Column Evaluation
        for j in [i[x] for i in game.current_state]:
            # calculate the number of consecutive X or O
            if j == 'O':
                list_max.append('O')
                consecutive_max = True
                if consecutive_min:
                    total_list_min.append(deepcopy(list_min))
                    list_min = []
                    consecutive_min = False

            elif j == 'X':
                list_min.append('X')
                consecutive_min = True
                if consecutive_max:
                    total_list_max.append(deepcopy(list_max))
                    list_max = []
                    consecutive_max = False
            # when it encounters the block, end counting the number of consecutive X or O
            elif j == '*':
                if consecutive_max:
                    total_list_max.append(deepcopy(list_max))
                    list_max = []
                    consecutive_max = False
                if consecutive_min:
                    total_list_min.append(deepcopy(list_min))
                    list_min = []
                    consecutive_min = False
            elif j == '.':
                list_min.append('.')
                list_max.append('.')
        # several strategies
        # two ends with "." MAX
        for i in total_list_max:
            counter_max += 5 * i.count('O')
            if i[0] == '.' and i[-1] == '.' and i.count('O') == game.s - 1:
                counter_max += 1000
            if i[0] == '.' and i[-1] == '.' and i.count('.') > 2 and i.count('O') == game.s - 2:
                counter_max += 500
            if (i[0] == '.' or i[-1] == '.') and 1 <= i.count('O') <= game.s - 2:
                counter_max += 100 * i.count('O')
            # possible winning ways
            if i.count('.') + i.count('O') >= game.s:
                counter = 0
                cons = False
                for j in i:
                    if not cons and i == '.':
                        counter += 1
                        cons = True
                    else:
                        cons = False

                    if counter == 0:
                        counter_max += 0
                    elif counter == 1:
                        counter_max += 10
                    elif counter == 2:
                        counter_max += 50
                    else:
                        counter_max += 100
        for i in total_list_min:
            counter_min += 5 * i.count('X')
            if i[0] == '.' and i[-1] == '.' and i.count('X') == game.s - 1:
                counter_min += 1000
            if i[0] == '.' and i[-1] == '.' and i.count('.') > 2 and i.count('X') == game.s - 2:
                counter_min += 500
            if (i[0] == '.' or i[-1] == '.') and 1 <= i.count('X') <= game.s - 2:
                counter_min += 100 * i.count('X')
            # possible winning ways
            if i.count('.') + i.count('X') >= game.s:
                counter = 0
                cons = False
                for j in i:
                    if not cons and i == '.':
                        counter += 1
                        cons = True
                    else:
                        cons = False

                    if counter == 0:
                        counter_min += 0
                    elif counter == 1:
                        counter_min += 10
                    elif counter == 2:
                        counter_min += 50
                    else:
                        counter_min += 100
    # diagnols evaluation
    # if n != s, we do have four diagonals other than the two main diagonal. Otherwise, we only need to consider
    # slash "/"
    list_all_diagonals_1 = game.get_diagonal("slash")
    # backslash "\"
    list_all_diagonals_2 = game.get_diagonal("backslash")

    # the eval for the first diag
    for x in list_all_diagonals_1:
        # initialize the parameters for the next evalution
        list_max = []
        list_min = []
        consecutive_min = False
        consecutive_max = False
        total_list_max = []
        total_list_min = []
        for j in x:
            # calculate the number of consecutive X or O
            if j == 'O':
                list_max.append('O')
                consecutive_max = True
                if consecutive_min:
                    total_list_min.append(deepcopy(list_min))
                    list_min = []
                    consecutive_min = False

            elif j == 'X':
                list_min.append('X')
                consecutive_min = True
                if consecutive_max:
                    total_list_max.append(deepcopy(list_max))
                    list_max = []
                    consecutive_max = False
            # when it encounters the block, end counting the number of consecutive X or O
            elif j == '*':
                if consecutive_max:
                    total_list_max.append(deepcopy(list_max))
                    list_max = []
                    consecutive_max = False
                if consecutive_min:
                    total_list_min.append(deepcopy(list_min))
                    list_min = []
                    consecutive_min = False
            elif j == '.':
                list_min.append('.')
                list_max.append('.')
        for i in total_list_max:
            counter_max += 5 * i.count('O')
            if i[0] == '.' and i[-1] == '.' and i.count('O') == game.s - 1:
                counter_max += 1000
            if i[0] == '.' and i[-1] == '.' and i.count('.') > 2 and i.count('O') == game.s - 2:
                counter_max += 500
            if (i[0] == '.' or i[-1] == '.') and 1 <= i.count('O') <= game.s - 2:
                counter_max += 100 * i.count('O')
            # possible winning ways
            if i.count('.') + i.count('O') >= game.s:
                counter = 0
                cons = False
                for j in i:
                    if not cons and i == '.':
                        counter += 1
                        cons = True
                    else:
                        cons = False

                    if counter == 0:
                        counter_max += 0
                    elif counter == 1:
                        counter_max += 10
                    elif counter == 2:
                        counter_max += 50
                    else:
                        counter_max += 100
        for i in total_list_min:
            counter_min += 5 * i.count('X')
            if i[0] == '.' and i[-1] == '.' and i.count('X') == game.s - 1:
                counter_min += 1000
            if i[0] == '.' and i[-1] == '.' and i.count('.') > 2 and i.count('X') == game.s - 2:
                counter_min += 500
            if (i[0] == '.' or i[-1] == '.') and 1 <= i.count('X') <= game.s - 2:
                counter_min += 100 * i.count('X')
            # possible winning ways
            if i.count('.') + i.count('X') >= game.s:
                counter = 0
                cons = False
                for j in i:
                    if not cons and i == '.':
                        counter += 1
                        cons = True
                    else:
                        cons = False
                    if counter == 0:
                        counter_min += 0
                    elif counter == 1:
                        counter_min += 10
                    elif counter == 2:
                        counter_min += 50
                    else:
                        counter_min += 100
    # the eval for the second diag
    for x in list_all_diagonals_2:
        # initialize the parameters for the next evalution
        list_max = []
        list_min = []
        consecutive_min = False
        consecutive_max = False
        total_list_max = []
        total_list_min = []
        for j in x:
            # calculate the number of consecutive X or O
            if j == 'O':
                list_max.append('O')
                consecutive_max = True
                if consecutive_min:
                    total_list_min.append(deepcopy(list_min))
                    list_min = []
                    consecutive_min = False

            elif j == 'X':
                list_min.append('X')
                consecutive_min = True
                if consecutive_max:
                    total_list_max.append(deepcopy(list_max))
                    list_max = []
                    consecutive_max = False
            # when it encounters the block, end counting the number of consecutive X or O
            elif j == '*':
                if consecutive_max:
                    total_list_max.append(deepcopy(list_max))
                    list_max = []
                    consecutive_max = False
                if consecutive_min:
                    total_list_min.append(deepcopy(list_min))
                    list_min = []
                    consecutive_min = False
            elif j == '.':
                list_min.append('.')
                list_max.append('.')
        for i in total_list_max:
            counter_max += 5 * i.count('O')
            if i[0] == '.' and i[-1] == '.' and i.count('O') == game.s - 1:
                counter_max += 100
            if i[0] == '.' and i[-1] == '.' and i.count('.') > 2 and i.count('O') == game.s - 2:
                counter_max += 500
            if (i[0] == '.' or i[-1] == '.') and 1 <= i.count('O') <= game.s - 2:
                counter_max += 100 * i.count('O')
            # possible winning ways
            if i.count('.') + i.count('O') >= game.s:
                counter = 0
                cons = False
                for j in i:
                    if not cons and i == '.':
                        counter += 1
                        cons = True
                    else:
                        cons = False

                    if counter == 0:
                        counter_max += 0
                    elif counter == 1:
                        counter_max += 10
                    elif counter == 2:
                        counter_max += 50
                    else:
                        counter_max += 100
        for i in total_list_min:
            counter_min += 5 * i.count('X')
            if i[0] == '.' and i[-1] == '.' and i.count('X') == game.s - 1:
                counter_min += 1000
            if i[0] == '.' and i[-1] == '.' and i.count('.') > 2 and i.count('X') == game.s - 2:
                counter_min += 500
            if (i[0] == '.' or i[-1] == '.') and 1 <= i.count('X') <= game.s - 2:
                counter_min += 100 * i.count('X')
            # possible winning ways
            if i.count('.') + i.count('X') >= game.s:
                counter = 0
                cons = False
                for j in i:
                    if not cons and i == '.':
                        counter += 1
                        cons = True
                    else:
                        cons = False

                    if counter == 0:
                        counter_min += 0
                    elif counter == 1:
                        counter_min += 10
                    elif counter == 2:
                        counter_min += 50
                    else:
                        counter_min += 100

    return counter_max - counter_min



