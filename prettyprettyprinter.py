#!/usr/bin/python

import argparse
from collections import defaultdict
from itertools import product
from os import path
from sys import stderr, exit

# TODO: Work on exposing this and writing unit tests

class WordMap(dict):
    """docstring for WordMap"""
    #TODO: Yeah...write that.
    def __init__(self, min_length, s = ()):
        super(WordMap, self).__init__()
        if min_length < 0:
            raise ValueError("Cannot allow negative min_length")
        
        self.min_length = min_length
        self.put_iterable(s)

    def __getitem__(self, key):
        return super(WordMap, self).__getitem__(self.__sanitize_key__(key))

    def __sanitize_key__(self, word):
        return "".join(sorted(word))

    def put(self, word):
        word = word.strip()
        if len(word) >= self.min_length:
            self[self.__sanitize_key__(word)] = word

    def put_iterable(self, iterable):
        for word in iterable:
            self.put(word)

    def get(self, word):
        try:
            return self[word]
        except KeyError:
            return None


class Measure(dict):
    # TODO: Make safer for broad range of input
    """docstring for measure"""
    def __init__(self, base):
        super(Measure, self).__init__()
        if isinstance(base, int):
            self.base = base
        else:
            raise TypeError("Cannot accept base of type {}".format(type(int)))

    def __getitem__(self, key):
        try:
            return super(Measure, self).__getitem__(key)
        except KeyError:
            if isinstance(key, tuple):
                if len(key) != 2:
                    raise ValueError("Invalid key passed to Measure: {}".format(key))
                return abs(key[1] - key[0])
            elif isinstance(key, int):
                return abs(self.base - key)
            else:
                raise TypeError("Invalid key passed to Measure: {}".format(key))

def process_args():
    parser = argparse.ArgumentParser(
        description = 'Complete PrettyPrettyPrinter challenge!')
    parser.add_argument('-d', type=str, default='mowords.txt',
        dest='dictionary', required=0, help='path to dictionary file')
    parser.add_argument('-s', type=str, dest='string', required=1,
        help='string to use or path to string file')
    parser.add_argument('-min_len', type=int, dest='min_len', default = 4,
        required=0, help='Define minimum acceptable word length')
    parser.add_argument('-max_len', type=int, dest='max_len', default = None,
        required=0, help='Define minimum acceptable word length')
    return parser.parse_args()

def dijkstra(neighbors, dist, target = None):
    #TODO: Still ought to be using a heap
    Q = set(neighbors.keys())
    final = max(Q)
    prev = defaultdict(lambda: None)
    while Q:
        curr = min(Q, key = lambda x: dist[x])
        Q.remove(curr)
        if curr == target:
            break
        for node in neighbors[curr].intersection(Q):
            alt = dist[curr] + dist[curr, node]
            if alt < dist[node]:
                dist[node] = alt
                prev[node] = curr
    curr = 0
    pointers = [curr]
    while prev[curr] != None:
        curr = prev[curr]
        pointers.append(curr)
    if pointers[-1] != final:
        pointers.append(final)
    return pointers

def main():
    """A humble attempt to solve Mopub's PrettyPrettyPrinting developer
    challenge: http://www.mopub.com/about/coding-challenges/"""

    args = process_args()

    if(path.exists(args.string)):
        fh = open(args.string, 'r') 
        args.string = fh.read().strip()
        fh.close()
    strlen = len(args.string)
    
    # TODO: Edit args to perceive args.dictionary as a file
    # TODO: Mention something about filetype...
    args.dictionary = open(args.dictionary, encoding = "ISO-8859-1")
        
    wl = WordMap(args.min_len, args.dictionary)
    args.dictionary.close()

    if not args.max_len:
        args.max_len = len(max(wl, key = len))

    diff = Measure(strlen)
    for start, offset in product(range(strlen), range(args.min_len, args.max_len)):
        result = wl.get(args.string[start:start + offset])
        if result:
            # We will be iterating backwards over our string
            diff[start + offset, start] = 0

    diff[strlen] = 0
    neighbors = {index:set(range(max(0, index - args.max_len), index))
                for index in range(strlen + 1)}
    pointers = dijkstra(neighbors, diff, 0)

    solution = []
    for start, stop in zip(pointers, pointers[1:]):
        word = wl.get(args.string[start:stop])
        if word:
            solution.append(word.capitalize())
        else:
            solution.append("-" * (stop - start))
    print("".join(solution))
    
if __name__ == "__main__":
    main()
