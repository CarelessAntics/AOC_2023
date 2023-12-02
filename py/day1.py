

def main():
    with open("../inputs/day1/input.txt") as f:
        raw = f.read().splitlines()

    #Problem 1
    calibration_values_P1 = []
    calibration_values_P2 = []
    for entry in raw:
        calibration_values_P1.append(get_calibration_value_P1(entry))
        calibration_values_P2.append(get_calibration_value_P2(entry))

    #print(calibration_values_P2)

    P1_answer = sum(calibration_values_P1)
    P2_answer = sum(calibration_values_P2)

    print(P1_answer)
    print(P2_answer)


def get_calibration_value_P1(entry):
    numbers = ""
    for c in entry:
        if c.isdigit():
            numbers += c
    
    if numbers != "":
        return int(numbers[0] + numbers[-1])
    else:
        return 0
    

def get_calibration_value_P2(entry):
    #numbers = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    numbers = {'one':'1', 'two':'2', 'three':'3', 'four':'4', 'five':'5', 'six':'6', 'seven':'7', 'eight':'8', 'nine':'9'}
    entryPartial = ""

    # Read string one character at a time. When the partial string matches a key in the numbers dictionary, or when the character is a digit,
    # add the digit to a new string. Then slice the original string to start from the penultimate character to account for overlaps, reset counters and start over
    i = 0
    digits = ""
    length = len(entry)

    while i < length:

        c = entry[i]
        entryPartial += c

        if any(number in entryPartial for number in numbers.keys()):
            n = tuple(n for number, n in numbers.items() if number in entryPartial)[0]
            digits += n
            entryPartial = ""
            entry = entry[i-1:]
            length = len(entry)
            i = 0

        elif c.isdigit():
            digits += c

        i += 1

    if digits != "":
        return int(digits[0] + digits[-1])
    else:
        return 0


if __name__ == "__main__":
    main()