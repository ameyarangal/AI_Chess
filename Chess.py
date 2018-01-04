#!/usr/bin/python
import heapq
import time
import sys

# Abstraction:
# Intial State: Current board with player who is going to play nect move
# Terminal State: If opposite plyer kingfisher is captured or the search depth is reached
# Successors: List of all the valid states for all the pieces on the board for the current player.
# Evaluation function: Our evaluation function is based on difference of material score for current player and opposite player.
# We referred 'http://chessprogramming.wikispaces.com/Evaluation' to design the evaluation function.In this function,we assigned different weights
# to different pieces on the board depending on their importance in the game. So the final material score is the weight of piece and difference
# between the there numbers for current and opposite player.e.g.we assigned 200 weight to the difference between kingfisher of current player
# and its opponent on the board.We added these products of weight and differences between pieces to calculate the final material score.
# We also computed doubled parakeet and isolated parakeet which affect the current player in future. We substracted these parakeets
# as they are weak conditions for the current player.We also added mobility which calculates the legal moves of all pieces present on the board.
# Things we tried :
# 1.We tried to implement piece weight table in our evalution function.Piece weight table contains the weight of piece for all positions on board for a particular piece.
# When we add these tables to our evalution function, it was getting higher priority than Kingfisher.It was giving us a wrong result. Since we are unable to decide the weighing factor ,
# we removed theses tables from final implementaton.
# Design overview:
# To create successors for each state, we have appended all the valid moves for each piece on the board to a lis succ[]. To calculate all the valid moves,
# we have checked for each piece and its indexes to calculate its free moves and its capture move if possible. Then for every move in the free moves list
# we have swapped the piece and '.' and for the capture move we have placed the current players piece on opposite players position. to calculate free moves and
# capture moves for Blujay, Quetzel, and Kingfisher we have used a single function calculate moves as these pieces movement is incremented by 1 always
# For parakeet and nighthawk we have calculated capture moves in there respective function only.
# We have used playerweight for each player, if white then playerweight = 1 and black then playerweight = -1, this helped us generating the next move for any player
# by only one formula as the board is symmetric.
# We ahve assumed very high and low value for default alpha and beta values at the start of the program.
# We have used piecemovements dictionary to save the directions in which a particular piece can move. For ex, Robin can move in "up, down, right, left" directions
# Improvement we could do in our code: We could have have one for loop which iterate over indexes and and then switch on the piece function depending on the
# piece on that index. Currently as we have modular code for each piece movement, hence we couldn't integrate all valid moves in one single for loop iteration.
# We think this has impacted our timing slightly, but we have a more modular code.
# Algorithm:
# We have used minmax algorithm using alpha beta pruning. In minmax algorithm, we have used a max heap in the main fucntion to get the maximum alpha value for a state.
# At start we consider current player as Max player and opposite player as Min player, then we calculate max of all the beta which in turn are the minimum of alpha (recurrence).
# we start with depth 2 for search and give the output and if there is still time remaining from the permissible time limit then we increase the
# the depth by one and search again for better output. If the time limits exceeds while the code is in recurrence we check the time limit
# in recurrence and exits if exceeded.
# References:
# 1) 'http://chessprogramming.wikispaces.com/Evaluation'
# 2) Discussed with Aishwarya Dhage and Ninaad Joshi for the evaluation function.




