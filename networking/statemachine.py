import game
import random
import copy



def remainingDeck(used):
    d = []
    for i in range(1, 13):
        for suit in ['Diamond', 'Heart', 'Club', 'Spade']:
            card = (i, suit)
            if card not in used:
                d.append(card)
    return d



def findopplegals(role, state):
    legals = []
    used = state.hand + state.roundseen + state.trickseen
    d = remainingDeck(used)

    tosample = ((state.nplayers*state.rounds) - len(state.trickseen) + 1)/state.nplayers
    possiblehand = random.sample(d, tosample)

    fakestate = copy.deepcopy(state)
    fakestate.hand = possiblehand
    fakestate.player = role
    return findlegals(role, fakestate)



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
    newstate = copy.deepcopy(state)
    '''
    print "role", role
    print "action", action
    print "me", state.player
    print "myhand", state.hand
    print "round seen", state.roundseen
    print "trick seen", state.trickseen
    print "num rounds", state.rounds
    print "rewards", state.rewards
    print "tricks", state.tricks
    print "bids", state.bids
    print ""
    '''

    if role == state.player:
        newstate.hand.remove(action)
    newstate.roundseen.append(action)
    newstate.trickseen.append(action)
    
    # if trick is done, increment tricks
    if len(newstate.trickseen) == state.nplayers:
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

        newstate.tricks[winner] += 1
        newstate.trickseen = []

        # if round is done, calc rewards
        if len(newstate.roundseen) == (state.nplayers * state.rounds):
            rw = -1
            tricks = newstate.tricks[role]
            bids = state.bids[role]
            if tricks == bids:
                if tricks == 0:
                    rw = 5
                else:
                    rw = tricks * 10
            elif tricks > bids:
                rw = tricks
            newstate.rewards = rw

    '''
    print role
    print action
    print newstate.player
    print newstate.hand
    print newstate.roundseen
    print newstate.trickseen
    print newstate.rounds
    print newstate.rewards
    print ""
    '''
    return newstate


        



    



    #return newstate


