from crawler import WebCrawler
from interface import SearchInterface
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import pandas as pd
import numpy as np
import pickle

class SearchEngine:
    """
    Manages a terminal search engine that conducts tfidf training on text scraped from wepages in the utk.edu domain.

    Constructor instantiates and uses WebCrawler and SearchInterface objects to collect data and accept queries from user.
    Contains a number of methods to conduct tfidf training and access/store/delete the results.
    """
    
    def __init__(self, mode, verbosity, query, root, depth):
        """
        Constructor that saves parameters as member variables, instantiates crawler and interface objects, then begins tfidf training.

        Called when instance is created in main.py.

        @param root: mode: take query from command line or from interactive terminal. verbosity: determines debugging output T/F.
               query: search term from command line. root: root url to begin web crawling. depth: layer of links to explore.
        @return N/A
        """
        self.mode = mode
        self.verbosity = verbosity
        self.query = query
        self.root = root
        self.depth = depth

        self.crawler = WebCrawler(root, verbosity, depth)
        self.interface = SearchInterface(mode, self, query)

        self.train()
        self.listen()

    def train(self):
        """
        Method that runs collect(), crawl(), and clean() if needed, otherwise loads data from pickle files then computes tfidf.

        If links.pickle and docs.pickle already exist, this method simply loads the data then computes tfidf. If those files do
        not exist, then they are created after collect(), crawl(), and clean run.

        @param N/A
        @return N/A
        """
        try:
            with open('links.pickle', 'xb') as f:
                self.crawler.collect(self.root, self.depth)
                pickle.dump(self.crawler.get_links(), f)
        except FileExistsError:
            with open('links.pickle', 'rb') as f:
                self.crawler.set_links(pickle.load(f))
        
        try:
            with open('docs.pickle', 'xb') as f:
                self.crawler.crawl()
                self.crawler.clean()
                pickle.dump(self.crawler.get_documents(), f)
        except FileExistsError:
            with open('docs.pickle', 'rb') as f:
                self.crawler.set_documents(pickle.load(f))

        self.compute_tf_idf()

    def delete(self):
        """
        Method that deletes data files links.pickle and docs.pickle.

        This is called when user inputs ':delete' in interactive mode.

        @param N/A
        @return N/A
        """
        if os.path.exists('links.pickle'):
            os.remove('links.pickle')
        
        if os.path.exists('docs.pickle'):
            os.remove('docs.pickle')                                                            
    
    def compute_tf_idf(self):
        """
        Read the cleaned documents and vectorizes the documents using Scikit-Learn's TfidfVectorizer.

        Resulting dataframe has the TFIDF vocabulary as the index.

        @param N/A
        @return N/A
        """
        self.tfidf_vectorizer = TfidfVectorizer() 
        # Send our docs into the Vectorizer
        tfidf_vectorizer_vectors = self.tfidf_vectorizer.fit_transform(self.crawler.cleaned_docs)
        # Transpose the result into a more traditional TF-IDF matrix, and convert it to an array.
        X = tfidf_vectorizer_vectors.T.toarray()
        # Convert the matrix into a dataframe using feature names as the dataframe index.
        self.df = pd.DataFrame(X, index=self.tfidf_vectorizer.get_feature_names())

    def handle_query(self):
        """
        Vectorize the query, calculates the cosine similarity to extraced web documents, and prints up to five most related docs.

        Called by SearchInterface when it receives a query from the user in interactive mode, or once with the query provided in command mode.

        @param N/A
        @return N/A
        """
        # Vectorize the query.
        q = [self.query]
        q_vec = self.tfidf_vectorizer.transform(q).toarray().reshape(self.df.shape[0],)
    
        # Calculate cosine similarity.
        sim = {}
        for i in range(len(self.df.columns)):
            denom = np.linalg.norm(self.df.loc[:, i]) * np.linalg.norm(q_vec)
            if denom == 0:
                sim[i] = 0
            else:
                sim[i] = np.dot(self.df.loc[:, i].values, q_vec) / denom
    
        # Sort the values 
        sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)
    
        # Print the document number, associated url, and their similarity values
        # 'Document number' wasn't really clear, so I just printed the number in order of most similar (most similar 1, least similar 5)
        printed = 0
        for k, v in sim_sorted:
            if v != 0.0 and not pd.isna(v):
                print('[' + str(printed + 1) + '] ' + self.crawler.links[k] + ' (' + str('{:.2f}'.format(v)) + ')')
                printed += 1
                if(printed == 5):
                    break
        
        if printed == 0:
            print('Your search did not match any documents. Try again.')

    def listen(self):
        """
        Method simply calls the SearchInterface's listen method for receiving user input.

        In command mode, query comes from command line. In interactive mode, user continually supplies queries or administrative commands.

        @param N/A
        @return N/A
        """
        self.interface.listen()