piecemovements = {}
whitepieces = ['R','N','B','Q','K','P']
blackpieces = ['r','n','b','q','k','p']
piecemovements['Q'] = ["up", "down","left", "right","diagonalrightup","diagonalrightdown","diagonalleftup","diagonalleftdown"]
piecemovements['R'] = ["up","down","right","left"]
piecemovements['B'] = ["diagonalrightup","diagonalrightdown","diagonalleftup","diagonalleftdown"]
piecemovements['K'] = ["up","down","right","left","diagonalrightup","diagonalrightdown","diagonalleftup","diagonalleftdown"]
piecemovements['P'] = ["up"]
upmovements = ["up", "diagonalrightup", "diagonalleftup"]
downmovements = ["down", "diagonalrightdown", "diagonalleftdown"]
directions = ["diagonalrightup", "diagonalleftup", "diagonalrightdown", "diagonalleftdown"]
parakeettable = [0,  0,  0,  0,  0,  0,  0,  0, 5, 10, 10,-20,-20, 10, 10,  5,5, -5,-10,  0,  0,-10, -5,  5,0,  0,  0, 20, 20,  0,  0,  0,5,  5, 10, 25, 25, 10,  5,  5,10, 10, 20, 30, 30, 20, 10, 10,50, 50, 50, 50, 50, 50, 50, 50,0,  0,  0,  0,  0,  0,  0,  0]
knighttable = [-50,-40,-30,-30,-30,-30,-40,-50,-40,-20,  0,  5,  5,  0,-20,-40,-30,  5, 10, 15, 15, 10,  5,-30,-30,  0, 15, 20, 20, 15,  0,-30,-30,  5, 15, 20, 20, 15,  5,-30,-30,  0, 10, 15, 15, 10,  0,-30,-40,-20,  0,  0,  0,  0,-20,-40,-50,-40,-30,-30,-30,-30,-40,-50]
bluejaytable = [-20,-10,-10,-10,-10,-10,-10,-20,-10,  5,  0,  0,  0,  0,  5,-10,-10, 10, 10, 10, 10, 10, 10,-10,-10,  0, 10, 10, 10, 10,  0,-10,-10,  5,  5, 10, 10,  5,  5,-10,-10,  0,  5, 10, 10,  5,  0,-10,-10,  0,  0,  0,  0,  0,  0,-10,-20,-10,-10,-10,-10,-10,-10,-20]
robintable = [0,  0,  0,  5,  5,  0,  0,  0, -5,  0,  0,  0,  0,  0,  0, -5,-5,  0,  0,  0,  0,  0,  0, -5,-5,  0,  0,  0,  0,  0,  0, -5,-5,  0,  0,  0,  0,  0,  0, -5,-5,  0,  0,  0,  0,  0,  0, -5,5, 10, 10, 10, 10, 10, 10,  5,0,  0,  0,  0,  0,  0,  0,  0]
quetzeltable = [-20,-10,-10, -5, -5,-10,-10,-20, -10,  0,  5,  0,  0,  0,  0,-10,-10,  5,  5,  5,  5,  5,  0,-10,0,  0,  5,  5,  5,  5,  0, -5,-5,  0,  5,  5,  5,  5,  0, -5,-10,  0,  5,  5,  5,  5,  0,-10,-10,  0,  0,  0,  0,  0,  0,-10,-20,-10,-10, -5, -5,-10,-10,-20]
kingfishertable = [20, 30, 10,  0,  0, 10, 30, 20, 20, 20,  0,  0,  0,  0, 20, 20,-10,-20,-20,-20,-20,-20,-20,-10,-20,-30,-30,-40,-40,-30,-30,-20,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30]



def isNextPositionvalid(rowdiff, coldiff, direction):
    if direction == 'up' and rowdiff == 1:
        return True
    if direction == 'down' and rowdiff == 1:
        return True
    if direction == 'left' and coldiff == 1:
        return True
    if direction == 'right' and coldiff == 1:
        return True
    if direction in directions and coldiff == 1 and rowdiff == 1:
        return True
    return False

