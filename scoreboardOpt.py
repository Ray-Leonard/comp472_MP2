import gameTraceOpt

def main():
    # sample parameters
    n = 1
    b = 2
    s = 3
    t = 4
    # Player 1:
    depth1 = 5
    a1 = True
    heuristicFunc1 = "manhattan"
    # Player 2:
    depth2 = 5
    a2 = True
    heuristicFunc2 = "manhattan"
    # round to play
    r = 10
    # e1 wins
    e1 = 3
    e2 = 7
    # endGame sample variable
    _winner = "AI-1"
    _avgEvalTime = 5
    _totalEval = 9999999
    _avgAvgDepth = 123456789
    _statesEvalAtDepth = {4: 22582, 8: 175396, 7: 590, 6: 663, 5: 85744, 3: 88, 2: 20, 1: 2}
    _avgARD = 8
    _totalMove = 999999999999

    # start writing
    fileFormat = "scoredBoard.txt"
    fWriter = open(fileFormat, "w")

    # 1. The parameters of the game: the values of n, b, s, t
    fWriter.write("Game parameters: [Size n = {}, Blocs b = {}, winSize s = {}, Overtime t = {}]\n".format(n, b, s, t))
    # 2. player info
    fWriter.write("Player 1: d={}, a={}, {}\n".format(depth1, a1, heuristicFunc1))
    fWriter.write("Player 2: d={}, a={}, {}\n\r".format(depth2, a2, heuristicFunc2))
    # 3. The number of games played (the value of 2xr)
    fWriter.write("The number of games played: {}\n\r".format(2 * r))
    # 4. The number and percentage of wins for heuristic el and for heuristic e2
    fWriter.write("Total wins for heuristic e1: {} ({}) ({})\n\r".format(e1, e1/(e1+e2), heuristicFunc1))
    fWriter.write("Total wins for heuristic e2: {} ({}) ({})\n\r".format(e2, e2/(e1+e2), heuristicFunc2))
    # 5. total game trace:
    # note that every parameter was averaged over 2 x t (professor writes 2 x s, confused!)
    gameTraceOpt.endGameTrace(fWriter, _winner, _avgEvalTime, _totalEval, _avgAvgDepth, _statesEvalAtDepth, _avgARD, _totalMove)


if __name__ == "__main__":
    main()
