
'''
Hands are represented as strings of length 2 (ex. 2H, 8D, JS, AC)
'''
from collections import Counter

class Game(object):
    def __init__(self, name1, name2, name3, stackSize, bb, numHands, timeBank):
        self.name1 = name1
        self.name2 = name2
        self.name3 = name3
        self.stackSize = stackSize
        self.bb = bb
        self.numHands = numHands

        self.hand = []


RANK_TO_IDX = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14,
}

SUIT_TO_IDX = {
    'c': 1,
    'd': 2,
    'h': 3,
    's': 4,
}

"""
NUM_HANDS = [
        num_singles,
        num_one_pair,
        num_two_pair,
        num_three,
        num_straight,
        num_flush,
        num_full_house,
        num_four,
        num_straight_flush
]
"""

NUM_HANDS = [
        1302540, 
        1098240, 
        123552, 
        54912, 
        10200, 
        5108, 
        3744, 
        624, 
        40,
]
TOTAL_NUM_HANDS = sum(NUM_HANDS) 

def score(hand, nleft):
    return hands_beat_rough(hand_rank(hand))
    rank = hand_rank(hand)

    return rank[0] + 3 * nleft

def hands_beat_rough(hand_rank):
    rough_rank = hand_rank[0]
    return sum(NUM_HANDS[:rough_rank]) 

'''
def hands_beat_fine(hand_rank):
    rough_rank = hand_rank[0]
    tie_breakers = hand_rank[1:]
    
    # calculate the number of hands within the rough rank
    # that our hand beats
    if rough_rank == 0: # high card
        h = max(tie_breakers)
        # doesn't include ties with same high card
        return h*(h-1)*(h-2)*(h-3)*(h-4) / math.factorial(5)
    if rough_rank == 1:
        h = tie_breakers[0]
        # doesn't include ties with the same pair
        return 
'''

def hand_rank(hand):
    ranks = card_ranks(hand)
    suits = card_suits(hand)

    if straight(ranks) and flush(suits):            # straight flush
        return (8, max(ranks))
    elif kind(4, ranks):                           # 4 of a kind
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):        # full house
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(suits):                              # flush
        return (5, ranks)
    elif straight(ranks):                          # straight
        return (4, max(ranks))
    elif kind(3, ranks):                           # 3 of a kind
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):                          # 2 pair
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):                           # kind
        return (1, kind(2, ranks), ranks)
    else:                                          # high card
        return (0, ranks)


def card_ranks(hand):
    return sorted((RANK_TO_IDX[r] for r, _ in hand), reverse=True)

def card_suits(hand):
    return sorted((SUIT_TO_IDX[s] for _, s in hand), reverse=True)


def straight(ranks):
    for x, y in zip(ranks, ranks[1:]):
        if x != y + 1:
            return False
    return True


def flush(suits):
    for x, y in zip(suits, suits[1:]):
        if x != y:
            return False
    return True


def kind(n, ranks):
    rank_count = Counter(ranks)
    for key, val in rank_count.iteritems():
        if val == rank_count:
            return key
    return False


def two_pair(ranks):
    rank_count = Counter(ranks)
    pairs = []
    for key, val in rank_count.iteritems():
        if val == 2:
            pairs.append(key)

    if len(pairs) == 2:
        return tuple(pairs)

