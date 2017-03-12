
from copy import deepcopy
import string
global boardSize, depth, alpha, beta, value, nodes, opponentPlayer,isFinalLevelCheck, positionalWeight, inputPlayer, playX, playY, counter
nodes = []
playX, playY = 0,0
counter = 0
#Prints infinity/-infinity for float inf values
def printInfinity(value):
    if value == -float("inf"):
        value = "-Infinity"
    elif value == float("inf"):
        value = "Infinity"
    return str(value)

#User defined class to store data and meta data of a node/move
class Nodes:
    def __init__(self, node, depth, value, alpha, beta, parent, originalMoveNumber, parentNumber):
        self.node = node
        self.depth = depth
        self.value = value
        self.alpha = alpha
        self.beta = beta
        self.parent = parent
        self.move = originalMoveNumber
        self.parentNumber = parentNumber
    def displayDetails(self):
        f = file("output1.txt", "a")
        f.write(self.node+",")
        f.write(str(self.depth)+",")
        f.write((printInfinity(self.value))+",")
        f.write(printInfinity(self.alpha)+",")
        f.write(printInfinity(self.beta))
        f.write("\n")

#Calculates value of a given state for the player
def evaluateValue(state, player):
    oppositePlayer = 'O' if 'X' == player.upper() else 'X'
    playerScore, oppositeScore = 0,0
    for i in range(boardSize):
        for j in range(boardSize):
            if player.upper() == state[i][j]:
                playerScore += positionalWeight[i][j]
            elif oppositePlayer.upper() == state[i][j]:
                oppositeScore += positionalWeight[i][j]
    return playerScore - oppositeScore

#Prints board state
def printState(state):
    f = file("output.txt", "a")
    f.write('\n'.join([''.join(['{:1}'.format(item) for item in row]) for row in state]))

#Determines next moves for the given state
def findMoves(state, player):
    moves = []
    tempmoves = []
    stateToCheck = "X" if "O" == player.upper() else "O"
    currentState = "X" if "X" == player.upper() else "O"
    for i in range(boardSize):
        for j in range(boardSize):
            if(currentState.upper() == str(state[i][j]).upper()):
                for x in (-1,0,1):
                    for y in (-1,0,1):
                        if 7>=x+i>=0 and 7>= y+j>=0 and stateToCheck == state[i+x][j+y] and (x!=0 or y!=0):
                            tempX = x
                            tempY = y
                            flag = True
                            while (flag and 7 >= tempX + i >= 0 and 7 >= tempY + j >= 0 and currentState != state[i + tempX][j + tempY]):
                                if ("*" == state[i + tempX][j + tempY]):
                                    if (int(str(i + tempX) + str(j + tempY)) not in tempmoves):
                                        tempmoves.append(int(str(i + tempX) + str(j + tempY)))
                                    flag = False
                                tempX += x
                                tempY += y
    tempmoves.sort()
    for move in tempmoves:
        a, b = divmod(move, 10)
        moves.append(str(a) + ":" + str(b))
    return moves

