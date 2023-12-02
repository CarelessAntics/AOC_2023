import re


def main():

    with open('../inputs/day2/input.txt') as f:
        raw = f.read().splitlines()

    # Split input strings by : or ; and remove the first entry
    raw = [re.split(': |; ', x)[1:] for x in raw]
    games = []

    # Define each game as a list where each turn is a list item. Turns are represented as a dictionary with cube colors as key and amount as value
    for game in raw:
        #scores = {'red': 0, 'green': 0, 'blue': 0}
        turns = []

        for turn in game:

            scores = [x for x in turn.split(', ')]
            scores = {x.split(' ')[1]: int(x.split(' ')[0]) for x in scores}

            for color in ('red', 'green', 'blue'):
                if color not in scores.keys():
                    scores[color] = 0
            
            turns.append(scores)
        games.append(turns)

    P1_answer = P1_possible_games(games)
    P2_answer = P2_fewest_cubes(games)

    print(P1_answer)
    print(P2_answer)


def P1_possible_games(games):
    limit = {'red': 12, 'green': 13, 'blue': 14}
    count = 0
    impossible = False

    # Iterate through each game > turn > score and if any score is above a set limit, set a flag for the game being impossible
    for i, game in enumerate(games):
        for scores in game:
            for color, amount in scores.items():

                if amount > limit[color]:
                    impossible = True
                    break
            
            if impossible:
                break

        if impossible:
            impossible = False
            continue
        
        count += i+1
    return count


def P2_fewest_cubes(games):
    count = 0

    for i, game in enumerate(games):
        fewest = {'red': 0, 'green': 0, 'blue': 0}

        for scores in game:
            fewest = {color: max(amount, fewest[color]) for color, amount in scores.items()}

        power = 1
        for amount in fewest.values():
            power *= amount

        count += power
        
    return count


if __name__ == '__main__':
    main()