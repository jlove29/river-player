import itertools, random
import numpy as np


'''
State information:
    number of cards in round
    trump suit
    cards in hand
    cards seen
    number of tricks won by each player
'''



class Trick():
    def __init__(self, leader, trump, parent):
        self.parent = parent
        self.seen = []
        self.trump = trump
        self.currentBest = 0
        self.currentWinner = leader
        self.leader = leader
    def lead(self, card):
        # if card[1] == self.trump:
        #     for c in self.parent.hands[self.leader]:
        #         if c[1] != self.trump:
        #             return -1
        self.seen.append(card)
        self.suit = card[1]
        if card[1] == self.trump:
            self.currentBest = card[0] + 100
        else:
            self.currentBest = card[0]
        self.parent.decrementHand(self.leader, card)
        return 0
    def play(self, card, player):
        if card[1] != self.suit:
            for c in self.parent.hands[player]:
                if c[1] == self.suit:
                    return -1
        self.seen.append(card)
        value = card[0]
        if card[1] == self.trump:
            value += 100
        elif card[1] != self.suit:
            value = 0
        if value > self.currentBest:
            self.currentBest = value
            self.currentWinner = player
        self.parent.decrementHand(player, card)
        return 0



class Round():
    def __init__(self, nplayers, height, deck, parent):
        self.parent = parent
        self.hands = []
        self.bids = np.zeros(nplayers, dtype=int)
        self.nplayers = nplayers
        self.deck = deck
        self.trump = self.deck[0][1]
        self.deck = self.deck[1:]
        self.height = height
    def deal(self):
        for p in range(self.nplayers):
            self.hands.append(self.deck[:self.height])
            self.deck = self.deck[self.height:]
        return self.hands
    def bid(self, player, amt):
        self.bids[player] = amt
    def newTrick(self, leader):
        self.currentTrick = Trick(leader, self.trump, self)
        return self.currentTrick
    def decrementHand(self, player, card):
        self.hands[player].remove(card)
    def getHand(self, player):
        return self.hands[player]


class Game():
    def __init__(self, nplayers, maxh, minh):
        self.deck = list(itertools.product(range(1,14),['Spade','Heart','Diamond','Club']))
        random.shuffle(self.deck)
        self.nplayers = nplayers
        self.maxh = maxh
        self.minh = minh
    def newRound(self, height):
        self.currentRound = Round(self.nplayers, height, self.deck, self)
        return self.currentRound
