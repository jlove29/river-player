
def makelead(hand, trump):
    print ""
    print "Hand: " + str(hand)
    print "Trump: " + trump
    # ask for input
    move = input("Enter position of card (0-indexed): ")
    if move >= len(hand):
        print "Illegal position"
        return makelead(hand, trump)
    return hand[move]

def makemove(hand, trump, suit, seen):
    print ""
    print "Hand: " + str(hand)
    print "Trump: " + trump
    print "Leading Suit: " + suit
    print "Trick so far: " + str(seen)
    move = input("Enter position of card (0-indexed): ")
    if move >= len(hand):
        print "Illegal position"
        return makemove(hand, trump, suit, seen)
    return hand[move]

def makebid(hand, trump):
    print ""
    print "Hand: " + str(hand)
    print "Trump: " + trump
    bid = input("Enter bid: ")
    print ""
    return bid

def reporttrick(lastwinner, i):
    print ""
    if i == lastwinner:
        print "You won the trick\n"
    else:
        print "You lost the trick, player " + str(i) + " won\n"

def reportpoints(k):
    print "You got " + str(k) + " points that round"

def reporterror():
    print "Illegal move"
