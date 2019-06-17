import sys
import numpy as np
import copy
import random

role = 0

def bidMinimax(state, alpha, beta):
    player = state.player
    if state.hands[player] == []:
        bestBid = 0
        bestScore = float("-inf")
        if state.bids[abs(role-1)] == -1:
            for mybid in range(state.rounds+1):
                worstScore = float("inf")
                for oppbid in range(state.rounds+1):
                    bids = [None, None]
                    bids[role] = mybid
                    bids[abs(role-1)] = oppbid
                    worstScore = scoreDiff(state.tricks, bids)
                if worstScore > bestScore:
                    bestBid = mybid
                    bestScore = worstScore
        else:
            for mybid in range(state.rounds+1):
                bids = list(state.bids)
                bids[role] = mybid
                score = scoreDiff(state.tricks, bids)
                if  score > bestScore:
                    bestBid = mybid
                    bestScore = score
        return (bestBid, bestScore)

    actions = findlegals(state)
    if player == role:
        bestBid = None
        bestVal = float("-inf")
        for a in actions:
            result = bidMinimax(simulate(state, a), alpha, beta)
            if result[1] >= beta:
                return (None, result[1])
            if result[1] > alpha:
                alpha = result[1]
            if result[1] > bestVal:
                bestAction = result[0]
                bestVal = result[1]
        return (bestAction, bestVal)
    else:
        worstAction = None
        worstVal = float("inf")
        for a in actions:
            result = bidMinimax(simulate(state, a), alpha, beta)
            if result[1] <= alpha:
                return (None, result[1])
            if result[1] < beta:
                beta = result[1]
            if result[1] < worstVal:
                worstAction = result[0]
                worstVal = result[1]
        return (worstAction, worstVal)

def scoreDiff(tricks, bids):
    rw = 0
    mytricks = tricks[role]
    mybid = bids[role]
    if mytricks == mybid:
        if mytricks == 0:
            rw = 5
        else:
            rw = mytricks * 10
    elif mytricks > mybid:
        rw = mytricks
    opprw = 0
    opptricks = tricks[abs(role-1)]
    oppbid = bids[abs(role-1)]
    if opptricks == oppbid:
        if opptricks == 0:
            opprw = 5
        else:
            opprw = opptricks * 10
    elif opptricks > oppbid:
        opprw = opptricks
    return rw - opprw

def findlegals(state):
    player = state.player
    legals = []
    rd = state.rounds
    cards = state.hands[player]
    trick = state.trickseen
    # make leading move
    if trick == []:
        return cards

    lead = trick[0][1]
    for card in cards:
        if card[1] == lead:
            legals.append(card)
    if len(legals) > 0:
        return legals
    return cards

def simulate(state, action):
    newstate = copy.deepcopy(state)

    # print(newstate.hands)
    player = state.player
    newstate.hands[player].remove(action)
    newstate.roundseen.append(action)
    newstate.trickseen.append(action)
    
    # if trick is done, increment tricks
    if len(newstate.trickseen) == state.nplayers:
        # calc winner
        winning = newstate.trickseen[0]
        winner = abs(player-1)

        card = newstate.trickseen[1]
        if winning[1] == state.trump:
            if card[1] == state.trump and card[0] > winning[0]:
                winning = card
                winner = player
        else:
            if card[1] == state.trump:
                winning = card
                winner = player
            elif card[1] == winning[1] and card[0] > winning[0]:
                winning = card
                winner = player

        newstate.tricks[winner] += 1
        newstate.trickseen = []
        newstate.player = winner

        # if round is done, calc rewards
        if len(newstate.roundseen) == (state.nplayers * state.rounds):
            newstate.rewards = scoreDiff(newstate.tricks, state.bids)
    else:
        newstate.player = abs(player-1)

    return newstate

def minimax(state, alpha, beta):
    player = state.player
    if state.hands[player] == []:
        return (None, state.rewards)
    minPossible = float("inf")
    maxPossible = float("-inf")
    for w in range(len(state.hands[player])+1):
        l = len(state.hands[player]) - w
        possTricks = list(state.tricks)
        possTricks[role] += w
        possTricks[abs(role-1)] += l
        diff = scoreDiff(possTricks, state.bids)
        minPossible = min(minPossible, diff)
        maxPossible = max(maxPossible, diff)
    actions = findlegals(state)
    if player == role:
        bestAction = None
        bestVal = float("-inf")
        for a in actions:
            result = minimax(simulate(state, a), alpha, beta)[1]
            if result >= beta:
                return (None, result)
            if result > alpha:
                alpha = result
            if result > bestVal:
                bestAction = a
                bestVal = result
                if result == maxPossible:
                    break
        return (bestAction, bestVal)
    else:
        worstAction = None
        worstVal = float("inf")
        for a in actions:
            result = minimax(simulate(state, a), alpha, beta)[1]
            if result <= alpha:
                return (None, result)
            if result < beta:
                beta = result
            if result < worstVal:
                worstAction = a
                worstVal = result
                if result == minPossible:
                    break
        return (worstAction, worstVal)