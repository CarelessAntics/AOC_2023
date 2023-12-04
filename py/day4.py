import re


def main():

    with open("../inputs/day4/input.txt") as f:
        raw = f.read().splitlines()

    raw = [x.split(': ')[1] for x in raw]

    numbers = [[int(z) for z in y.split(' ') if z != ''] 
                for y in [x.split(' | ')[0] for x in raw]]

    winners = [[int(z) for z in y.split(' ') if z != ''] 
                for y in [x.split(' | ')[1] for x in raw]]

    P1_Answer = P1_get_score(numbers, winners)
    P2_Answer = P2_exponential_scratchcards(numbers, winners)

    print(P1_Answer)
    print(P2_Answer)


def P1_get_score(numbers, winners):

    pairs = zip(numbers, winners)
    total_score = 0
    
    for pair in pairs:
        card_score = 0

        for number in pair[0]:
            if number in pair[1]:
                if card_score == 0:
                    card_score = 1
                else:
                    card_score *=2

        total_score += card_score

    return total_score


def P2_exponential_scratchcards(numbers, winners):

    pairs = zip(numbers, winners)
    card_counts = [1] * len(numbers)

    # Get the amount of winning cards with set intersection, loop that many times and increment the later card counts by the amount of copies of the current card
    for i, pair in enumerate(pairs):
        win_count = len(list(set(pair[0]).intersection(pair[1])))

        for j in range(win_count):
            card_counts[min(i + j + 1, len(card_counts) - 1)] += card_counts[i]

    return sum(card_counts)



if __name__ == "__main__":
    main()