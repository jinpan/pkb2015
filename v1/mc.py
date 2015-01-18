from copy import copy
from random import sample

from eval import evaluate


NTrials = 1e3

def sim(card1, card2, n_revealed):
    deck = range(1, 53)
    deck.remove(card1)
    deck.remove(card2)

    total = 0
    for _ in xrange(int(NTrials)):
        common = sample(deck, n_revealed)
        deck_copy = copy(deck)
        for card in common:
            deck_copy.remove(card)
        total += sim_once(card1, card2, common, deck_copy)
    return total / NTrials


def sim_once(card1, card2, common, deck):
    cards = sample(deck, 9-len(common))
    p2_cards = cards[0:2]
    p3_cards = cards[2:4]
    common2 = cards[4:]

    hand1 = [card1, card2] + common + common2
    hand2 = p2_cards + common + common2
    hand3 = p3_cards + common + common2

    score1 = evaluate(hand1)['value']
    score2 = evaluate(hand2)['value']
    score3 = evaluate(hand3)['value']

    # TODO incorporate ties
    if score1 > score2 and score1 > score3:
        return 1.
    elif score1 == score2 and score1 == score3:
        return 1./3
    elif score1 == score2 and score1 > score3:
        return 1./2
    elif score1 == score3 and score1 > score2:
        return 1./2
    else:
        return 0.


if __name__ == '__main__':

    '''
    cards = range(1, 53)
    results = [[None] * len(cards) for _ in cards]

    for idx1, card1 in enumerate(cards):
        for idx2, card2 in enumerate(cards):
            if idx1 >= idx2:
                continue
            results[idx1][idx2] = sim(card1, card2, 0)
    '''

    # two aces
    print sim(49, 50, 0)

    # flush draw
    print sim(9, 33, 0)

    # high card
    print sim(10, 45, 0)

    # trash
    print sim(2, 24, 0)