# returns freemoves list and capture move for a particular piece at a particular index.
def calculatemoves(state, playerweight, pieceindex, maximumpossiblemoves, piece, direction):
    capturingmove = -1
    freemoves = []

    for move in range(1,maximumpossiblemoves+1):
        if direction == "diagonalrightup":
            nextposition = pieceindex + (move * 8 + move) * playerweight
            previousposition = pieceindex + ((move-1) * 8 + (move-1)) * playerweight
        elif direction == "diagonalrightdown":
            nextposition = pieceindex - (move * 8 - move) * playerweight
            previousposition = pieceindex - ((move-1) * 8 - (move-1)) * playerweight
        elif direction == "diagonalleftup":
            nextposition = pieceindex + (move * 8 - move) * playerweight
            previousposition = pieceindex + ((move-1) * 8 - (move-1)) * playerweight
        elif direction == "diagonalleftdown":
            nextposition = pieceindex - (move * 8 + move) * playerweight
            previousposition = pieceindex - ((move-1) * 8 + (move-1)) * playerweight
        elif direction == "up":
            nextposition = pieceindex + move * playerweight * 8
            previousposition = pieceindex + (move-1) * playerweight * 8
        elif direction == "down":
            nextposition = pieceindex - move * playerweight * 8
            previousposition = pieceindex - (move-1) * playerweight * 8
        elif direction == "right":
            nextposition = pieceindex + move * playerweight
            previousposition = pieceindex + (move-1) * playerweight
        else:
            nextposition = pieceindex - move * playerweight
            previousposition = pieceindex - (move-1) * playerweight

        if 0 <= nextposition and nextposition <= 63:
            if playerweight == 1:
                nextrow = nextposition / 8
                nextcol = nextposition % 8
                previousrow = previousposition / 8
                previouscol = previousposition % 8
                rowdiff = abs(nextrow - previousrow)
                coldiff = abs(nextcol - previouscol)
                if not isNextPositionvalid(rowdiff, coldiff, direction):
                    return freemoves, capturingmove
                if state[nextposition] == '.':
                    freemoves.append(nextposition)
                elif state[nextposition] in whitepieces:
                    return freemoves, capturingmove
                elif state[nextposition] in blackpieces and piece != 'P':
                    capturingmove = nextposition
                    return freemoves, capturingmove
                elif state[nextposition] in blackpieces and piece == 'P':
                    return freemoves, capturingmove
            else:
                nextrow = nextposition / 8
                nextcol = nextposition % 8
                previousrow = previousposition / 8
                previouscol = previousposition % 8
                rowdiff = abs(nextrow - previousrow)
                coldiff = abs(nextcol - previouscol)
                if not isNextPositionvalid(rowdiff, coldiff, direction):
                    return freemoves, capturingmove
                if state[nextposition] == '.':
                    freemoves.append(nextposition)
                elif state[nextposition] in blackpieces:
                    return freemoves, capturingmove
                elif state[nextposition] in whitepieces and piece != 'P':
                    capturingmove = nextposition
                    return freemoves, capturingmove
                elif state[nextposition] in blackpieces and piece == 'P':
                    return freemoves, capturingmove
    return freemoves, capturingmove

# appends the capturing state in successor by replacing a piece with opponent piece
def capturePiece(state, pieceIndex, capturingPositionIndex, succ):
    statecopy = list(state)
    statecopy[capturingPositionIndex] = statecopy[pieceIndex]
    statecopy[pieceIndex] = '.'
    succ.append(statecopy)

# appends a state by swapping a piece with blank location.
def movePieceToFreeLocation(state, pieceIndex, freePositionIndex, succ):
    statecopy = list(state)
    statecopy[freePositionIndex], statecopy[pieceIndex] = statecopy[pieceIndex], statecopy[freePositionIndex]
    succ.append(statecopy)

# plays a white player nighthawk
def whitenighthawkMove(state, pieceIndex, nextposition, succ, allowedmoves):
    if state[nextposition] == '.':
        movePieceToFreeLocation(state, pieceIndex, nextposition, succ)
        allowedmoves.append(1)
    elif state[nextposition] not in whitepieces:
        capturePiece(state, pieceIndex, nextposition, succ)
        allowedmoves.append(1)

# plays a black player nighthawk
def blacknighthawkMove(state, pieceIndex, nextposition, succ, allowedmoves):
    if state[nextposition] == '.':
        movePieceToFreeLocation(state, pieceIndex, nextposition, succ)
        allowedmoves.append(1)
    elif state[nextposition] not in blackpieces:
        capturePiece(state, pieceIndex, nextposition, succ)
        allowedmoves.append(1)

