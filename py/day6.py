import re


def main():

    with open("../inputs/day6/input.txt") as f:
        raw = f.read().splitlines()

    stats_P1 = [[int(y) for y in re.split('\s+', x)[1:]] for x in raw]
    stats_P2 = [int("".join(str(y) for y in x)) for x in stats_P1]

    stats_P1 = zip(stats_P1[0], stats_P1[1])

    P1_answer = P1_calculate_speed(stats_P1)
    P2_answer = P1_calculate_speed([stats_P2])

    print(P1_answer)
    print(P2_answer)


def P1_calculate_speed(stats):
    prod = 1

    for stat in stats:
        time = stat[0]
        target = stat[1]
        count = 0

        for wait in range(time + 1):
            distance = wait * (time - wait)
            if distance > target:
                count += 1

        prod *= count

    return prod

if __name__ == "__main__":
    main()