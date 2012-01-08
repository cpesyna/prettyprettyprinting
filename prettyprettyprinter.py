#!/usr/bin/python2

import argparse
import os.path
from collections import defaultdict
from itertools import product
from sys import stderr, exit

class WordMap(dict):
    """docstring for WordMap"""
    #TODO: Yeah...write that.
    def __init__(self, min_length, s = ()):
        super(WordMap, self).__init__()
        
        if min_length < 0:
            raise ValueError, "Cannot allow negative min_length"

        self.min_length = min_length
        for item in s:
            self.put(item)

    def __getitem__(self, key):
        return super(WordMap, self).__getitem__(self.__sanitize_key__(key))

    def __sanitize_key__(self, word):
        return "".join(sorted(word.strip()))

    def put(self, word):
        if len(word) < self.min_length:
            return
        self[self.__sanitize_key__(word)] = word

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
        self.base = base

    def __getitem__(self, key):
        try:
            return super(Measure, self).__getitem__(key)
        except KeyError:
            if isinstance(key, tuple):
                return abs(key[1] - key[0])
            elif isinstance(key, int):
                return abs(self.base - key)
            else:
                raise TypeError

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

def main():
    """A humble attempt to solve Mopub's PrettyPrettyPrinting developer
    challenge: http://www.mopub.com/about/coding-challenges/"""

    args = process_args()

    if(os.path.exists(args.string)):
        try:
            fh = open(args.string, 'r') 
        except:
            print >> stderr, "{}: Supplied string file cannot be opened".format(args.string)
        args.string = fh.read().strip()
    strlen = len(args.string)
    
    # TODO: Edit args to perceive args.dictionary as a file
    try:
        args.dictionary = open(args.dictionary)
    except IOError:
        print >> stderr, "{}: Supplied dictionary file cannot be opened".format(args.dictionary)
        exit(1)
        
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

    prev = defaultdict(lambda: None)

    # TODO: Implement this based on a FibHeap
    # Dijkstra's algorithm, run starting from the last character in the test
    # string.
    Q = range(strlen + 1)
    diff[strlen] = 0
    while Q:
        curr = min(Q, key = lambda x: diff[x])
        Q.remove(curr)
        if curr == 0:
            break
        for node in Q:
            if node > curr:
                continue
            alt = diff[curr] + diff[curr, node]
            if alt <= diff[node]:
                diff[node] = alt
                prev[node] = curr
    S = []
    curr = 0
    while prev[curr] != None:
        S.append(curr)
        curr = prev[curr]
    # Even if S is of the form [...,strlen] to begin with, this is unconditionally
    # safe, and at worst adds one iteration to the following loop
    S.append(strlen)

    solution = []
    for start, stop in zip(S, S[1:]):
        word = wl.get(args.string[start:stop])
        if word:
            solution.append(word.strip().capitalize())
        else:
            solution.append("-" * (stop - start))
    print("".join(solution))
    
if __name__ == "__main__":
    main()
