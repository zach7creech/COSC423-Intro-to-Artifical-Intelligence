This program is a simple search engine in the terminal that returns webpages from the utk.edu domain relevant to a user's query using
BeautifulSoup4 and urllib3 to scrape webpages and Scikit-Learn and Pandas to perform TFIDF vectorization, then calculate cosine similarity.
In interactive mode, the user is prompted for queries in a terminal interface. This terminal interface also accepts administrative commands.
The program is split into four files: main.py that processes command line arguments and creates the engine; engine.py that implements
the SearchEngine class; crawler.py that implements the WebCrawler class; and interface.py that implements the SearchInterface class.

To run this code locally in a Unix environment, place 'main.py', 'engine.py', 'crawler.py', and 'interface.py' in the same directory. In a
terminal, within that directory, run the following command: 'python3 main.py -root <url> -mode <mode> -query <search query> -verbose <verbosity>'
The order of commands does not matter. -root and -mode are required arguments, where <url> is the root link to begin collecting links from and
<mode> is either 'C' or 'I'; 'C' is command mode and the query is taken from command line arguments, 'I' is interactive mode and will create a
terminal interface to continually receive queries and administrative commands from the user. Administrative commands are ':train' to collect
links and data from specified root and compute tfidf, ':delete' to remove any saved links or docs (links.pickle and docs.pickle), and ':exit' to
exit the program. -query is required if -mode 'C' is specified, and -verbose is required if -mode 'I' is specified. <search query> is a string
to be searched for in the root domain. To use a string separated by spaces, simply encapsulate the strings in ' '. In interactive mode, this is
unnecessary. <verbosity> is either 'T' or 'F' and determines if debugging information will be printed. If 'T' then extra information regarding
activities of collect(), crawl(), and clean() will be printed to the terminal interface as the webpages are scraped.
