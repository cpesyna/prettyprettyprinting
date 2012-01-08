#!/usr/bin/python2

import argparse
import os.path
from collections import defaultdict
from itertools import product
from sys import stderr, exit

def key_wrangler(word):
    return "".join(sorted(word.strip()))

def build_val_wrangler(minimum_length):
    def val_wrangler(word):
        sanitized = word.strip().capitalize()
        l = len(sanitized)
        if l < minimum_length:
            return "-" * l
        else:
            return sanitized
    return val_wrangler
        
class wrangled_dict(dict):
    """docstring for wrangled_dict"""
    #TODO: Yeah...write that.
    def __init__(self, s = (), key_wrangler = lambda x:x, val_wrangler = lambda x:x):
        super(wrangled_dict, self).__init__()

        self.key_wrangler = key_wrangler
        self.val_wrangler = val_wrangler

        for item in s:
            self.put(item)

    def __getitem__(self, key):
        return super(wrangled_dict, self).__getitem__(self.key_wrangler(key))

    def put(self, word):
        self[self.key_wrangler(word)] = self.val_wrangler(word)

    def get(self, word):
        try:
            return self[word]
        except KeyError:
            return "-" * len(word)

class Measure(dict):
    # TODO: Make safer for broad range of input
    """docstring for measure"""
    def __init__(self):
        super(Measure, self).__init__()

    def __getitem__(self, key):
        try:
            return super(Measure, self).__getitem__(key)
        except KeyError:
            if isinstance(key, tuple):
                return key[1] - key[0]
            elif isinstance(key, int):
                return key
            else:
                raise ValueError

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
            print >> stderr, "{0}: Supplied string file cannot be opened".format(args.string)
        args.string = fh.read().strip()
    strlen = len(args.string)
    
    # TODO: Edit args to perceive args.dictionary as a file
    try:
        args.dictionary = open(args.dictionary)
    except IOError:
        print >> stderr, "{0}: Supplied dictonary file cannot be opened".format(args.dictionary)
        exit(1)
        
    wl = wrangled_dict(args.dictionary, key_wrangler, build_val_wrangler(args.min_len))
    args.dictionary.close()

    if not args.max_len:
        args.max_len = len(max(wl, key = len))

    diff = Measure()
    for start, offset in product(range(strlen), range(args.min_len, args.max_len)):
        result = wl.get(args.string[start:start + offset])
        #Assumes no hyphenated words...is this okay?
        if '-' not in result:
            diff[start, start + offset] = 0

    prev = defaultdict(lambda: None)

    # There ought to be a cleaner way to write this
    # TODO: Implement this based on a FibHeap
    Q = range(strlen + 1)
    while Q:
        curr = min(Q, key = lambda x: diff[x])
        Q.remove(curr)
        for node in Q:
            if node < curr:
                continue
            alt = diff[curr] + diff[curr, node]
            if alt <= diff[node]:
                diff[node] = alt
                prev[node] = curr
    S = []
    curr = strlen
    while prev[curr] != None:
        S.insert(0, curr)
        curr = prev[curr]
    # Even if S is of the form [0, ...] to begin with, this is unconditionally
    # safe
    S.insert(0, 0)

    print("".join([wl.get(args.string[i:j]) for i, j in zip(S[:-1], S[1:])]))
    
if __name__ == "__main__":
    main()
