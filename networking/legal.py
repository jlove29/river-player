import sys
from multiprocessing.connection import Listener
addr = ('localhost', int(sys.argv[1]))
listener = Listener(addr)
conn = listener.accept()

import statemachine


def play(state):
    action = state[0]
    if action == 'init':
        return init(state[1:])
    if action == 'bid':
        return bid(state[1:])
    if action == 'move':
        return move(state[1:])
    if action == 'trickdone':
        return
    if action == 'rddone':
        return rddone(state[1:])

def init(state):
    global role
    role = state[0]

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
    rd = state[1]
    return float(rd)/2.

def rddone(state):
    #print "My reward was", state[-1]
    return

def move(state):
    legals = statemachine.findlegals(role, state)
    return legals[0]


role = 0
state = None
while True:
    state = conn.recv()
    retval = play(state)
    if retval is not None:
        conn.send(retval)
    if state[0] == 'close':
        conn.close()
        break

conn.close()