# moves a nighthawk
def nighthawkMove(state, index, nextposition, succ, playerweight, allowedmoves):
    if playerweight == 1:
        whitenighthawkMove(state, index, nextposition, succ, allowedmoves)
    else:
        blacknighthawkMove(state, index, nextposition, succ, allowedmoves)

# returns mobility and piece score for all nighthawks in a given state
def validnighthawkMoves(succ, state, playerweight):
    mobility = 0
    score = 0
    allowedmoves = []
    occurences = state.count('N') if playerweight == 1 else state.count('n')
    if occurences > 0:
        indexes = []
        for i, letter in enumerate(state):
            if (playerweight == 1 and letter == 'N') or (playerweight == -1 and letter == 'n'):
                indexes.append(i)
        for index in indexes:
            score += knighttable[index] if playerweight == 1 else knighttable[63-index]
            row = index/8
            nextposition = (index + 16) + 1
            if abs(nextposition/8 - row) == 2 and 0 <= nextposition and nextposition <= 63:
                nighthawkMove(state, index, nextposition, succ, playerweight, allowedmoves)
            nextposition = (index + 16) - 1
            if abs(nextposition / 8 - row) == 2 and 0 <= nextposition and nextposition <= 63:
                nighthawkMove(state, index, nextposition, succ, playerweight, allowedmoves)
            nextposition = (index - 16) + 1
            if abs(row - nextposition / 8) == 2 and 0 <= nextposition and nextposition <= 63:
                nighthawkMove(state, index, nextposition, succ, playerweight, allowedmoves)
            nextposition = (index - 16) - 1
            if abs(row - nextposition / 8) == 2 and 0 <= nextposition and nextposition <= 63:
                nighthawkMove(state, index, nextposition, succ, playerweight, allowedmoves)
            nextposition = (index + 2) + 8
            if abs(nextposition / 8 - row) == 1 and 0 <= nextposition and nextposition <= 63:
                nighthawkMove(state, index, nextposition, succ, playerweight, allowedmoves)
            nextposition = (index + 2) - 8
            if abs(row - nextposition / 8) == 1 and 0 <= nextposition and nextposition <= 63:
                nighthawkMove(state, index, nextposition, succ, playerweight, allowedmoves)
            nextposition = (index - 2) + 8
            if abs(nextposition / 8 - row) == 1 and 0 <= nextposition and nextposition <= 63:
                nighthawkMove(state, index, nextposition, succ, playerweight, allowedmoves)
            nextposition = (index - 2) - 8
            if abs(row - nextposition / 8) == 1 and 0 <= nextposition and nextposition <= 63:
                nighthawkMove(state, index, nextposition, succ, playerweight, allowedmoves)
    return len(allowedmoves), score

