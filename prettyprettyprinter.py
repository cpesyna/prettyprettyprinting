#!/usr/bin/python2

import argparse
import os.path
from collections import defaultdict

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

    def __putitem__(self, key):
        super(wrangled_dict, self).__putitem__(self.key_wrangler(key), self.val_wrangler(key))

    def put(self, word):
        self[self.key_wrangler(word)] = self.val_wrangler(word)

    def get(self, word):
        try:
            return self[word]
        except KeyError:
            return "-" * len(word)

class measure(dict):
    """docstring for wrangled_dict"""
    def __init__(self):
        super(measure, self).__init__()

    def __getitem__(self, key):
        try:
            return super(measure, self).__getitem__(key)
        except KeyError:
            return key[1] - key[0]


def slicepoints(total_length, min_length = 4, max_length = 29):
    ## Check out if there's a saner way to write this...
    for start in range(total_length - min_length + 1):
        top = min(total_length + 1, start + max_length)
        for stop in range(start + min_length, top):
            yield start, stop

def process_args():
    parser = argparse.ArgumentParser(
        description = 'Complete PrettyPrettyPrinter challenge!')
    parser.add_argument('-d', type=str, default='mowords.txt',
        dest='dictionary', required=0, help='path to dictionary file')
    parser.add_argument('-s', type=str, dest='string', required=1,
        help='string to use or path to string file')
    return parser.parse_args()

def get_limits(wordlist):
    longest = None
    shortest = None
    for key in wordlist:
        keylen = len(key)
        shortest = keylen if not shortest else min(shortest, keylen)
        longest = keylen if not longest else max(longest, keylen)
    return shortest, longest 

def main():
    """A humble attempt to solve Mopub's PrettyPrettyPrinting developer
    challenge: http://www.mopub.com/about/coding-challenges/"""

    MOPUB_MINLENGTH = 4
    args = process_args()

    if(os.path.exists(args.string)):
        fh = open(args.string, 'r') 
        args.string = fh.read().strip()
    
    # TODO: Edit args to perceive args.dictionary as a file
    args.dictionary = open(args.dictionary)
    wl = wrangled_dict(args.dictionary, key_wrangler, build_val_wrangler(MOPUB_MINLENGTH))
    args.dictionary.close()

    # Could do something cleaner to deal with Mopub defined min_length
    min_len, max_len = get_limits(wl)

    # Come up with a cleaner way of expressing "measure"
    # maybe just do try/except
    delta = measure()
    strlen = len(args.string)
    for start, stop in slicepoints(strlen, MOPUB_MINLENGTH, max_len):
        result = wl.get(args.string[start:stop])
        if '-' not in result:
            delta[start, stop] = 0

    # Tidy up Dijkstra
    dist = defaultdict(lambda: strlen + 1)
    prev = defaultdict(lambda: None)

    dist[0] = 0
    # There ought to be a cleaner way to write this
    # TODO: Implement this based on a FibHeap
    Q = range(strlen + 1)
    while Q:
        curr = min(Q, key = lambda x: dist[x])
        Q.remove(curr)
        for node in Q:
            if node < curr:
                continue
            alt = dist[curr] + delta[curr, node]
            if alt <= dist[node]:
                dist[node] = alt
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
