import multiprocessing as mp
import math


class Node:

    def __init__(self, label):
        self.label = label
        self.left = None
        self.right = None


# I thought this might be a tree but it's more like a node graph. 
class Tree:

    # Store node objects in a set
    def __init__(self, tree_map):
        self.root = None
        self.catalogue = set()

        for rule in tree_map:
            self.add_node(rule)

        # For Problem 1
        self.root = [x for x in self.catalogue if x.label == 'AAA'][0]


    def add_node(self, rule):

        # For an empty set, add first node manually
        if not self.catalogue:
            root = Node(rule[0])
            left = Node(rule[1])

            self.root = root
            self.root.left = left

            self.catalogue.update((root, left))

            if rule[1] == rule[2]:
                self.root.right = self.root.left
            else:
                right = Node(rule[2])
                self.root.right = right
                self.catalogue.add(right)

        # For the rest, search if any of the nodes in the input exist
        else:
            found = self.search_node(rule)
            labels = [x.label for x in found]

            # Then for each rule, either create a new node, or utilize the existing one
            if rule[0] not in labels:
                root = Node(rule[0])
                self.catalogue.add(root)
            else:
                root = [x for x in found if x.label == rule[0]][0]

            if rule[1] not in labels:
                left = Node(rule[1])
                self.catalogue.add(left)
            else:
                left = [x for x in found if x.label == rule[1]][0]

            # If the branch nodes are not the same, add a right side node as usual. Otherwise point the right parameter to the left parameter
            if rule[1] != rule[2]:
                if rule[2] not in labels:
                    right = Node(rule[2])
                    self.catalogue.add(right)
                else:
                    right = [x for x in found if x.label == rule[2]][0]
            else:
                right = left

            root.left = left
            root.right = right


    # Search for multiple nodes in the "Tree" catalogue, return only if found
    def search_node(self, targets):
        found = []
        for node in self.catalogue:
            if node.label in targets:
                found.append(node)
            # Stop searching if the found nodes match the amount of targets
            if len(found) >= len(targets):
                break
        
        return found

    
    # Print the structure for debug purposes
    def print_tree(self, nxt='start', ignore=set()):
        if nxt is None:
            return
        if nxt == 'start':
            nxt = self.root
        if nxt.label in ignore:
            return

        ignore.add(nxt.label)

        print(f"Node: {nxt.label}\nLeft: {nxt.left.label if nxt.left is not None else 'None'}, Right: {nxt.right.label if nxt.right is not None else 'None'}\n----")
        #print(f"Node: {nxt.label, nxt}\nLeft: {nxt.left}, Right: {nxt.right}\n----")
        self.print_tree(nxt.left, ignore)
        self.print_tree(nxt.right, ignore)


    # Multithread the separate paths. Then find the least common multiple of the results to find the first step count where all the paths match up
    # I remember this from last year!
    def P2_run_paths(self, instructions):
        start_nodes = [x for x in self.catalogue if x.label[-1] == 'A']
        threads = []

        # Return the values to a shared dictionary
        manager = mp.Manager()
        paths = manager.dict()

        for i, node in enumerate(start_nodes):
            t = mp.Process(target=self.traverse_P2, args=(node, instructions, i, paths))
            threads.append(t)
            t.start()

        for thread in threads:
            thread.join()

        nums = math.lcm(*paths.values())
        return nums


    # Travel along the node path and count the steps
    def traverse_P1(self, instructions):

        current = self.root
        l = len(instructions)
        i = 0

        while True:
            #print(current.label)
            if current is None:
                print("FAIL")
                break
            if current.label == 'ZZZ':
                break

            if instructions[i%l] == 'L':
                current = current.left
            else:
                current = current.right
            i += 1

        return i
    

    # Same as P1, but for multiple starting points
    def traverse_P2(self, start, instructions, num, paths):

        current = start
        l = len(instructions)
        i = 0

        while True:
            if current is None:
                print("FAIL")
                break
            if current.label[-1] == 'Z':
                #print(f"Found in {i} steps")
                break

            if instructions[i%l] == 'L':
                current = current.left
            else:
                current = current.right
            i += 1

        paths[num] = i


def main():
    with open("../inputs/day8/input.txt") as f:
        raw = f.read()

    instructions, tree_map = tuple(x for x in raw.split('\n\n'))
    tree_map = [[y[0]] + y[1][1:-1].split(', ') for y in [x.split(' = ') for x in tree_map.split('\n')]]

    tree = Tree(tree_map)
    #tree.print_tree()

    P1_answer = tree.traverse_P1(instructions)
    P2_answer = tree.P2_run_paths(instructions)

    print(f"P1 found in {P1_answer} steps")
    print(f"P2 found in {P2_answer} steps")

if __name__ == "__main__":
    main()