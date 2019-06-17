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
        return trickdone(state)
    if action == 'rddone':
        return rddone(state)

def init(state):
    global role
    role = state.player
    global nplayers
    nplayers = state.nplayers

def bid(state):
    print ""
    if state.bids[abs(role-1)] >= 0:
        print "Opponent's Bid: " + str(state.bids[abs(role-1)]) 
    print "Hand: " + str(state.hand)
    print "Trump: " + state.trump
    bid = input("Enter bid: ")
    print ""
    return bid

def trickdone(state):
    print ""
    print "Previous Trick: " + str(state.trickseen)
    print "Tricks Won: " + str(state.tricks)
    return


def rddone(state):
    print ""
    print "Round done"
    print "Current scores: " + str(state.scores)
    return

def makemove(hand, trump, seen, bids):
    print ""
    print "Bids: " + str(bids)
    print "Hand: " + str(hand)
    print "Trump: " + trump
    print "Trick so far: " + str(seen)
    move = input("Enter position of card (0-indexed): ")
    if move >= len(hand):
        print "Illegal position"
        return makemove(hand, trump, seen, bids)
    return hand[move]

def move(state):
    hand = state.hand
    trump = state.trump
    trick = state.trickseen
    bids = state.bids
    legals = sm.findlegals(role, state)
    move = makemove(hand, trump, trick, bids)
    while move not in legals:
        print "Illegal move"
        move = makemove(hand, trump, trick, bids)
    return move


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