# returns mobility and piece score for all parakeet in a given state
def validParakeetMoves(succ, state, playerweight):
    mobility = 0
    score = 0
    occurences = state.count('P') if playerweight == 1 else state.count('p')
    if occurences>0:
        indexes = []
        for i, letter in enumerate(state):
            if (playerweight == 1 and letter == 'P') or (playerweight == -1 and letter == 'p'):
                indexes.append(i)

        for index in indexes:
            row = index / 8
            col = index % 8
            startrow = 1 if playerweight == 1 else 6
            score += parakeettable[index] if playerweight == 1 else parakeettable[63 - index]
            if row == startrow:
                freemoves, capturemove = calculatemoves(state, playerweight, index, 2, 'P', "up")
            else:
                freemoves, capturemove = calculatemoves(state, playerweight, index, 1, 'P', "up")
            mobility += len(freemoves)
            for freemoveposition in freemoves:
                movePieceToFreeLocation(state, index,freemoveposition, succ)
            if capturemove != -1:
                capturePiece(state, index, capturemove, succ)

            if playerweight == 1:
                rightnextposition = index + 9
                leftnextposition = index + 7
                if col == 0 and state[rightnextposition] != '.' and state[rightnextposition] not in whitepieces:
                    capturePiece(state, index, index + 9, succ)
                    mobility += 1
                elif col == 7 and state[index + 7] != '.' and state[index + 7] not in whitepieces:
                    capturePiece(state, index, index + 7, succ)
                    mobility += 1
                elif col != 0 and col != 7 and state[index + 9] != '.' and state[index + 9] not in whitepieces:
                    capturePiece(state, index, index + 9, succ)
                    mobility += 1
                elif col != 0 and col != 7 and state[index + 7] != '.' and state[index + 7] not in whitepieces:
                    capturePiece(state, index, index + 7, succ)
                    mobility += 1
            elif playerweight == -1:
                if col == 7 and state[index - 9] != '.' and state[index - 9] not in blackpieces:
                    capturePiece(state, index, index - 9, succ)
                    mobility += 1
                elif col == 0 and state[index - 7] != '.' and state[index - 7] not in blackpieces:
                    capturePiece(state, index, index - 7, succ)
                    mobility += 1
                elif col != 0 and col != 7 and state[index - 9] != '.' and state[index - 9] not in blackpieces:
                    capturePiece(state, index, index - 9, succ)
                    mobility += 1
                elif col != 0 and col != 7 and state[index - 7] != '.' and state[index - 7] not in blackpieces:
                    capturePiece(state, index, index - 7, succ)
                    mobility += 1
    return mobility, score

# returns mobility and piece score for all robin in a given state
def validrobinMoves(succ, state, playerweight):
    mobility = 0
    score = 0
    occurences = state.count('R') if playerweight == 1 else state.count('r')
    if occurences > 0:
        indexes = []
        for i, letter in enumerate(state):
            if (playerweight == 1 and letter == 'R') or (playerweight == -1 and letter == 'r'):
                indexes.append(i)
        for index in indexes:
            score += robintable[index] if playerweight == 1 else robintable[63 - index]
            for movement in piecemovements['R']:
                freemoves, capturemove = calculatemoves(state, playerweight, index, 8, 'R', movement)
                mobility += len(freemoves)
                for freemoveposition in freemoves:
                    movePieceToFreeLocation(state, index,freemoveposition, succ)
                if capturemove != -1:
                    capturePiece(state, index, capturemove, succ)
                    mobility += 1
    return mobility, score

# returns mobility and piece score for all bluejay in a given state
def validBlueJayMoves(succ, state, playerweight):
    mobility = 0
    score = 0
    occurences = state.count('B') if playerweight == 1 else state.count('b')
    if occurences > 0:
        indexes = []
        for i, letter in enumerate(state):
            if (playerweight == 1 and letter == 'B') or (playerweight == -1 and letter == 'b'):
                indexes.append(i)
        for index in indexes:
            score += bluejaytable[index] if playerweight == 1 else bluejaytable[63 - index]
            for movement in piecemovements['B']:
                freemoves, capturemove = calculatemoves(state, playerweight, index, 8, 'B', movement)
                mobility += len(freemoves)
                for freemoveposition in freemoves:
                    movePieceToFreeLocation(state, index,freemoveposition, succ)
                if capturemove != -1:
                    capturePiece(state, index, capturemove, succ)
                    mobility += 1
    return mobility, score

# returns mobility and piece score for all quetzel in a given state
def validquetzelMoves(succ, state, playerweight):
    mobility = 0
    score = 0
    occurences = state.count('Q') if playerweight == 1 else state.count('q')
    if occurences > 0:
        indexes = []
        for i, letter in enumerate(state):
            if (playerweight == 1 and letter == 'Q') or (playerweight == -1 and letter == 'q'):
                indexes.append(i)
        for index in indexes:
            score += quetzeltable[index] if playerweight == 1 else quetzeltable[63 - index]
            for movement in piecemovements['Q']:
                freemoves, capturemove = calculatemoves(state, playerweight, index, 8, 'Q', movement)
                mobility += len(freemoves)
                for freemoveposition in freemoves:
                    movePieceToFreeLocation(state, index,freemoveposition, succ)
                if capturemove != -1:
                    capturePiece(state, index, capturemove, succ)
                    mobility += 1
    return mobility, score

