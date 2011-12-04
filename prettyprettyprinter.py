import argparse
import os.path
import sys

def main():
    parser = argparse.ArgumentParser(
        description = 'Complete PrettyPrettyPrinter challenge!')
    parser.add_argument('-d', type=str, default='mowords.txt', nargs=1,
        dest='dictionary', required=0, help='path to dictionary file')
    parser.add_argument('-s', type=str, dest='string', required=1,
        help='string to use or path to string file')
    args = parser.parse_args()
    if(os.path.exists(args.string)):
        fh = open(args.string, 'r') 
        args.string = fh.read()
    
if __name__ == "__main__":
    main()
