import time
import GameEngine as Engine
from Const import *

turnStartTime = time.time()
bestMoveMatrix = [[]]

def getNextMoveMinMax(matrix, depth, playerOnMove):
    global turnStartTime
    global bestMoveMatrix
    turnStartTime = time.time()
    bestMoveMatrix = [[]]

    if AI_TURN == 1:
        bestMoveValue = -float("inf")
    elif AI_TURN == 2:
        bestMoveValue = +float("inf")
    
    availableMovesMatrices = Engine.getAvailableMovesMatrices(matrix, playerOnMove)
    newCount = len(availableMovesMatrices)
    if newCount > PRUNING_THRESHOLD:
        availableMovesMatrices = Engine.sortAndPruneMatricesByBoardState(availableMovesMatrices, playerOnMove)
        newCount = len(availableMovesMatrices)
    
    count = len(availableMovesMatrices)
    print("available moves left :", count)
    print("search depth:", depth)
    for moveMatrix in availableMovesMatrices:

        #time restriction
        currentTurnTime = time.time()
        if currentTurnTime-turnStartTime >= TIME_LIMIT_SECONDS:
            return Engine.get_last_move(bestMoveMatrix)

        val = min_maxWithAlphaBeta(moveMatrix, depth, ALPHA_START, BETA_START, Engine.getNextPlayer(playerOnMove), count)
        print("val is : " , val)
        if AI_TURN == 1:
            if val > bestMoveValue:
                bestMoveValue = val
                bestMoveMatrix = moveMatrix
                print("picked :" , bestMoveValue)
                if bestMoveValue == P1_WIN_VALUE:
                    return Engine.get_last_move(bestMoveMatrix)

        elif AI_TURN == 2:
            if val < bestMoveValue:
                bestMoveValue = val
                bestMoveMatrix = moveMatrix
                print("picked :" , bestMoveValue)
                if bestMoveValue == P2_WIN_VALUE:
                    return Engine.get_last_move(bestMoveMatrix)
    return Engine.get_last_move(bestMoveMatrix)

transposition_table = {}
def min_maxWithAlphaBeta(matrix, depth, alpha, beta, playerOnMove, count):
    # Check if the position is in the transposition table
    key = str(matrix)
    if key in transposition_table:
        return transposition_table[key]

    if count == 1 or depth == 0:
        return Engine.getBoardStateOptimized(matrix, playerOnMove)

    availableMovesMatrices = Engine.getAvailableMovesMatrices(matrix, playerOnMove)
    newCount = len(availableMovesMatrices)
    if newCount > PRUNING_THRESHOLD:
        availableMovesMatrices = Engine.sortAndPruneMatricesByBoardState(availableMovesMatrices, playerOnMove)
        newCount = len(availableMovesMatrices)

    if playerOnMove == 1:
        max_val = -float("inf")
        for moveMatrix in availableMovesMatrices:
            val = min_maxWithAlphaBeta(moveMatrix, depth - 1, alpha, beta, Engine.getNextPlayer(playerOnMove), newCount)
            max_val = max(max_val, val)
            alpha = max(alpha, val)
            if beta <= alpha:
                break
        transposition_table[key] = max_val
        return max_val

    else:
        min_val = float("inf")
        for moveMatrix in availableMovesMatrices:
            val = min_maxWithAlphaBeta(moveMatrix, depth - 1, alpha, beta, Engine.getNextPlayer(playerOnMove), newCount)
            min_val = min(min_val, val)
            beta = min(beta, val)
            if beta <= alpha:
                break
        transposition_table[key] = min_val
        return min_val