# returns mobility and piece score for all kingfisher in a given state
def validkingfisherMoves(succ, state, playerweight):
    mobility = 0
    score = 0
    occurences = state.count('K') if playerweight == 1 else state.count('k')
    if occurences > 0:
        indexes = []
        for i, letter in enumerate(state):
            if (playerweight == 1 and letter == 'K') or (playerweight == -1 and letter == 'k'):
                indexes.append(i)
        for index in indexes:
            score += kingfishertable[index] if playerweight == 1 else kingfishertable[63 - index]
            for movement in piecemovements['K']:
                freemoves, capturemove = calculatemoves(state, playerweight, index, 1, 'K', movement)
                mobility += len(freemoves)
                for freemoveposition in freemoves:
                    movePieceToFreeLocation(state, index,freemoveposition, succ)
                if capturemove != -1:
                    capturePiece(state, index, capturemove, succ)
                    mobility += 1
    return mobility, score

def doubleParakeet(state, playerweight):
    parakeetdoubles = 0
    occurences = state.count('P') if playerweight == 1 else state.count('p')
    if occurences > 0:
        indexes = []
        for i, letter in enumerate(state):
            if (playerweight == 1 and letter == 'P') or (playerweight == -1 and letter == 'p'):
                indexes.append(i)
        for index in indexes:
            if indexes.__contains__(index+ playerweight * 8):
                parakeetdoubles += 1
    return parakeetdoubles

# returns a mobility and piece score for all piece in a state
def mobility(state, playerweight):
    succ1 = []
    parakeetmobility, parakeetscore = validParakeetMoves(succ1, state, playerweight)
    robinmobility, robinscore = validrobinMoves(succ1, state, playerweight)
    bluejaymobility, bluejayscore = validBlueJayMoves(succ1, state, playerweight)
    nighthawkmobility, nighthawkscore = validnighthawkMoves(succ1, state, playerweight)
    quetzelmobility, quetzelscore = validquetzelMoves(succ1, state, playerweight)
    kingfishermobility, kingfisherscore = validkingfisherMoves(succ1, state, playerweight)

    mobility = parakeetmobility + robinmobility + bluejaymobility + nighthawkmobility + quetzelmobility
    score = parakeetscore + robinscore + bluejayscore + nighthawkscore + quetzelscore + kingfisherscore

    return mobility, score

# returns number of robin files
def numberOfrobinOpenFile(state, playerweight):
    robinOpenfile = 0
    robinCloseFile = 0
    occurences = state.count('R') if playerweight == 1 else state.count('r')
    if occurences > 0:
        indexes = []
        for i, letter in enumerate(state):
            if (playerweight == 1 and letter == 'R') or (playerweight == -1 and letter == 'r'):
                indexes.append(i)
        for index in indexes:
            col = index % 8
            column = [state[col + j*8] for j in range(0, 7)]
            if column.count('.') == 7:
                robinOpenfile += 1
    return robinOpenfile

# returns number os isolated parakeets
def numberofisolatedparakeets(state, playerweight):
    isolatedparakeets = 0
    occurences = state.count('P') if playerweight == 1 else state.count('p')
    if occurences > 0:
        indexes = []
        for i, letter in enumerate(state):
            if (playerweight == 1 and letter == 'P') or (playerweight == -1 and letter == 'p'):
                indexes.append(i)
        for index in indexes:
            col = index %8
            nextcol = [state[j] for j in range(col+1,64, 8)]
            prevcol = [state[j] for j in range(col - 1, 64, 8)]
            if playerweight == 1:
                if not nextcol.__contains__('P') and not prevcol.__contains__('P'):
                    isolatedparakeets += 1
            elif not nextcol.__contains__('p') and not prevcol.__contains__('p'):
                isolatedparakeets += 1
    return isolatedparakeets

