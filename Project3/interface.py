class SearchInterface:
    """
    Implements methods that create an interface for interacting with EECS search engine.

    listen() method for prompting for user input, unless "Command Mode" is specified, in
    which case the provided query is passed to the engine. handle_input() method routes
    commands to appropriate handlers; handles commands such as :train, :delete, and :exit.
    """
    
    def __init__(self, mode, engine, query):
        """
        Constructor that saves mode, engine that created this interface, and query passed in command mode.

        Called when instance is created in engine.py, SearchEngine's constructor.

        @param mode: command or interactive mode. engine: engine instance that instantiated this class. query: query provided in command mode.
        @return N/A
        """
        self.mode = mode
        self.engine = engine
        self.query = query

    def listen(self):
        """
        Method that prompts for user input in interactive mode.

        Simply sends query to engine in command mode, but prompts for queries in interactive mode. Also routes
        administrative commands.

        @param N/A
        @return N/A
        """
        # command mode
        if self.mode == 'C':
            self.engine.handle_query()
        
        # interactive mode
        elif self.mode == 'I':
            print('-----------------------------------')
            print('|         UTK EECS SEARCH         |')
            print('-----------------------------------')
            
            # prompt for input and send it to handle_input()
            while True:
                self.query = input('> ')
                self.handle_input()
    
    def handle_input(self):
        """
        Handle input passed from listen().

        :delete calls SearchEngine's delete() that removes all pickle files, :train calls SearchEngine's train() to perform
        tfidf training (potentially calling collect(), crawl(), and clean()), and :exit exits the program. Queries are sent
        to SearchEngine's handle_query.

        @param N/A
        @return N/A
        """
        if self.query == ':delete':
            self.engine.delete()

        elif self.query == ':train':
            self.engine.train()

        elif self.query == ':exit':
            exit()

        else:
            self.engine.query = self.query
            self.engine.handle_query()
