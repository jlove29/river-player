import numpy as np



class GameState():
    def __init__(self, player, trick, tricks, rewards=0, scores=[]):
        self.player = player
        self.tricks = tricks
        self.rewards = rewards
        self.scores = scores
        if type(trick) == list:
            self.rounds = trick[0]
            self.trump = trick[1]
            self.hand = trick[2]
            self.roundseen = trick[3]
            self.trickseen = trick[4]
            self.bids = trick[5]
            self.nplayers = trick[6]
            self.hands = trick[7]
        elif trick is not None:
            self.rounds = trick.parent.height
            self.trump = trick.trump
            self.hand = trick.parent.getHand(player)
            self.roundseen = trick.parent.seen
            self.trickseen = trick.seen
            self.bids = trick.parent.bids
            self.nplayers = trick.parent.parent.nplayers
            self.hands = trick.parent.hands