#Min function for alpha beta pruning
def minValue(state, level,originalMove, parent, player, originalMoveNumber, alpha, beta, parentNumber):
    global playX, playY, counter, inputPlayer
    value = float("inf")
    isFinalLevelCheck = True if level == int(depth) else False
    if isFinalLevelCheck:
        oppositePlayer = 'O' if 'X' == player.upper() else 'X'
        value = evaluateValue(state, inputPlayer)
        newNode = Nodes(originalMove, level, value, alpha, beta, parent, originalMoveNumber, parentNumber)
        nodes.append(newNode)
        Nodes.displayDetails(newNode)
    else:
        moves = findMoves(state, player)
        opponentPlayer = 'O' if 'X' == player.upper() else 'X'
        if 0 == moves.__len__():
            intermediateState = deepcopy(state)
            if 'X' == player:
                playX += 1
                currentPlay = playX
            else:
                playY += 1
                currentPlay = playY
            if (2 <= currentPlay):
                value = evaluateValue(intermediateState, inputPlayer)
                newNode = Nodes(originalMove, level, value, alpha, beta, parent, originalMoveNumber, parentNumber)
                nodes.append(newNode)
                Nodes.displayDetails(newNode)
            else:
                newNode = Nodes(originalMove, level, value, alpha, beta, parent, originalMoveNumber, parentNumber)
                nodes.append(newNode)
                Nodes.displayDetails(newNode)
                counter += 1
                value = min(value, maxValue(intermediateState, level + 1, "pass", originalMove, opponentPlayer, originalMoveNumber, alpha, beta, counter))
                if value > alpha:
                    beta = min(beta, value)
                for node in nodes:
                    if node.node == originalMove and node.parent == parent and node.parentNumber == parentNumber:
                        if node.value > value:
                            node.value = value
                            node.beta = beta
                        Nodes.displayDetails(node)
        else:
            newNode = Nodes(originalMove, level, value, alpha, beta, parent, originalMoveNumber, parentNumber)
            nodes.append(newNode)
            Nodes.displayDetails(newNode)
            flag = True
            for move in moves:
                playX, playY = 0, 0
                if(flag):
                    updatedMove = convert(move)
                    intermediateState = deepcopy(state)
                    intermediateState = drawBoard(intermediateState, move, player)
                    counter += 1
                    value = min(value, maxValue(intermediateState, level+1, updatedMove, originalMove, opponentPlayer, move, alpha, beta, counter))
                    if value <= alpha:
                        flag =False
                    else:
                        beta = min(beta, value)
                    for node in nodes:
                        if node.node == originalMove and node.parent == parent and node.parentNumber == parentNumber:
                            if node.value > value:
                                node.value = value
                                node.beta = beta
                            Nodes.displayDetails(node)
    return value

#Max function for alpha beta pruning
def maxValue(state, level, originalMove, parent, player, originalMoveNumber, alpha, beta, parentNumber):
    global playX, playY, counter, inputPlayer
    value = -float("inf")
    isFinalLevelCheck = True if level == int(depth) else False
    if isFinalLevelCheck:
        oppositePlayer = 'O' if 'X' == player.upper() else 'X'
        value = evaluateValue(state, inputPlayer)
        newNode = Nodes(originalMove, level, value, alpha, beta, parent, originalMoveNumber, parentNumber)
        nodes.append(newNode)
        Nodes.displayDetails(newNode)
    else:
        moves = findMoves(state, player)
        opponentPlayer = 'O' if 'X' == player.upper() else 'X'
        if 0 == moves.__len__():
            intermediateState = deepcopy(state)
            if 'X' == player:
                playX += 1
                currentPlay = playX
            else:
                playY += 1
                currentPlay = playY
            if(2 <= currentPlay):
                value = evaluateValue(intermediateState,inputPlayer)
                newNode = Nodes(originalMove, level, value, alpha, beta, parent, originalMoveNumber, parentNumber)
                nodes.append(newNode)
                Nodes.displayDetails(newNode)
            else:
                newNode = Nodes(originalMove, level, value, alpha, beta, parent, originalMoveNumber, parentNumber)
                nodes.append(newNode)
                Nodes.displayDetails(newNode)
                counter += 1
                value = max(value, minValue(intermediateState, level + 1, "pass", originalMove, opponentPlayer, originalMoveNumber, alpha, beta, counter))
                if value <= beta:
                    alpha = max(value, alpha)
                for node in nodes:
                    if node.node == originalMove and node.parent == parent and node.parentNumber == parentNumber:
                        if node.value < value:
                            node.value = value
                            node.alpha = alpha
                        Nodes.displayDetails(node)
        else:
            newNode = Nodes(originalMove, level, value, alpha, beta, parent, originalMoveNumber, parentNumber)
            nodes.append(newNode)
            Nodes.displayDetails(newNode)
            flag = True
            for move in moves:
                playX, playY = 0, 0
                if(flag):
                    updatedMove = convert(move)
                    intermediateState = deepcopy(state)
                    intermediateState = drawBoard(intermediateState, move, player)
                    counter += 1
                    value = max(value, minValue(intermediateState, level+1, updatedMove, originalMove, opponentPlayer, move, alpha, beta, counter))
                    if value >= beta:
                        flag = False
                    else:
                        alpha = max(value, alpha)
                    for node in nodes:
                        if node.node == originalMove and node.parent == parent and node.parentNumber == parentNumber:
                            if node.value < value:
                                node.value = value
                                node.alpha = alpha
                            Nodes.displayDetails(node)
    return value

