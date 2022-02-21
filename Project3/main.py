"""
Author: Zachery Creech.

This program is a simple search engine in the terminal that returns webpages from the utk.edu domain relevant to a user's query using
BeautifulSoup4 and urllib3 to scrape webpages and Scikit-Learn and Pandas to perform TFIDF vectorization, then calculate cosine similarity.
In interactive mode, the user is prompted for queries in a terminal interface. This terminal interface also accepts administrative commands.
The program is split into four files: main.py that processes command line arguments and creates the engine; engine.py that implements
the SearchEngine class; crawler.py that implements the WebCrawler class; and interface.py that implements the SearchInterface class.
"""

import sys
import argparse

from engine import SearchEngine

def main():
    """
    Perform argument parsing and instantiate the SearchEngine driver class.

    Argument parsing is performed with argparse library, but not all functionality of the library is utilized so that particular error
    messages exactly match the format provided in the writeup.

    @param N/A
    @return N/A
    """
    if '-root' not in sys.argv or '-mode' not in sys.argv:
        print('ERROR: Missing required arguments')
        exit()

    parser = argparse.ArgumentParser()

    parser.add_argument('-root')
    parser.add_argument('-mode')
    parser.add_argument('-query')
    parser.add_argument('-verbose')

    args = parser.parse_args()

    if not args.root.startswith('http') and not args.root.startswith('https'):
        print('ERROR: Invalid arguments provided')
        exit()

    if args.mode != 'C' and args.mode != 'I':
        print('ERROR: Invalid arguments provided')
        exit()

    if args.mode == 'C' and args.query == None:
        print('ERROR: Missing query argument')
        exit()

    if args.mode == 'I' and args.verbose == None:
        print('ERROR: Missing verbose argument')
        exit()

    if args.verbose != None:
        if args.verbose != 'T' and args.verbose != 'F':
            print('ERROR: Invalid arguments provided')
            exit()

    main_engine = SearchEngine(args.mode, args.verbose, args.query, args.root, 1)

if __name__ == '__main__':
    main()
