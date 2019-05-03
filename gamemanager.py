import numpy as np
from game import Game
import players.baseline as baseline
import players.human as human
import random




nplayers = 2
maxh = 7
minh = 1

players = [baseline, human]

def playround(rd):
    print "ROUND " + str(rd) 
    # create a new round
    r = game.newRound(rd)
    r.deal()
    trump = r.trump

    # bid
    bids = np.zeros(nplayers)
    for j in range(playround.startplayer, playround.startplayer + nplayers):
        hand = r.getHand(j % nplayers)
        bids[j % nplayers] = players[j % nplayers].makebid(hand, trump)

    lastwinner = playround.startplayer
    tricks = np.zeros(nplayers)

    # play
    for card in range(rd):
        # create tricks
        trick = r.newTrick(lastwinner)
        hand = r.getHand(lastwinner)
        while True:
            x = trick.lead(players[lastwinner].makelead(hand, trump))
            if x < 0:
                players[lastwinner].reporterror()
            else:
                break
        suit = trick.suit

        for i in range(1, nplayers):
            p = (lastwinner + i) % nplayers
            hand = r.getHand(p)
            while True:
                x = trick.play(players[p].makemove(hand, trump, suit, trick.seen), p)
                if x < 0:
                    players[p].reporterror()
                else:
                    break

        lastwinner = trick.currentWinner
        tricks[lastwinner] += 1

        # report to players
        for i in range(0, nplayers):
            players[i].reporttrick(lastwinner, i)

    # assign points
    for k in range(nplayers):
        if tricks[k] == bids[k]:
            if tricks[k] == 0:
                points[k] += 5
                players[k].reportpoints(5)
            else:
                points[k] += tricks[k] * 10
                players[k].reportpoints(tricks[k] * 10)
        elif tricks[k] > bids[k]:
            points[k] += tricks[k]
            players[k].reportpoints(tricks[k])
        else:
            players[k].reportpoints(0)
    print points
    print "\n"
    playround.startplayer = (playround.startplayer + 1) % nplayers
playround.startplayer = 0





# create a new game
game = Game(nplayers, maxh, minh)
points = np.zeros(nplayers)
# up the river
for rd in range(minh, maxh+1):
    playround(rd)
    random.shuffle(game.deck)
# down the river
for rd in range(maxh-1, minh-1, -1):
    playround(rd)
    random.shuffle(game.deck)
print "Final Score:"
print points

