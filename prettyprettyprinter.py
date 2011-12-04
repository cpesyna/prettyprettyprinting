#!/usr/bin/python2

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
    f = open("mowords.txt")
    wl = prep_wordlist(f)
    for item in wl["cat"]:
        print(item)

if __name__ == '__main__':
    main()
