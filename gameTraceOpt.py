import lineemup


def inGameTrace(f, move, newBoardGraph, evalTime, numOfStates, depthOfNodes):
    """Responsible for displaying in loop game trace."""
    """
       Imported Parameters
       ----------
            f : file writer
            move : list
                A list containing the move taken in this iteration
            newBoardGraph: string
                a string containing the new boardGraph
            evalTime : float/int/double
                The evaluation time of the heuristic (in seconds)
            numOfStates : int
                The number of states evaluated by the heuristic function
            depthOfNodes : list of int
                A list of the depth of each nodes
                
       Generated Parameters
       ----------    
            statesOfEachDepth: list of strings
                The number of states evaluated at each depth (consider the root to be at depth 0)
            averageDepth: double
                The average depth (AD) of the heuristic evaluation in the tree
    """
    # generating parameters
    statesOfEachDepth = ["depth{} = {}".format(x, depthOfNodes.count(x)) for x in sorted(set(depthOfNodes))]
    averageDepth = sum(depthOfNodes) / len(depthOfNodes)

    # write
    f.write("5(a). The move taken: {}\n\r".format(move))
    f.write("5(b). New configuration of the board.{}\n".format(newBoardGraph))
    f.write("5(ci). The evaluation time of the heuristic: {}s\n".format(evalTime))
    f.write("5(cii). The number of states evaluated by the heuristic function: {}\n".format(numOfStates))
    f.write("5(ciii). The number of states evaluated at each depth: {}\n".format(statesOfEachDepth))
    f.write("5(civ).The average depth (AD): {}\n".format(averageDepth))
    # Todo 5(cv). The average recursion depth (ARD) at the current state
    f.write("5(cv). The average recursion depth (ARD): {}\n\r".format(" "))
    # need to write a recursive function to grab the information


def endGameTrace(f, winner, avgEvalTime, totalEval, avgAvgDepth, statesEvalAtDepth, avgARD, totalMove):
    """Responsible for displaying end game statics."""
    """
           Imported Parameters
           ----------
                f : file writer
                the winner : string
                    The name of the winner
                avgEvalTime : float/int/double
                    The average evaluation time of the heuristic for each state evaluated (in seconds)
                totalEval : int
                    The number of states evaluated by the heuristic function during the entire game
                avgAvgDepth: float/double
                    The average of the per-move average depth of the heuristic evaluation in the tree
                statesEvalAtDepth: dict
                    The total number of states evaluated at each depth during the entire game
                avgARD:
                    The average of the per-move average recursion depth
                totalMove:
                    The total number of moves in the game
    """
    # print
    f.write("6(a). The Winner: {}\n".format(winner))
    f.write("6(bi). Average evaluation time: {}\n".format(avgEvalTime))
    f.write("6(bii). Total heuristic evaluations: {}\n".format(totalEval))
    f.write("6(biii). Average of Average depth: {}\n".format(avgAvgDepth))
    f.write("6(biv). The total number of states evaluated at each depth: {}\n".format(statesEvalAtDepth))
    f.write("6(bv). Average of average recursion depth: {}\n".format(avgARD))
    f.write("6(bvi). The total number of moves in the game: {}\n\r".format(totalMove))


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

    #sample graph
    g = lineemup.Game(n=5, s=3, b=0)
    g1 = lineemup.Game(n=5, s=3, b=0)
    g.current_state = [
        ['X', '.', '.', '.', '.'],
        ['O', 'X', 'X', '.', 'O'],
        ['X', 'O', '.', 'O', '.'],
        ['X', 'X', 'X', 'O', 'O'],
        ['.', 'X', '.', 'X', '.']
    ]
    g1.current_state = [
        ['X', '.', 'O', 'O', 'O'],
        ['O', 'X', 'X', '.', 'O'],
        ['X', 'O', 'O', 'O', 'O'],
        ['X', 'X', 'X', 'O', 'O'],
        ['O', 'X', '.', 'X', '.']
    ]
    oldBoardGraph = g.draw_board()
    newBoardGraph = g1.draw_board()

    # start writing
    fileFormat = "gameTrace-{}{}{}{}.txt".format(n, b, s, t)
    fWriter = open(fileFormat, "w")

    # 1. The parameters of the game: the values of n, b, s, t
    fWriter.write("Game parameters: [Size n = {}, Blocs b = {}, winSize s = {}, Overtime t = {}]\n".format(n, b, s, t))
    # 2. The position of the blocs
    fWriter.write("Position of each blocs: {}\n\r".format(bloc))
    # 3. player info
    fWriter.write("Player 1: {}, d={}, a={}, {}\n".format(playerType1, depth1, a1, heuristicFunc1))
    fWriter.write("Player 2: {}, d={}, a={}, {}\n\r".format(playerType2, depth2, a2, heuristicFunc2))

    inGameTrace(fWriter, oldBoardGraph, _move, newBoardGraph, _evalTime, _numOfStates, _depthOfNodes)
    endGameTrace(fWriter, _winner, _avgEvalTime, _totalEval, _avgAvgDepth, _statesEvalAtDepth, _avgARD, _totalMove)

    fWriter.close()


if __name__ == "__main__":
    main()
