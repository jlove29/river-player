import sys
import numpy as np
import copy
import random
import collections
import operator
# import scipy.stats
from multiprocessing.connection import Listener
addr = ('localhost', int(sys.argv[1]))
listener = Listener(addr)
conn = listener.accept()

import statemachine as sm



def play(msg):
    action = msg[0]
    state = msg[1]
    if action == 'init':
        return init(state)
    if action == 'bid':
        return bid(state)
    if action == 'move':
        return move(state)
    if action == 'trickdone':
        return
    if action == 'rddone':
        return rddone(state)

def init(state):
    global role
    role = state.player
    global nplayers
    nplayers = state.nplayers

def featureExtractor(state):
    featureVector = np.zeros(NUM_FEATURES) 
    hand = state.hand
    oppBid = state.bids[abs(1 - role)]
    if oppBid < 0:
        featureVector[len(featureVector)-2] = 1
        oppBid = 0 #round(float(state.rounds) / nplayers)

    for card in hand:
        num = card[0]
        suit = card[1]
        if suit == state.trump:
            num += 13 # shift the number down to the trump side of the featureVector
        featureVector[num - 1] += 1

    featureVector[-1] = oppBid #last one is opponent's bid
    # print("Trump:" + str(state.trump))
    # print(hand)
    # print(featureVector)
    return featureVector

def bid(state):
    global featureVector

    featureVector = featureExtractor(state)
    bid = round(np.dot(featureVector, weights))

    return bid

def updateWeights(state):
    global weights
    curBid = round(np.dot(featureVector, weights))
    # loss = abs(rewards - curBid)
    print("Current Bid:", curBid)
    print("Tricks won:" + str(state.tricks))
    sign = np.sign(state.tricks - curBid)
    # print(sign)
    # print("rewards:")
    # print(state.tricks)
    weights = weights + featureVector * ETA * sign

def rddone(state):
    global solvedPositions
    solvedPositions = dict()
    # updateWeights(state)
    # print(weights)
    # np.save('doubledummy_weights.npy', weights)
    #print "My reward was", state[-1]
    print
    return

def remainingDeck(state):
    used = state.hand + state.roundseen + state.trickseen
    d = []
    for i in range(1, 13):
        for suit in ['Diamond', 'Heart', 'Club', 'Spade']:
            card = (i, suit)
            if card not in used:
                d.append(card)
    return d

def fakeHands(n, state):
    hands = []
    remaining = remainingDeck(state)
    numCards = len(state.hands[abs(role-1)])
    for _ in range(n):
        hands.append(random.sample(remaining, numCards))
    return hands

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
    global solvedPositions
    s = (state.player, str(state.hands), str(state.tricks)) #fake state for memoization
    if s in solvedPositions:
        return solvedPositions[s]
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
        solvedPositions[s] = (bestAction, bestVal)
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
        solvedPositions[s] = (worstAction, worstVal)
        return (worstAction, worstVal)

def move(state):
    global solvedPositions
    possHands = fakeHands(10, state)
    # print(possHands)
    fakeState = copy.deepcopy(state)
    actionsDict = collections.defaultdict(int)
    # possActions = []6
    for fh in possHands:
        # print
        fakeState.hands[abs(role-1)] = fh
        # print(fakeState.hands)
        # print(fakeState.trump)
        goodMove = minimax(fakeState, float("-inf"), float("inf"))[0]
        solvedPositions = dict()
        # print(goodMove)
        actionsDict[goodMove] += 1
        # possActions.append(minimax(state, float("-inf"), float("inf"))[0])
    # print(possActions)
    # print(actionsDict)
    m = max(actionsDict.iteritems(), key = operator.itemgetter(1))[0]
    # m = scipy.stats.mode(possActions)
    # print(m)
    return m




    

ETA = 0.01 #eta for the gradient descent 
NUM_FEATURES = 28 # number of features
try:
    weights = np.load('smartbidding_weights.npy')
except:
    weights = np.zeros(NUM_FEATURES) #weights for features
featureVector = np.zeros(NUM_FEATURES)
role = 0
nplayers = 0
state = None
solvedPositions = dict()
while True:
    msg = conn.recv()
    retval = play(msg)
    if retval is not None:
        conn.send(retval)
    if msg[0] == 'close':
        conn.close()
        #np.save('doubledummy_weights.npy', weights)
        break

conn.close()
