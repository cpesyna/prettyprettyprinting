#!/usr/bin/python2

import argparse
import os.path
import sys
from collections import defaultdict

class worddict(defaultdict):
    #TODO: Figure this subclassing out...
    """docstring for worddict"""
    def __getitem__(self, key):
        x = super(worddict, self).__getitem__("".join(sorted(key)))
        return x
        
def lookup(word, wl):
    """Stupid hack. Lookup subclassing defaultdict and overriding __getitem__"""
    print wl["act"]
    try:
        return wl["".join(sorted(word))]
    except KeyError:
        return False

def prep_wordlist(wl_file):
    wl = worddict(list)
    for line in wl_file:
        line = line.strip()
        if len(line) > 3:
            wl["".join(sorted(line))].append(line)
            if len( wl["".join(sorted(line))]) > 1:
                print wl["".join(sorted(line))]
    return wl

def sliceup(word, min_len = 4, max_len = 29):
    for start in range(len(word) - min_len):
        for stop in range(start + min_len, min(len(word) + 1, start + max_len)):
            yield(word[start:stop])
    
def main():
    """A humble attempt to solve Mopub's PrettyPrettyPrinting developer
    challenge: http://www.mopub.com/about/coding-challenges/"""
    parser = argparse.ArgumentParser(
        description = 'Complete PrettyPrettyPrinter challenge!')
    parser.add_argument('-d', type=str, default='mowords.txt',
        dest='dictionary', required=0, help='path to dictionary file')
    parser.add_argument('-s', type=str, dest='string', required=1,
        help='string to use or path to string file')
    args = parser.parse_args()

    if(os.path.exists(args.string)):
        fh = open(args.string, 'r') 
        args.string = fh.read()
    
    wl = prep_wordlist(open(args.dictionary))
    print wl["act"]

if __name__ == "__main__":
    main()
