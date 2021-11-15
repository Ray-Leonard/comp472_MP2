# simple heuristcs
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
        score += (pow(2, game.current_state[x].count('0')) - 1)
        score -= (pow(2, game.current_state[x].count('X')) - 1)
    # diagonal evaluation
    diff_size_win = game.n - game.s

    # if n != s, we do have four diagonals other than the two main diagonal. Otherwise, we only need to consider
    # slash "/"
    list_all_diagonals_1 = game.get_diagonal("slash")
    # backslash "\"
    list_all_diagonals_2 = game.get_diagonal("backslash")
    # Iterate all possible diagonals to calculate the score
    for x in list_all_diagonals_1:
        score += (pow(2, x.count('0')) - 1)
        score -= (pow(2, x.count('X')) - 1)

    for x in list_all_diagonals_2:
        score += (pow(2, x.count('0')) - 1)
        score -= (pow(2, x.count('X')) - 1)

    # column evaluation
    for x in range(0, game.n):
        score += (pow(2, [i[x] for i in game.current_state].count('0')) - 1)
        score -= (pow(2, [i[x] for i in game.current_state].count('X')) - 1)
    return score

#complicated heuristics
#return the number of possible winning rows,columns diagnols of max -the number possible winning rows, columns, diagnols of min
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
    win_indicator_max=0
    win_indicator_min = 0
    consecutive_min = False
    consecutive_max = False


    #row plus columns evaluation
    for x in range(game.n):
        # initialize the parameters for the next evalution
        win_indicator_max = 0
        win_indicator_min = 0
        consecutive_min = False
        consecutive_max = False
        # row evalution
        for j in game.current_state[x]:
            # calculate the number of consecutive X or O
            if j == 'O':
                win_indicator_max += 1
                consecutive_max = True
                if consecutive_min:
                    win_indicator_min = 0
                    consecutive_min = False

            elif j == 'X':
                win_indicator_min += 1
                consecutive_min = True
                if consecutive_max:
                    win_indicator_max = 0
                    consecutive_max = False
            # when it encounters the block, end counting the number of consecutive X or O
            elif j == '*':
                if consecutive_max:
                    win_indicator_max = 0
                    consecutive_max = False
                elif consecutive_min:
                    win_indicator_min = 0
                    consecutive_min = False

            # update the win_indicator according to the number of "."
            if j == '.' and consecutive_max:
                win_indicator_max += 1

            elif j == '.' and consecutive_min:
                win_indicator_min += 1

        if win_indicator_max >= game.s:
            counter_max += 1

        if win_indicator_min >= game.s:
            counter_min += 1

        #initialize the parameters for the next evalution
        win_indicator_max = 0
        win_indicator_min = 0
        consecutive_min = False
        consecutive_max = False

        # Column Evaluation
        for j in [i[x] for i in game.current_state]:
            # calculate the number of consecutive X or O
            if j == 'O':
                win_indicator_max += 1
                consecutive_max = True
                if consecutive_min:
                    win_indicator_min = 0
                    consecutive_min = False

            elif j == 'X':
                win_indicator_min += 1
                consecutive_min = True
                if consecutive_max:
                    win_indicator_max = 0
                    consecutive_max = False
            # when it encounters the block, end counting the number of consecutive X or O
            elif j == '*':
                if consecutive_max:
                    win_indicator_max = 0
                    consecutive_max = False
                elif consecutive_min:
                    win_indicator_min = 0
                    consecutive_min = False

            #update the win_indicator according to the number of "."
            if j == '.' and consecutive_max :
                 win_indicator_max += 1

            elif j == '.' and consecutive_min:
                 win_indicator_min += 1

        if win_indicator_max>= game.s:
            counter_max += 1

        if win_indicator_min>= game.s:
            counter_min += 1

        

    #diagnols evaluation
    # if n != s, we do have four diagonals other than the two main diagonal. Otherwise, we only need to consider
    # slash "/"
    list_all_diagonals_1 = game.get_diagonal("slash")
    # backslash "\"
    list_all_diagonals_2 = game.get_diagonal("backslash")
    
    # the eval for the first diag
    for i in list_all_diagonals_1:
        # initialize the parameters for the next evalution
        win_indicator_max = 0
        win_indicator_min = 0
        consecutive_min = False
        consecutive_max = False
        
        for j in i:
            # calculate the number of consecutive X or O
            if j == 'O':
                win_indicator_max += 1
                consecutive_max = True
                if consecutive_min:
                    win_indicator_min = 0
                    consecutive_min = False

            elif j == 'X':
                win_indicator_min += 1
                consecutive_min = True
                if consecutive_max:
                    win_indicator_max = 0
                    consecutive_max = False
            # when it encounters the block, end counting the number of consecutive X or O
            elif j == '*':
                if consecutive_max:
                    win_indicator_max = 0
                    consecutive_max = False
                elif consecutive_min:
                    win_indicator_min = 0
                    consecutive_min = False

            # update the win_indicator according to the number of "."
            if j == '.' and consecutive_max:
                win_indicator_max += 1

            elif j == '.' and consecutive_min:
                win_indicator_min += 1

        if win_indicator_max >= game.s:
            counter_max += 1

        if win_indicator_min >= game.s:
            counter_min += 1

    # the eval for the second diag
    for i in list_all_diagonals_2:
            # initialize the parameters for the next evalution
            win_indicator_max = 0
            win_indicator_min = 0
            consecutive_min = False
            consecutive_max = False

            for j in i:
                # calculate the number of consecutive X or O
                if j == 'O':
                    win_indicator_max += 1
                    consecutive_max = True
                    if consecutive_min:
                        win_indicator_min = 0
                        consecutive_min = False

                elif j == 'X':
                    win_indicator_min += 1
                    consecutive_min = True
                    if consecutive_max:
                        win_indicator_max = 0
                        consecutive_max = False
                # when it encounters the block, end counting the number of consecutive X or O
                elif j == '*':
                    if consecutive_max:
                        win_indicator_max = 0
                        consecutive_max = False
                    elif consecutive_min:
                        win_indicator_min = 0
                        consecutive_min = False

                # update the win_indicator according to the number of "."
                if j == '.' and consecutive_max:
                    win_indicator_max += 1

                elif j == '.' and consecutive_min:
                    win_indicator_min += 1

            if win_indicator_max >= game.s:
                counter_max += 1

            if win_indicator_min >= game.s:
                counter_min += 1
     
    return counter_max - counter_min




