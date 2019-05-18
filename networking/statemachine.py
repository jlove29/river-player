import game
import random
import copy



def remainingDeck(state):
    d = []
    for i in range(13):
        for suit in ['Diamonds', 'Hearts', 'Clubs', 'Spades']:
            card = (i, suit)
            if card not in state.hand or state.roundseen or state.trickseen:
                d.append(card)
    return d



def findopplegals(role, state):
    legals = []
    cards = state.hand
    seen = state.roundseen
    trick = state.trickseen

    d = remainingDeck(state)
    possiblehand = random.sample(d, len(cards))

    fakestate = copy.deepcopy(state)
    fakestate.hand = possiblehand
    return findlegals(state.player, fakestate)



def findlegals(role, state):
    if role != state.player:
        return findopplegals(role, state)

    legals = []
    rd = state.rounds
    cards = state.hand
    trick = state.trickseen
    # make leading move
    if trick == []:
        return cards

    lead = trick[0][1]
    for card in cards:
        if card[1] == lead:
            legals.append(card)
    if len(legals) > 0:
        return legals
    return cards

def simulate(role, state, action):
    print ""
    print "SIMULATING"
    print "role", role
    print "hand", state.hand
    print "action", action
    print "trickseen", state.trickseen
    newstate = copy.deepcopy(state)

    if role == state.player:
        newstate.hand.remove(action)
    newstate.roundseen.append(action)
    newstate.trickseen.append(action)
    
    print "newhand", newstate.hand
    print "newseen", newstate.trickseen

    # if trick is done, increment tricks
    if len(newstate.trickseen) == state.nplayers:
        print "trick is now done"
        # calc winner
        winning = newstate.trickseen[0]
        winner = 0
        for c in range(1, len(newstate.trickseen)):
            card = newstate.trickseen[c]
            if winning[1] == state.trump:
                if card[1] == state.trump and card[0] > winning[0]:
                    winning = card
                    winner = c
            else:
                if card[1] == state.trump:
                    winning = card
                    winner = c
                elif card[1] == winning[1] and card[0] > winning[0]:
                    winning = card
                    winner = c
        print "winning card", winning
        print "winner", winner

        newstate.tricks[winner] += 1
        newstate.trickseen = []
        print "old tricks", state.tricks
        print "new tricks", newstate.tricks

        # if round is done, calc rewards
        if len(newstate.roundseen) == (state.nplayers * state.rounds):
            print "round done"
            rw = -1
            tricks = newstate.tricks[role]
            bids = state.bids[role]
            print "tricks won", tricks
            print "bids", bids
            if tricks == bids:
                if tricks == 0:
                    rw = 5
                else:
                    rw = tricks * 10
            elif tricks > bids:
                rw = tricks
            newstate.rewards = rw
            print "old rewards", state.rewards
            print "new rewards", newstate.rewards

    return newstate


        



    



    #return newstate


