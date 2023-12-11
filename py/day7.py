import string
import copy
import pprint


def main():
    with open("../inputs/day7/input.txt") as f:
        raw_P1 = [{'hand': hand, 'bid': int(bid)} for hand, bid in [x.split(' ') for x in f.read().splitlines()]]
        raw_P2 = copy.deepcopy(raw_P1)
    
    P1_answer = P1_compare_hands(raw_P1)
    P2_answer = P2_compare_hands(raw_P2)

    print(P1_answer)
    print(P2_answer)


def P1_compare_hands(data):
    # Conversion dictionary for card values. Convert values to alphabet for later sorting
    cards_alphabet = {str(i+2): x for i, x in enumerate(string.ascii_lowercase[12:4:-1])} | {'T': 'e', 'J': 'd', 'Q': 'c', 'K': 'b', 'A': 'a'}

    for play in data:

        hand = play['hand']
        hand_type = {}
        hand_values = "".join(cards_alphabet[x] for x in hand)

        # count the amount of occurrences in the hand
        for card in hand:
            if card not in hand_type:
                hand_type[card] = 1
            else:
                hand_type[card] += 1

        hand_strength = 0
        v = list(hand_type.values())

        # Determine hand strength based on card amounts
        if 5 in v:
            # Five of a kind
            hand_strength = 7
        elif 4 in v:
            # Four of a kind
            hand_strength = 6
        elif 3 in v:
            if 2 in v:
                # Full House
                hand_strength = 5
            else:
                # Three of a kind
                hand_strength = 4
        elif 2 in v:
            if v.count(2) == 2:
                # Two pair
                hand_strength = 3
            else:
                # Pair
                hand_strength = 2
        else:
            # High Card
            hand_strength = 1
        
        play['strength'] = hand_strength
        play['values'] = hand_values

    # Sort hands by strength
    data.sort(key=lambda x: x['strength'], reverse=True)
    rank = 0
    winning_order = []

    # Order same strength hands based on previous alphabet conversion. Set hand rank
    for i in range(7):
        division = sorted([x for x in data if x['strength'] == i + 1], key=lambda x: x['values'], reverse=True)
        for d in division:
            rank += 1
            d['rank'] = rank

        winning_order += division

    return calculate_winnings(winning_order)


# Same as P1, but with Jokers
def P2_compare_hands(data):
    # Conversion dictionary for card values. Convert values to alphabet for later sorting. Added Joker as lowest card value
    cards_alphabet = {str(i+2): x for i, x in enumerate(string.ascii_lowercase[12:4:-1])} | {'T': 'e', 'J': 'd', 'Q': 'c', 'K': 'b', 'A': 'a', 'J': 'z'}

    for play in data:

        hand = play['hand']
        hand_type = {'J': 0}
        hand_values = "".join(cards_alphabet[x] for x in hand)

        for card in hand:
            if card not in hand_type:
                hand_type[card] = 1
            else:
                hand_type[card] += 1

        # Extract the highest occurrence amount from the list, ignoring Jokers. Joker occurrences in a separate variable
        hand_strength = 0
        v = sorted([x if card != 'J' else 0 for card, x in hand_type.items()], reverse=True)
        best = v.pop(0)
        jokers = hand_type['J']

        # Same comparison as in P1, but hand strength is determined by the sum of jokers and the highest occurrence of similar cards
        if best + jokers == 5:
            # Five of a kind
            hand_strength = 7

        elif best + jokers == 4:
            # Four of a kind
            hand_strength = 6

        elif best + jokers == 3:
            if 2 in v:
                # Full House
                hand_strength = 5
            else:
                # Three of a kind
                hand_strength = 4

        elif best + jokers == 2:
            if 2 in v and best == 2:
                # Two pair
                hand_strength = 3
            else:
                # Pair
                hand_strength = 2
        else:
            # High Card
            hand_strength = 1
        
        play['strength'] = hand_strength
        play['values'] = hand_values

    data.sort(key=lambda x: x['strength'], reverse=True)
    rank = 0
    winning_order = []


    for i in range(7):
        division = sorted([x for x in data if x['strength'] == i + 1], key=lambda x: x['values'], reverse=True)
        for d in division:
            rank += 1
            d['rank'] = rank

        winning_order += division

    #pprint.pprint(winning_order)

    return calculate_winnings(winning_order)


def calculate_winnings(data):
    result = 0
    for d in data:
        result += d['rank'] * d['bid']

    return result


if __name__ == "__main__":
    main()