#Draws the board state for a move of a player
def drawBoard(state, move, player):
    a = move.split(":");
    x, y= int(a[0]), int(a[1])
    stateToCheck = "X" if "O" == player.upper() else "O"
    currentState = "X" if "X" == player.upper() else "O"
    for a in (-1, 0, 1):
        for b in (-1, 0, 1):
            flag = True
            if 7>=x+a>=0 and 7>= y+b>=0 and stateToCheck == state[x + a][y + b] and (a!=0 or b!=0):
                tempX = a
                tempY = b
                intermediateState = deepcopy(state)
                isCorrect =False
                while (flag and 7 >= x + tempX >= 0 and 7 >= y + tempY >= 0):
                    m = tempX
                    n = tempY
                    while(7>=x+m>=0 and 7>=y+n>=0):
                        if ("*" == state[x + m][y + n]):
                            state = intermediateState
                            break
                        else:
                            if(currentState == state[x+m][y+n]):
                                isCorrect = True
                                break
                            else:
                                state[x+m][y+n] = currentState
                            flag = False
                        m +=a
                        n +=b
                    if(not isCorrect):
                        state = intermediateState
                    tempX += a
                    tempY += b
    if "X" == player.upper():
        state[x][y] = "X"
    else:
        state[x][y] = "O"
    return state

#Converts array position of a move to board position name
def convert(move):
    a = move.split(":");
    d = dict(enumerate(string.ascii_lowercase, 1))
    updatedMove = d[int(a[1])+1] + str(int(a[0])+1)
    return updatedMove

boardSize = 8
depth = 0
state = [["*" for x in range(boardSize)] for y in range(boardSize)]
f = open('input3.txt')
count = 1;
i=0;
for line in f:
    if 1 == count:
        for char in line:
            if ('\n' != char):
                player = char
    elif 2 == count:
        for char in line:
            if('\n' != char):
                depth = char
    else:
        j=0
        for char in line:
            if('\n' != char):
                state[i][j] = char
                j += 1
        i += 1
    count += 1
inputPlayer = player
opponentPlayer = 'O' if 'X' == player.upper() else 'X'
alpha = -float("inf")
beta =  float("inf")
isFinalLevelCheck = False
positionalWeight = [[99,-8,8,6,6,8,-8,99],
                    [-8, -24, -4, -3, -3, -4, -24, -8],
                    [8, -4, 7, 4, 4, 7, -4, 8],
                    [6, -3, 4, 0, 0, 4, -3, 6],
                    [6, -3, 4, 0, 0, 4, -3, 6],
                    [8, -4, 7, 4, 4, 7, -4, 8],
                    [-8, -24, -4, -3, -3, -4, -24, -8],
                    [99, -8, 8, 6, 6, 8, -8, 99]]
f = file("output.txt", "w")
f.truncate()
f = file("output1.txt", "w")
f.truncate()
maxValue(state,0,"root",None, player, 99, alpha, beta, counter)
for node in nodes:
    if node.node == "root":
        finalValue = node.value
    if node.parent == "root" and node.depth == 1 and node.value == finalValue:
        if(99 != node.move):
            state = drawBoard(state, node.move, player)
        printState(state)
        tempFile = file("output1.txt", "r")
        f = file("output.txt","a")
        f.write("\n")
        f.write("Node," + "Depth," + "Value," + "Alpha," + "Beta")
        f.write("\n")
        for line in tempFile:
            f.write(line)
        break