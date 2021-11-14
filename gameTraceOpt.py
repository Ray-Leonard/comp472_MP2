
# sample parameters of the game
n = 1
b = 2
s = 3
t = 4
fileFormat = "gameTrace-{}{}{}{}.txt".format(n, b, s, t)
f = open(fileFormat, "w")
# 1. The parameters of the game: the values of n, b, s, t
f.write("Game parameters: [Size n = {}, Blocs b = {}, Winning size s = {}, Overtime t = {}]\n".format(n, b, s, t))

# sample bloc
bloc = [(2, 3), (3, 4), (4, 5)]
# 2. The position of the blocs
f.write("Position of each blocs: {}\n\r".format(bloc))

# 3. player info
# note that for a: true for alpha-beta, false for minimax
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
# print:
f.write("Player 1: {},{},{},{}\n".format(playerType1, depth1, a1, heuristicFunc1))
f.write("Player 2: {},{},{},{}\n\r".format(playerType2, depth2, a2, heuristicFunc2))

# Todo 4. A display of the initial configuration of the board.
# need import skeleton-tictactoe.py
# but the weird naming of that file doesn't allow me to do that


# 5. Then, for each move, display:
# (a) the move taken
# sample move
move = ["B", 4]
f.write("The move taken: {}\n".format(move))

# Todo (b) the new configuration of the board
# need import skeleton-tictactoe.py

# (c) statistics:

# i. The evaluation time of the heuristic (in seconds)
# sample time
evaluTime = 10
f.write("The evaluation time of the heuristic: {}s\n".format(evaluTime))

# ii. The number of states evaluated by the heuristic function
# sample numOfStates
numOfStates = 9999
f.write("The number of states evaluated by the heuristic function: {}\n".format(numOfStates))

# iii. The number of states evaluated at each depth (consider the root to be at depth 0)
# sample Depth of nodes
depthOfNodes = [3, 3, 2, 3, 3, 2, 2, 1, 1]
depths = sorted(set(depthOfNodes))
# sample numOfStatesOfDepth
statesOfEachDepth = ["depth{} = {}".format(x, depthOfNodes.count(x)) for x in depths]
f.write("The number of states evaluated at each depth: {}\n".format(statesOfEachDepth))

# iv. The average depth (AD) of the heuristic evaluation in the tree
# sample average depth
averageDepth = sum(depthOfNodes)/len(depthOfNodes)
f.write("The number of states evaluated at each depth: {}\n".format(averageDepth))

# Todo v. The average recursion depth (ARD) at the current state
# for x in depths[::-1]:
#     for



f.close()