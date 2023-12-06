import re


class Converter:

    def __init__(self, node_input: str, previous=None):

        lists = node_input.split('\n')
        labels = re.split('\-to\-|\s', lists.pop(0))[:2]

        self.previous_label = labels[0]
        self.next_label = labels[1]

        self.previous = previous
        self.next = None

        self.start_dst = []
        self.start_src = []
        self.ranges = []

        self.last_location = None

        for l in lists:
            values = [int(x) for x in l.split(' ')]
            self.start_dst.append(values[0])
            self.start_src.append(values[1])
            self.ranges.append(values[2])


    def add_node(self, node_input):
        if self.next is None:
            self.next = Converter(node_input, self)
        else:
            self.next.add_node(node_input)


    def P1_convert(self, seed: int):
        conversions = zip(self.start_src, self.start_dst, self.ranges)
        new_seed = None

        # Source, destination, range
        for src, dst, rng in conversions:
            if seed >= src and seed < src + rng:
                new_seed = dst + (seed - src)
        
        if new_seed is None:
            new_seed = seed

        # print(f"P1: {self.previous_label}: {seed} to {self.next_label}: {new_seed}")

        if self.next is None:
            self.last_location = new_seed
        else:
            self.next.P1_convert(new_seed)

    
    def P2_convert(self, seed_ranges: set):

        # Working with sets instead to easily eliminate duplicates
        conversions = zip(self.start_src, self.start_dst, self.ranges)
        new_seeds = set()

        # Start going through te conversion ranges
        for src, dst, rng in conversions:

            range_count = 1
            range_count_previous = 0

            # Keep looping as for as long as seed_ranges has elements or the amount of elements remains the same
            while range_count != range_count_previous:

                if seed_ranges:
                    sa, sb = seed_ranges.pop()
                else:
                    break

                # If the seed range is completely within conversion range
                if sa >= src and sa + sb < src + rng:
                    offset = sa - src
                    new_seeds.add((dst + offset, sb))

                # If seed range start is within conversion range
                elif sa >= src and sa < src + rng:
                    offset = sa - src
                    new_range = max(1, (src + rng) - sa)
                    new_seeds.add((dst + offset, new_range))

                    # Make a new range of part left outside
                    if sa + sb > src + rng:
                        seed_ranges.add((src + rng, sb - new_range))

                # if seed range end is within conversion range, but start isn't
                elif sa + sb >= src and sa + sb < src + rng:
                    new_range = max(1, (sa + sb) - src)
                    new_seeds.add((dst, new_range))

                    # Same as before, new range from part left outside
                    if sa < src:
                        seed_ranges.add((sa, sb - new_range))

                # No overlap between seed and conversion ranges
                else:
                    seed_ranges.add((sa, sb))

                range_count_previous = range_count
                range_count = len(seed_ranges)
        
        if self.next is None:
            lowest = min(x[0] for x in new_seeds.union(seed_ranges))
            self.last_location = lowest

        else:
            self.next.P2_convert(new_seeds.union(seed_ranges))


def main():

    with open("../inputs/day5/input.txt") as f:
        raw = f.read().split('\n\n')

    P1_seeds = [int(x) for x in raw.pop(0).split(' ') if x.isnumeric()]
    P2_seeds = [(P1_seeds[i], P1_seeds[i + 1]) for i in range(0, len(P1_seeds), 2)]

    # A linked list, even
    converter_chain = None
    for r in raw:

        if converter_chain is None:
            converter_chain = Converter(r)
        else:
            converter_chain.add_node(r)

    P1_answer = get_closest(P1_seeds, converter_chain, 'P1')
    P2_answer = get_closest(P2_seeds, converter_chain, 'P2')

    print(P1_answer)
    print(P2_answer)


def get_closest(seeds, converter_chain, problem: str):
    locations = []

    for seed in seeds:
        if problem == 'P1':
            converter_chain.P1_convert(seed)
        elif problem == 'P2':
            converter_chain.P2_convert({seed})
        
        node = converter_chain
        while True:
            if node.last_location is None:
                node = node.next
            else:
                location = node.last_location
                break

        locations.append(location)

    return min(locations)
        

if __name__ == "__main__":
    main()
