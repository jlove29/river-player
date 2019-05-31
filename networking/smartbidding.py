import sys
import numpy as np
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
    # for now, naive bidding
    featureExtractor(state)
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
    updateWeights(state)
    print(weights)
    #print "My reward was", state[-1]
    return

def move(state):
    trump = state.trump
    trick = state.trickseen
    legals = sm.findlegals(role, state)
    maxcard = legals[0]
    if len(trick) == 0 or maxcard[1] == trick[0][1]:
        for card in legals:
            if card[0] > maxcard[0]:
                maxcard = card
        return maxcard
    for card in legals:
        if card[1] == trump:
            if maxcard[1] == trump:
                if card[0] < maxcard[0]:
                    maxcard = card
            else:
                maxcard = card
        else:
            if card[0] < maxcard[0]:
                maxcard = card
    return maxcard

ETA = 0.01 #eta for the gradient descent 
NUM_FEATURES = 28 # number of features
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
        break

conn.close()
