import sys
import numpy as np
import random
from multiprocessing.connection import Listener
addr = ('localhost', int(sys.argv[1]))
listener = Listener(addr)
conn = listener.accept()

import statemachine


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
    return float(rd)/2.

def rddone(state):
    #print "My reward was", state[-1]
    return

def move(state):
    legals = statemachine.findlegals(role, state)
    return random.choice(legals)


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
