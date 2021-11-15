import lineemup


def inGameTrace(f, curr_player, move, newBoardGraph, evalTime, numOfStates, depthOfNodes, ard, count):
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
    f.write("5(a). {} plays: {}\n\r".format(curr_player, move))
    f.write("5(b). (move {}) \nNew configuration of the board.{}\n".format(count, newBoardGraph))
    f.write("5(ci). The evaluation time of the heuristic: {}s\n".format(evalTime))
    f.write("5(cii). The number of states evaluated by the heuristic function: {}\n".format(numOfStates))
    f.write("5(ciii). The number of states evaluated at each depth: {}\n".format(statesOfEachDepth))
    f.write("5(civ).The average depth (AD): {}\n".format(averageDepth))
    f.write("5(cv). The average recursion depth (ARD): {}\n\r".format(ard))


def endGameTrace(f, winner, totalEvalTime, totalEval, depthOfNodes, avgARDList, totalMove):
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

    avgEvalTime = totalEvalTime / totalMove
    statesEvalAtDepth = ["depth{} = {}".format(x, depthOfNodes.count(x)) for x in sorted(set(depthOfNodes))]
    avgAvgDepth = sum(depthOfNodes) / len(depthOfNodes)
    avgARD = sum(avgARDList) / len(avgARDList)

    # print
    if winner != '.':
        f.write("6(a). The Winner: {}\n".format(winner))
    else:
        f.write("6(a). Tie\n")


    f.write("6(bi). Average evaluation time: {}\n".format(avgEvalTime))

    f.write("6(bii). Total heuristic evaluations: {}\n".format(totalEval))

    f.write("6(biii). Average of Average depth: {}\n".format(avgAvgDepth))
    f.write("6(biv). The total number of states evaluated at each depth: {}\n".format(statesEvalAtDepth))
    f.write("6(bv). Average of average recursion depth: {}\n".format(avgARD))
    f.write("6(bvi). The total number of moves in the game: {}\n\r".format(totalMove))


