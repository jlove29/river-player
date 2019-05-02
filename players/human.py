
def makelead(hand, trump):
    print "Hand: " + str(hand)
    print "Trump: " + trump
    # ask for input
    move = input("Enter position of card (0-indexed): ")
    return hand[move]

def makemove(hand, trump, suit, seen):
    print "Hand: " + str(hand)
    print "Trump: " + trump
    print "Leading Suit: " + suit
    print "Trick so far: " + str(seen)
    move = input("Enter position of card (0-indexed): ")
    return hand[move]

def makebid(hand, trump):
    print "Hand: " + str(hand)
    print "Trump: " + trump
    bid = input("Enter bid: ")
    return bid

def reporttrick(lastwinner, i):
    if i == lastwinner:
        print "you win"
    else:
        print "you lose, player " + str(i) + " won"

def reportpoints(k):
    print "you got " + str(k) + " points from that round"
