from array import array
from random import sample
from time import time

Data = array('I')

HANDTYPES = [
    "invalid hand",
    "high card",
    "one pair",
    "two pairs",
    "three of a kind",
    "straight",
    "flush",
    "full house",
    "four of a kind",
    "straight flush",
]

CARDS_TO_ID = {
    "2c": 1,
    "2d": 2,
    "2h": 3,
    "2s": 4,
    "3c": 5,
    "3d": 6,
    "3h": 7,
    "3s": 8,
    "4c": 9,
    "4d": 10,
    "4h": 11,
    "4s": 12,
    "5c": 13,
    "5d": 14,
    "5h": 15,
    "5s": 16,
    "6c": 17,
    "6d": 18,
    "6h": 19,
    "6s": 20,
    "7c": 21,
    "7d": 22,
    "7h": 23,
    "7s": 24,
    "8c": 25,
    "8d": 26,
    "8h": 27,
    "8s": 28,
    "9c": 29,
    "9d": 30,
    "9h": 31,
    "9s": 32,
    "tc": 33,
    "td": 34,
    "th": 35,
    "ts": 36,
    "jc": 37,
    "jd": 38,
    "jh": 39,
    "js": 40,
    "qc": 41,
    "qd": 42,
    "qh": 43,
    "qs": 44,
    "kc": 45,
    "kd": 46,
    "kh": 47,
    "ks": 48,
    "ac": 49,
    "ad": 50,
    "ah": 51,
    "as": 52,
}

def evalHand(cards):
    hand = map(lambda card: CARDS_TO_ID[card], cards)
    return evalHand(hand)

def evaluate(hand):
    p = 53
    for card in hand:
        p = evalCard(p + card)

    if len(hand) == 5:
        p = evalCard(p)

    return {
        'handType': p >> 12,
        'handRank': p & 0x00000fff,
        'value': p,
        'handName': HANDTYPES[p >> 12],
    }


def evalCard(card):
    return Data[card]

def init():
    global Data
    Data.fromfile(open('../HandRanks.dat', 'rb'), 32487834)


init()

if __name__ == '__main__':
    to_eval = []
    for _ in xrange(int(1e6)):
        to_eval.append(sample(range(1, 53), 7))

    start_time = time()
    for hand in to_eval:
        evaluate(hand)
    end_time = time()

    print end_time - start_time

    '''
    print evaluate([52, 48, 44, 40, 37])
    print evaluate([1, 2, 3, 4, 5])
    print evaluate([1,5,9,13,17])
    print evaluate([1,5,9,13,17,21,25])
    '''

