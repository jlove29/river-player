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

def bid(state):
    # for now, naive bidding
    rd = state.rounds
    return np.ceil(float(rd)/float(nplayers))

def rddone(state):
    #print "My reward was", state[-1]
    return

def move(state):
    legals = sm.findlegals(role, state)
    bestaction = legals[0]
    bestscore = 0
    for action in legals:
        newstate = sm.simulate(role, state, action)
        reward = depthcharge(role, newstate)
        if reward > bestscore:
            bestscore = reward
            bestaction = action
    return action


def depthcharge(role, state):
    if state.rewards != 0:
        return max(0, state.rewards)
    
    opp = role + 1
    if opp == nplayers:
        opp = 0
    print ""
    print role
    print state.hand
    print state.trickseen
    legals = sm.findlegals(opp, state)
    action = random.choice(legals)
    newstate = sm.simulate(opp, state, action)
    return depthcharge(opp, newstate)


    


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
