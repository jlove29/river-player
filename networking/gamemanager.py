import numpy as np
from game import Game
import random
from state import GameState
from multiprocessing.connection import Client


nplayers = 2
maxh = 6
minh = 1

conn1 = Client(('localhost', 7000))
conn2 = Client(('localhost', 7001))
conns = [conn1, conn2]



def send(playernum, action, state):
    conn = conns[playernum]
    conn.send([action, state])

def sendrcv(playernum, action, state):
    send(playernum, action, state)
    response = conns[playernum].recv()
    return response

def playround(rd):
    #print "ROUND " + str(rd) 
    # create a new round
    r = game.newRound(rd)
    r.deal()
    trump = r.trump
    tricks = np.zeros(nplayers)
    bids = np.array([-1 for _ in range(nplayers)])

    for k in range(nplayers):
        initialstate = GameState(k, [rd, trump, [], [], [], bids, nplayers, []], tricks)
        send(k, 'init', initialstate)

    # bid
    for j in range(playround.startplayer, playround.startplayer + nplayers):
        pnum = j % nplayers
        newstate = GameState(pnum, [rd, trump, r.getHand(pnum), [], [], bids, nplayers, r.hands], tricks)
        bid = sendrcv(pnum, 'bid', newstate)
        bids[pnum] = bid
        r.bid(pnum, bid)

    lastwinner = playround.startplayer

    # play
    for card in range(rd):
        # create tricks
        trick = r.newTrick(lastwinner)
        hand = r.getHand(lastwinner)
        while True:
            newstate = GameState(lastwinner, trick, tricks)
            lead = sendrcv(lastwinner, 'move', newstate)
            x = trick.lead(lead)
            if x >= 0:
                break
        suit = trick.suit

        for i in range(1, nplayers):
            p = (lastwinner + i) % nplayers
            hand = r.getHand(p)
            newstate = GameState(p, trick, tricks)
            while True:
                play = sendrcv(p, 'move', newstate)
                x = trick.play(play, p)
                if x >= 0:
                    break

        lastwinner = trick.currentWinner
        tricks[lastwinner] += 1

        # report to players
        for i in range(0, nplayers):
            newstate = GameState(i, trick, tricks)
            send(i, 'trickdone', newstate)

    '''
    print "round", rd
    print "tricks", tricks
    print "bids", bids
    print ""
    '''
    # assign points
    #print tricks
    for k in range(nplayers):
        if tricks[k] == bids[k]:
            if tricks[k] == 0:
                points[k] += 5
                # newstate = GameState(k, None, 5)
                # send(k, 'rddone', newstate)
            else:
                points[k] += tricks[k] * 10
                # newstate = GameState(k, None, tricks[k] * 10)
                # send(k, 'rddone', newstate)
        elif tricks[k] > bids[k]:
            points[k] += tricks[k]
            # newstate = GameState(k, None, tricks[k])
            # send(k, 'rddone', newstate)
        else:
            pass
            # newstate = GameState(k, None, 0)
            # send(k, 'rddone', newstate)

    for k in range(nplayers):
        newstate = GameState(k, None, tricks[k], scores=points)
        # print(tricks[k])
        send(k, 'rddone', newstate)
        

    #print points
    #print "\n"
    playround.startplayer = (playround.startplayer + 1) % nplayers

playround.startplayer = 0



game = 0
def go():
    # create a new game
    global game
    game = Game(nplayers, maxh, minh)
    global points
    points = np.zeros(nplayers)
    # up the river
    for rd in range(minh, maxh+1):
        playround(rd)
        random.shuffle(game.deck)
    # down the river
    for rd in range(maxh-1, minh-1, -1):
        playround(rd)
        random.shuffle(game.deck)


    #print "Final Score:"
    print points
    return points


totalpoints = np.zeros(nplayers)
n = 1
p1wins = 0
for i in range(n):
    points = go()
    for i in range(len(points)):
        totalpoints[i] += (float(points[i])/n)
    if points[0] > points[1]:
            p1wins += 1.0/n
# close connections
for p in range(nplayers):
    send(p, 'close', None)

print p1wins
print totalpoints
