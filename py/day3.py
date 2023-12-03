


def main():
    
    with open("../inputs/day3/input.txt") as f:
        raw = f.read().splitlines()

    # Generate coordinates of all parts in the schematic
    # format: [{'row: int,'start': int, 'end': int}]
    part_coords = []
    for i, row in enumerate(raw):

        start = None
        current = None
        end = None

        for j, c in enumerate(row):
            if c.isnumeric():
                if current is None:
                    start = j

                current = j

                if j == len(row) - 1:
                    end = current
            else:
                if current is not None:
                    end = current

            if end is not None:
                part = {'row': i, 'start': start, 'end': end}
                part_coords.append(part)
                
                start = None
                current = None
                end = None

    P1_answer = P1_validate_parts(raw, part_coords)
    P2_answer = P2_gears(raw, part_coords)

    print(P1_answer)
    print(P2_answer)



def P1_validate_parts(input, coords):

    valid = []
    
    # Find adjacent symbols by offsetting part coordinates by 1 and ignoring the original coordinate positions
    for coord in coords:
        row = coord['row']
        start = coord['start']
        end = coord['end']

        min_y = max(row - 1, 0)
        max_y = min(row + 1, len(input) - 1)

        min_x = max(start - 1, 0)
        max_x = min(end + 1, len(input[0]) - 1)

        adjacent = any(input[y][x] != '.' if not (y == row and x >= start and x <= end) else False
                        for x in range(min_x, max_x + 1) 
                        for y in range(min_y, max_y + 1))

        if adjacent:
            valid.append(int(input[row][start : end + 1]))

    return sum(valid)


def P2_gears(input, coords):

    # Start by finding all asterisks
    possible_gears = [(x, y) for y, row in enumerate(input) for x, c in enumerate(row) if c == '*']
    prods = []

    # For each asterisk, generate offset coordinate ranges, and convert them to sets
    for gear in possible_gears:
        range_y = set(range(gear[1] - 1, gear[1] + 2))
        range_x = set(range(gear[0] - 1, gear[0] + 2))

        # Create a tuple of adjacent coordinates with set intersection for x and direct comparison for y
        adjacent_parts = tuple(coord for coord in coords 
                            if range_x.intersection(range(coord['start'], coord['end'] + 1)) 
                            and coord['row'] in range_y)
        
        if len(adjacent_parts) == 2:

            start_a = adjacent_parts[0]['start']
            end_a = adjacent_parts[0]['end']
            row_a = adjacent_parts[0]['row']
            
            start_b = adjacent_parts[1]['start']
            end_b = adjacent_parts[1]['end']
            row_b = adjacent_parts[1]['row']

            prod = int(input[row_a][start_a : end_a + 1]) * int(input[row_b][start_b : end_b + 1])
            prods.append(prod)

    return sum(prods)


if __name__ == '__main__':
    main()