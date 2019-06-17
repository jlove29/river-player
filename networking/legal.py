import sys
import numpy as np
import random
from multiprocessing.connection import Listener
addr = ('localhost', int(sys.argv[1]))
listener = Listener(addr)
conn = listener.accept()

import statemachine
import oracle


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

def bid(state):
    # for now, naive bidding
    '''
    trump = state[2]
    cards = state[3]
    count = 0
    for card in cards:
        if card[1] == trump:
            count += 1
    return count
    '''
    rd = state.rounds
    bid = float(rd)/2

    optimal = oracle.bidMinimax(state, float("-inf"), float("inf"))[0]
    global ideal_bids
    global total_bids
    total_bids += 1
    if optimal == bid:
        ideal_bids += 1

    return bid

def rddone(state):
    #print "My reward was", state[-1]
    return

def move(state):
    legals = statemachine.findlegals(role, state)
    move = random.choice(legals)

    optimal = oracle.minimax(state, float("-inf"), float("inf"))
    bestOutcome = oracle.minimax(oracle.simulate(state, move), float("-inf"), float("inf"))
    global ideal_moves
    global total_moves
    total_moves += 1
    if optimal[1] == bestOutcome[1]:
        ideal_moves += 1

    return move

ideal_bids = 0
total_bids = 0
ideal_moves = 0
total_moves = 0

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
        print("Optimal Bid Rate: " + str(float(ideal_bids)/total_bids))
        print("Optimal Move Rate: " + str(float(ideal_moves)/total_moves))
        break

conn.close()
