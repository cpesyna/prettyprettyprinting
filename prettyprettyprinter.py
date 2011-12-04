#!/usr/bin/python2

import argparse
import os.path
import sys
from collections import defaultdict

def lookup(word, wl):
    """Stupid hack. Lookup subclassing defaultdict and overriding __getitem__"""
    try:
        return wl["".join(sorted(word))]
    except KeyError:
        return False

def prep_wordlist(wl_file):
    wl = worddict(list)
    for line in wl_file:
        line = line.strip()
        wl["".join(sorted(line))].append(line)
    return wl

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
    
    wl = prep_wordlist(args.dictionary)
    for item in wl["cat"]:
        print(item)

if __name__ == "__main__":
    main()
