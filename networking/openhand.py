import sys
import numpy as np
import copy
import random
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
    print
    # updateWeights(state)
    # print(weights)
    # np.save('doubledummy_weights.npy', weights)
    #print "My reward was", state[-1]
    return

def findlegals(player, state):
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

def simulate(player, state, action):
    newstate = copy.deepcopy(state)

    #print(newstate.hands)
    newstate.hands[player].remove(action)
    newstate.roundseen.append(action)
    newstate.trickseen.append(action)
    
    # if trick is done, increment tricks
    if len(newstate.trickseen) == state.nplayers:
        # calc winner
        winning = newstate.trickseen[0]
        winner = abs(player-1)
        for c in range(1, len(newstate.trickseen)):
            card = newstate.trickseen[c]
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

        # if round is done, calc rewards
        if len(newstate.roundseen) == (state.nplayers * state.rounds):
            rw = 0
            tricks = newstate.tricks[0]
            bids = state.bids[0]
            if tricks == bids:
                if tricks == 0:
                    rw = 5
                else:
                    rw = tricks * 10
            elif tricks > bids:
                rw = tricks
            opprw = 0
            tricks = newstate.tricks[1]
            bids = state.bids[1]
            if tricks == bids:
                if tricks == 0:
                    opprw = 5
                else:
                    opprw = tricks * 10
            elif tricks > bids:
                opprw = tricks
            newstate.rewards = rw - opprw

    return newstate

def minimax(player, state):
    if state.hands[player] == []:
        return (None, state.rewards)
    actions = findlegals(player, state)
    if player == 0:
        bestAction = None
        bestVal = float("-inf")
        for a in actions:
            result = minimax(1, simulate(0, state, a))
            if result[1] > bestVal:
                bestAction = a
                bestVal = result[1]
        return (bestAction, bestVal)
    else:
        worstAction = None
        worstVal = float("inf")
        for a in actions:
            result = minimax(0, simulate(1, state, a))
            if result[1] < worstVal:
                worstAction = a
                worstVal = result[1]
        return (worstAction, worstVal)

def move(state):
    m =  minimax(0, state)
    print(m)
    return m[0]




    

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
