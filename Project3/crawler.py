import requests
import re, string
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

class WebCrawler:
    """
    Implements a number of methods to facilitate crawling webpages in the utk.edu domain.

    Getter and setter methods for getting and setting links and documents. Mostly unused and
    exist to meet project specification. collect() method for scraping links from webpages,
    crawl() method for scraping text from collected webpages, and clean() method for modifying
    scraped text to be used in tfidf training, performed in engine.py.
    """

    def __init__(self, root, verbosity, depth):
        """
        Constructor that saves root url, verbosity, depth, and collected/crawled base values as member variables.

        Called when instance is created in engine.py, SearchEngine's constructor.

        @param root: root url to begin web crawling. verbosity: determines debugging output T/F. depth: layer of links to explore.
        @return N/A
        """
        self.root = root
        self.verbosity = verbosity
        self.depth = depth
        self.collected = 1
        self.crawled = 0
    
    def get_documents(self):
        """
        Getter method to retrieve list of cleaned documents.

        Cleaned documents are created in clean().

        @param N/A
        @return list of cleaned documents.
        """
        return self.cleaned_docs

    def set_documents(self, d):
        """
        Setter method to set list of cleaned documents.

        Cleaned documents are created in clean().

        @param d: list of strings representing cleaned documents.
        @return N/A
        """
        self.cleaned_docs = d

    def get_links(self):
        """
        Getter method to retrieve list of links collected in collect().

        Links, represented as urls, are collected in collect().

        @param N/A
        @return list of links.
        """
        return self.links

    def set_links(self, l):
        """
        Setter method to set list of links collected in collect().

        Links, represented as urls, are collected in collect().

        @param l: list of links collected in collect().
        @return N/A
        """
        self.links = l
    
    def collect(self, s, d):
        """
        Collect all links from root link s, as well as every link from those links up to depth d.

        If d = 0, only collect links on the root s's page. Collect links from each link up to depth d.

        @param s: root url to collect links from. d: depth to collect links from.
        @return N/A
        """
        if self.verbosity == 'T':
            print('collect(): [VERBOSE] 1. COLLECTING LINKS - STARTED')

        hdr = {'User-Agent': 'Mozilla/5.0'}

        self.link_level = [[s]]
        
        if self.verbosity == 'T':
            print('collect(): [VERBOSE] COLLECTED: LINK (1)')

        depth = 0

        while depth <= d: 
            self.link_level.append([])

            for link in self.link_level[depth]:
                req = Request(link, headers=hdr)
                
                try:
                    page = urlopen(req)
                except HTTPError as err:
                    #print(err.code)
                    #print('Error on link: ' + link)
                    continue
                except URLError as uerr:
                    #print('Error on link: ' + link)
                    continue

                soup = BeautifulSoup(page, 'html.parser')

                # find all links in HTML <a> fields
                for i in soup.find_all('a'):
                    # if a valid href field leading to http or https link in utk.edu domain, check if it has been collected yet
                    if i.get('href') != None and i.get('href').startswith('http') and 'utk.edu' in i.get('href'):
                        unique = True
                        for level in self.link_level:   
                            if i.get('href') in level or i.get('href')[:-1] in level:
                                unique = False
                                break
                        
                        # if it hasn't been collected, add it to the list of collected links
                        if unique:
                            self.collected += 1
                            if self.verbosity == 'T':
                                print('collect(): [VERBOSE] COLLECTED: LINK (' + str(self.collected) + ')')
                            self.link_level[depth + 1].append(i.get('href'))

            depth += 1

        if self.verbosity == 'T':
            print('collect(): [VERBOSE] 1. COLLECTING LINKS - DONE')

        # create a flattened list of links so indices of links corresponds to documents scraped
        links = []

        for level in self.link_level:
            for link in level:
                links.append(link)

        self.set_links(links)
        
    def crawl(self):
        """
        Scrape all <p> elements inside <div> elements with class attributes 'entry-content' or 'person_content'.

        Collect all text from above listed elements and save them as 'documents' associated with a url. Also scrapes
        from <table> elements that have 'table_default' as class attribute.

        @param N/A
        @return N/A
        """
        if self.verbosity == 'T':
            print('crawl(): [VERBOSE] 2. CRAWLING LINKS - STARTED')

        self.docs = []

        hdr = {'User-Agent': 'Mozilla/5.0'}

        # scrape from all collected links
        for level in self.link_level:
            for link in level:
                self.docs.append('')

                self.crawled += 1
                if self.verbosity == 'T':
                    print('crawl(): [VERBOSE] CRAWLING: LINK (' + str(self.crawled) + '/' + str(self.collected) + ')')
        
                req = Request(link, headers=hdr)
                
                try:
                    page = urlopen(req)
                except HTTPError as err:
                    #print(err.code)
                    #print('Error on link: ' + link)
                    continue
                except URLError as uerr:
                    #print('Error on link: ' + link)
                    continue

                soup = BeautifulSoup(page, 'html.parser')

                # append each scraped string to this link's associated document

                # check all tables from current link
                for i in soup.find_all('table', {'class':'table_default'}):
                    for j in i.find_all('td'):
                        self.docs[self.crawled - 1] += j.text + ' ' #str(j.renderContents()) + ' '

                # check all divs of these class attributes from current link
                for i in soup.find_all('div', {'class':['entry-content', 'person_content']}):
                    for j in i.find_all('p'):
                        self.docs[self.crawled - 1] += i.text + ' '
        
        if self.verbosity == 'T':
            print('crawl(): [VERBOSE] 2. CRAWLING LINKS - DONE')

    def clean(self):
        """
        Clean all text scraped with crawl() for use in tfidf training.

        Remove all unicode characters, all punctuation, all Twitter handles, all instances
        of double-spaces, and convert all character to lowercase.

        @param N/A
        @return N/A
        """
        if self.verbosity == 'T':
            print('clean(): [VERBOSE] 3. CLEANING TEXT - STARTED')

        cleaned_docs = []

        # clean every document scraped in crawl()
        for d in self.docs:
            # remove unicode by encoding/decoding
            d_temp = str(d).encode('ascii', 'ignore')
            d_temp = d_temp.decode()
            
            d_temp = d_temp.lower()
            d_temp = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', d_temp)
            d_temp = re.sub('@[\w]+', '', d_temp)                       
            ' '.join(d_temp.split())
            cleaned_docs.append(d_temp)

        self.set_documents(cleaned_docs)

        if self.verbosity == 'T':
            print('clean(): [VERBOSE] 3. CLEANING TEXT - DONE')
