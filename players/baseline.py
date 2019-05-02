
def makelead(hand, trump):
    for card in hand:
        if card[1] != trump:
            print "player leads with " + str(card)
            return card
    print "player leads with " + str(hand[0])
    return hand[0]

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

def makebid(hand, trump):
    total = 0
    for card in hand:
        if card[1] == trump:
            total += 1
    print "player bids " + str(total)
    return total

def reporttrick(lastwinner, i):
    pass

def reportpoints(k):
    pass
