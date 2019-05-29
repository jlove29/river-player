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

def bid(state):
    # for now, naive bidding
    rd = state.rounds
    return np.ceil(float(rd)/float(nplayers))

def rddone(state):
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
