def inGameTrace(f, move, evalTime, numOfStates, depthOfNodes):
    # Todo 4. A display of the initial configuration of the board.

    # 5(a) the move taken
    f.write("The move taken: {}\n".format(move))

    # Todo 5(b) the new configuration of the board

    # 5(ci). The evaluation time of the heuristic (in seconds)
    f.write("The evaluation time of the heuristic: {}s\n".format(evalTime))

    # 5(cii). The number of states evaluated by the heuristic function
    f.write("The number of states evaluated by the heuristic function: {}\n".format(numOfStates))

    # 5(ciii). The number of states evaluated at each depth (consider the root to be at depth 0)
    statesOfEachDepth = ["depth{} = {}".format(x, depthOfNodes.count(x)) for x in sorted(set(depthOfNodes))]
    f.write("The number of states evaluated at each depth: {}\n".format(statesOfEachDepth))

    # 5(civ). The average depth (AD) of the heuristic evaluation in the tree
    averageDepth = sum(depthOfNodes) / len(depthOfNodes)
    f.write("The average depth (AD): {}\n".format(averageDepth))

    # Todo 5(cv). The average recursion depth (ARD) at the current state
    f.write("The average recursion depth (ARD): {}\n\r".format(" "))


def endGameTrace(f, winner, avgEvalTime, totalEval, avgAvgDepth, statesEvalAtDepth, avgARD, totalMove):
    # 6(a) the winner
    f.write("The Winner: {}\n".format(winner))

    # 6(bi). The average evaluation time of the heuristic for each state evaluated (in seconds)
    f.write("6(b)i   Average evaluation time: {}\n".format(avgEvalTime))

    # Todo 6(bii). The number of states evaluated by the heuristic function during the entire game
    f.write("6(b)ii  Total heuristic evaluations: {}\n".format(totalEval))

    # 6(biii). The average of the per-move average depth of the heuristic evaluation in the tree
    f.write("6(b)iii Average of Average depth: {}\n".format(avgAvgDepth))

    # 6(biv). The total number of states evaluated at each depth during the entire game
    f.write("6(b)iv The total number of states evaluated at each depth: {}\n".format(statesEvalAtDepth))

    # 6(bv). The average of the per-move average recursion depth
    f.write("6(b)v Average of average recursion depth: {}\n".format(avgARD))

    # 6(bvi). The total number of moves in the game
    f.write("6(b)vi The total number of moves in the game: {}\n".format(totalMove))


def main():
    # sample parameters
    n = 1
    b = 2
    s = 3
    t = 4
    bloc = [(2, 3), (3, 4), (4, 5)]
    # Player 1:
    playerType1 = "AI"
    depth1 = 5
    a1 = True
    heuristicFunc1 = "manhattan"
    # Player 2:
    playerType2 = "AI"
    depth2 = 5
    a2 = True
    heuristicFunc2 = "manhattan"

    # inGame sample variable
    _move = ["B", 4]
    _evalTime = 10
    _numOfStates = 9999
    _depthOfNodes = [3, 3, 2, 3, 3, 2, 2, 1, 1]

    # endGame sample variable
    _winner = "AI-1"
    _avgEvalTime = 5
    _totalEval = 9999999
    _avgAvgDepth = 123456789
    _statesEvalAtDepth = {4: 22582, 8: 175396, 7: 590, 6: 663, 5: 85744, 3: 88, 2: 20, 1: 2}
    _avgARD = 8
    _totalMove = 999999999999

    # start writing
    fileFormat = "gameTrace-{}{}{}{}.txt".format(n, b, s, t)
    fWriter = open(fileFormat, "w")

    # 1. The parameters of the game: the values of n, b, s, t
    fWriter.write("Game parameters: [Size n = {}, Blocs b = {}, winSize s = {}, Overtime t = {}]\n".format(n, b, s, t))
    # 2. The position of the blocs
    fWriter.write("Position of each blocs: {}\n\r".format(bloc))
    # 3. player info
    fWriter.write("Player 1: {},{},{},{}\n".format(playerType1, depth1, a1, heuristicFunc1))
    fWriter.write("Player 2: {},{},{},{}\n\r".format(playerType2, depth2, a2, heuristicFunc2))

    inGameTrace(fWriter, _move, _evalTime, _numOfStates, _depthOfNodes)
    endGameTrace(fWriter, _winner, _avgEvalTime, _totalEval, _avgAvgDepth, _statesEvalAtDepth, _avgARD, _totalMove)

    fWriter.close()


if __name__ == "__main__":
    main()
