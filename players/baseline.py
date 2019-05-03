
# Leads with first non-trump card in hand
# if all trump cards, leads with first card in hand
def makelead(hand, trump):
    for card in hand:
        if card[1] != trump:
            print "Player leads with " + str(card)
            return card
    print "Player leads with " + str(hand[0])
    return hand[0]

# plays highest suit-matching card in hand
# if none, plays lowest trump card
# if none, plays first card
def makemove(hand, trump, suit, seen):
    bestoption = list(hand[0])
    bestoption[0] = 0
    
    worsttrump = list(hand[0])
    worsttrump[0] = 20

    for card in hand:
        if card[1] == suit:
            if card[0] > bestoption[0]:
                bestoption = list(card)
        elif card[1] == trump:
            if card[0] < worsttrump[0]:
                worsttrump = list(card)
    if bestoption[0] > 0:
        print "player plays " + str(bestoption)
        return tuple(bestoption)
    if worsttrump[0] < 20:
        print "player plays " + str(worsttrump)
        return tuple(worsttrump)
    print "player plays " + str(hand[0])
    return hand[0]

# bids with number of trump cards in hand
def makebid(hand, trump):
    total = 0
    for card in hand:
        if card[1] == trump:
            total += 1
    print "Player bids " + str(total)
    return total

# does not take info on tricks
def reporttrick(lastwinner, i):
    pass

# does not take info on round rewards
def reportpoints(k):
    pass

# does not report errors (it does not make errors)
def reporterror():
    pass