# returns the successor for a particular state
def successors(state, playerweight):
    succ = []
    validParakeetMoves(succ, state, playerweight)
    validrobinMoves(succ, state, playerweight)
    validBlueJayMoves(succ, state, playerweight)
    validnighthawkMoves(succ, state, playerweight)
    validquetzelMoves(succ, state, playerweight)
    validkingfisherMoves(succ, state, playerweight)
    return succ

# referred "http://chessprogramming.wikispaces.com/Evaluation" for evaluation function
# returns a int value for how promising the successor state is to win/loss/draw for the given player.
def evaluate(state, playerweight):
    promisevalue = 0
    promisevalue = 200 * (state.count('K') - state.count('k'))\
                    + 9 * (state.count('Q') - state.count('q'))\
                    + 5 * (state.count('R') - state.count('r'))\
                    + 3 * (state.count('B') - state.count('b'))\
                    + 1 * (state.count('P') - state.count('p'))
    promisevalue = promisevalue * playerweight
    playermobility, playerscore = mobility(state, playerweight)
    oppositeplayermobility, oppositeplayerscore = mobility(state, playerweight*-1)
    promisevalue = promisevalue + 0.1 * (playermobility - oppositeplayermobility)\
                    - 0.5 * (doubleParakeet(state, playerweight) - doubleParakeet(state, playerweight*-1)) \
                    - 0.5 * (numberofisolatedparakeets(state, playerweight) - numberofisolatedparakeets(state, playerweight*-1))\
                    + 1 * (numberOfrobinOpenFile(state, playerweight) - numberOfrobinOpenFile(state, playerweight*-1))
                    # + 0.01 * (playerscore - oppositeplayerscore)
    return promisevalue

# returns if the state is a terminal state
def isTerminalState(state, playerweight):
    if playerweight == 1:
        if state.count('k') == 0:
            return True
    else:
        if state.count('K') == 0:
            return True

# returns the max value for the state
def maxvalue(successor, alpha, beta, depthlevel, playerweight, depthlimit):
    depthlevel += 1
    if time.time() >= endtime - 1:
        sys.exit(0)
    if depthlevel == depthlimit or isTerminalState(successor, playerweight):
        return evaluate(successor, playerweight)
    else:
        minsuccessors = successors(successor, playerweight)
        for minsucc in minsuccessors:
            alpha = max(alpha, minvalue(minsucc, alpha, beta, depthlevel, playerweight, depthlimit))
            if alpha >= beta:
                return alpha
    return alpha

# returns the min value for the state
def minvalue(successor, alpha, beta, depthlevel, playerweight, depthlimit):
    depthlevel += 1
    if time.time() >= endtime - 1:
        sys.exit(0)
    if depthlevel == depthlimit or isTerminalState(successor, playerweight):
        return evaluate(successor, playerweight)
    else:
        oppositeplayer = -1 * playerweight
        maxsuccessors = successors(successor, oppositeplayer)
        for maxsucc in maxsuccessors:
            beta = min(beta, maxvalue(maxsucc, alpha, beta, depthlevel, playerweight, depthlimit))
            if alpha >= beta:
                return beta
        return beta

# solve using alpha beta pruning
def AlphaBetaDecision(state, playerweight, depthlimit):
    succ = successors(state, playerweight)
    defaultBetaValue = 100000000
    defaultAlphaValue = -10000000
    betavaluemaxheap = []
    for minsucc in succ:
        heapq.heappush(betavaluemaxheap, (minvalue(minsucc, defaultAlphaValue, defaultBetaValue, 0, playerweight, depthlimit)*-1, minsucc))
    return heapq.heappop(betavaluemaxheap)[1]

player = sys.argv[1]
state = sys.argv[2]
timelimit = sys.argv[3]
state = list(state)

starttime = time.time()
endtime = time.time() + float(timelimit)
depthlimit = 2
while(1):
    playerweight = 1 if player == 'w' else -1
    optimized = AlphaBetaDecision(state, playerweight, depthlimit)
    print "{0}".format(''.join(optimized))
    depthlimit += 1
