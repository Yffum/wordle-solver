from constants import WORD_LENGTH, ALPHABET
from SearchAgent import SearchAgent
from OrderedSet import OrderedSet

from collections import Counter
import queue
import copy


class  Node:
    """ Nodes contain a word which might be guessed """
    def __init__(self, word: str, prev_node: 'Node'=None):
        # The content of a node is this potential guess word
        self.word = word
        self.prev = prev_node
        self.depth = 0

        # Get depth from previous node
        if self.prev != None:
            self.depth = self.prev.depth + 1
    def __lt__(self, other):
        # To make priority queues work:
        return False



class TreeSearchAgent(SearchAgent):
    """ A TreeSearchAgent must be instantiated with a vocabulary of words it can guess, 
        and a letter probability distribution (a list of Counters), from which it 
        calculates its guesses. A new agent should be instantiated for each game, as 
        the vocab and probability distribution are adjusted each search. """
    def __init__(self, vocab: set, letter_probability_distribution: list[Counter], mode: str='None'):
        # Words that can be guessed
        self.vocab = set(vocab)
        # List of adjusted letter probabilities
        self.letter_probs = copy.deepcopy(letter_probability_distribution)
        # These are letters that have a confirmed position in the answer. The key is
        # the index and the value is the char
        # Example: if confimered_letters == {0: 'e', 3: 's'} then the agent knows 
        #          the first letter in the answer is 'e' and the fourth is 's'
        self.confirmed_letters = dict()
        # These letters are known to be in the word, but we don't know the position
        self.known_letters = Counter()
        # Starting word for tree search
        self.root_word = 'AUDIO'
        # Agent guesses the first word found with a score above this threshold
        self.score_threshold = 0
        # Domains of possible letters for each character in the guess. Each element
        # corresponds to a char index, and contains the possible letters for that index.
        # Each domain starts with the entire alphabet and is refined after each guess.
        self.char_domains = [OrderedSet(ALPHABET) for _ in range(5)]
        # Tracks how many guesses the agent has already made
        self.guess_count = 0
        # Sequence of guesses to start with
        self.start_guesses = ['AUDIO', 'NERTS', 'LYMPH']
        
        # Default to simple tree search. The tree_search function returns the first word
        # it finds under score_threshold
        self.tree_search = self.simple_tree_search
        if mode == None:
            mode = 'bfs' # Default to BFS mode
            
        # Set the fringe and the tree search function based on the given mode
        if mode == 'bfs':     
            self.fringe = queue.Queue()
        elif mode == 'dfs':
            self.fringe = queue.LifoQueue()
        elif mode == 'greedy':
            self.fringe = queue.PriorityQueue()
            self.tree_search = self.greedy_tree_search
        elif mode == 'astar':
            self.fringe = queue.PriorityQueue()
            self.tree_search = self.astar_tree_search
        else:
            raise ValueError(f"Mode '{mode}' not found. Select from {'bfs', 'dfs', 'greedy', 'astar'}")
    
    
    # --- Define abstract methods
    # See SearchAgent.py
    def get_guess(self) -> str:
        # Increment guess count
        self.guess_count += 1
        guess = None
        # Use start_guesses first
        if self.guess_count <= len(self.start_guesses):
            guess = self.start_guesses[self.guess_count - 1]
        # Tree search
        else:
            guess = self.tree_search_with_threshold()
        # Adjust root node for next search
        self.root_word = guess
        # Remove guess from vocab
        self.vocab.discard(guess)
        # Return guess for the game
        return guess

    # See SearchAgent.py
    def process_feedback(self, guess: str, letter_ratings: list[int]):
        return self.adjust_letter_probs(guess, letter_ratings)
        
        
    def clear_fringe(self):
        """ Clears self.fringe by determining its datatype and re-instantiating """
        fringe_type = type(self.fringe)
        self.fringe = fringe_type()
        

    def adjust_letter_probs(self, guess: str, letter_ratings: list[int]):
        """ Takes a guess and its corresponding ratings, and updates
            letter_probs for each character in the guess. """
        # Track letters that are in the word, but we don't know the position
        new_known_letters = Counter()
        # Check every letter in the guess and its corresponding rating
        for i, rating in enumerate(letter_ratings):
            char = guess[i]
            # If letter is correct, set probability to 1
            if rating == '2':
                # If letter was known without position, remove it from the tracker
                if char in self.known_letters:
                    self.known_letters[char] -= 1
                    # Prevent negative values
                    if self.known_letters[char] < 0:        
                        self.known_letters[char] = 0
                # Track confirmed letter
                self.confirmed_letters[i] = char
                # Set proability to 1
                self.letter_probs[i][char] = 1
                # Restrict domain to this letter
                self.char_domains[i] = OrderedSet(char)
            # If letter is known, but in the wrong position, set prob to 0 and track it
            elif rating == '1':
                self.letter_probs[i][char] = 0
                new_known_letters[char] += 1
                # Remove letter from domain
                self.char_domains[i].discard(char)
            # If letter is incorrect, set probability to 0
            elif rating == '0':
                self.letter_probs[i][char] = 0
                # Remove letter from domain
                self.char_domains[i].discard(char)
                # Adjust probabilities of other positions and remove letter from 
                # char domains corresponding to those positions
                # ToDo: I'm not sure whether this accounts for all edge cases
                # Make sure letter is not already known (without position)
                if char not in new_known_letters:
                    # Loop through probability tables for every char position
                    for j, table in enumerate(self.letter_probs):
                        # Make sure letter is not already known (with position)
                        if table[char] != 1:
                            # Set probability to 0
                            table[char] = 0
                            # Remove letter from domain
                            self.char_domains[j].discard(char)
        # Add new known letters to persistent list
        for char, count in new_known_letters.items():
            # Only add if the count in the new list is greater
            # E.g., if the letter was not previously known, or if only 1 was known,
            # but now there are 2.
            if count > self.known_letters[char]:
                # Update count
                self.known_letters[char] = count


    def get_score(self, word: str) -> float:
        """ Returns a word score equal to the sum of the probability of each letter
            being in its respective position. """
        score = 0
        # Make sure word is in vocab
        if word not in self.vocab:
            return 0
        
        # Make sure confirmed letters are accounted for by removing each letter
        # from a list of chars in the word
        chars = list(word)
        for position, letter in self.confirmed_letters.items():
            if letter in chars:
                chars.remove(letter)
            else:
                # Not all confirmed letters are in the word
                return 0
        # Repeat with known letters
        for letter, count in self.known_letters.items():
            # Repeat for count of each letter
            for i in range(count):
                if letter in chars:
                    chars.remove(letter)
                else:
                    # Not all known letters are in the word
                    return 0            

        # For each character
        for i, char in enumerate(word):
            # Get probability
            prob = self.letter_probs[i][char]
            # If any letter prob is 0, then the entire word score is 0
            if prob == 0:
                return 0
            
            # ToDo: test with/without increasing factor
            # Increase probability if letter is known
            #factor = 1/WORD_LENGTH # chance to be in that position
            #prob += factor * self.known_letters[char]
            # Example: If we know a 5-letter word has 2 'a', then we increase the
            #          probability of 'a' in this position by 0.2 * 2 = 0.4

            # Add probability of character to score
            score += prob
        # Return rounded score
        return round(score, 3)


    def expand(self, node: Node, prev_words: set) -> list:
        """ Expands the given node, excluding words in prev_words. A list of the
            successor nodes is returned. Successor words are added to prev_words. """
        successors = []
        # For each character in the word
        for i, char in enumerate(node.word):
            # Skip confirmed letters
            if i in self.confirmed_letters:
                continue
            # Try changing the char to each letter in its domain
            for letter in self.char_domains[i]:
                # Make sure it's not the same letter
                if letter != char:
                    # Insert letter to make new word
                    new_word = node.word[:i] + letter + node.word[i+1:]
                    # Make sure word wasn't previously visited
                    if new_word not in prev_words:
                        # ToDo
                        #print('trying', new_word)
                        prev_words.add(new_word)
                        # Create node with new word and add to successor list
                        new_node = Node(new_word, node)
                        successors.append(new_node)
        return successors
    

    def get_threshold(self) -> float:
        """ Returns the word score threshold, which is calculated using a reciprocal 
            function that increases at a diminishing rate with respect to the number 
            of letters that have been confirmed so far """
        
        # -- Constants --
        # These values are tuned based on word score results from
        # brute force testing
        base_threshold = 0.5
        increase_factor = 2 * base_threshold
        
        # -- Independent Variable --
        # The threshold increases with respect to this number of confirmed letters
        confirm_count = len(self.confirmed_letters)
        
        # Base case
        if confirm_count == 0:
            return base_threshold
        
        # Calculate threshold using reciprocal function on confirmed letter count
        threshold = base_threshold + increase_factor * (1 - 1/confirm_count)
        return threshold
    
    
    def get_threshold_alt(self) -> float:
        """ Returns the word score threshold, which is calculated using a linear
            function that increases with respect to the number of letter that have
            been confirmed so far"""
        # -- Constants --
        base_threshold = 0.5
        increase_factor = 0.3
        
        # Calculate threshold using linear function on confirmed letter count
        threshold = base_threshold + increase_factor * len(self.confirmed_letters)
        return threshold
        
        
    def simple_tree_search(self) -> str:
        """ Performs a tree search and returns the first word it finds with 
            a score above self.score_threshold. Returns None if no word is
            found above the threshold. """
        # Track words already parsed
        prev_words = set()

        # Clear fringe
        self.clear_fringe()
        # Create root
        root = self.root_word
        # Insert confirmed letters into root word
        for i in self.confirmed_letters:
            # Replace letter at index i
            root = root[:i] + self.confirmed_letters[i] + root[i+1:]
        # Insert root into fringe
        root_node = Node(root)
        self.fringe.put(root_node)

        # While there are nodes in the fringe
        while not self.fringe.empty():
            # Get node from fringe
            node = self.fringe.get()
            # If the node's score is above the threshold
            if self.get_score(node.word) > self.score_threshold:
                # Guess word
                return node.word
            # Else expand node
            successors = self.expand(node, prev_words)
            # Add successors to fringe
            for succ_node in successors:
                self.fringe.put(succ_node)
        # No word was found outside the threshold
        print("No word found with score above threshold =", self.score_threshold)
        return None
    
    
    def greedy_tree_search(self) -> str:
        """ Performs a tree search using a priority queue and returns the first word 
            it finds with a score above self.score_threshold. Returns None if no word 
            is found above the threshold. The priority queue return the word with the
            highest score. """
        # Track words already parsed
        prev_words = set()

        # Clear fringe
        self.clear_fringe()
        # Create root
        root = self.root_word
        # Insert confirmed letters into root word
        for i in self.confirmed_letters:
            # Replace letter at index i
            root = root[:i] + self.confirmed_letters[i] + root[i+1:]
        # Insert root into fringe
        root_node = Node(root)
        # Use score of 0 for root node
        self.fringe.put((0, root_node))

        # While there are nodes in the fringe
        while not self.fringe.empty():
            # Get node from fringe
            score, node = self.fringe.get()
            # If the node's score is above the threshold (priority queue holds negative score)
            if -score > self.score_threshold:
                # Guess word
                return node.word
            # Else expand node
            successors = self.expand(node, prev_words)
            # Add successors to fringe
            for succ_node in successors:
                # Get word's score
                score = self.get_score(succ_node.word)
                # Store negative score because priority queue gets lowest
                self.fringe.put((-score, succ_node))
        # No word was found outside the threshold
        print("No word found with score above threshold =", self.score_threshold)
        return None
    
    
    def astar_tree_search(self) -> str:
        """ Performs a tree search using a priority queue and returns the first word 
            it finds with a score above self.score_threshold. Returns None if no word 
            is found above the threshold. """
        # Track words already parsed
        prev_words = set()
        
        def get_priority(node: Node, word_score: float) -> float:
            # This constant scales the difference between a current word's score and
            # the current score threshold in astar, in order to estimate the number
            # of nodes until a word above the threshold is reached
            H_SCALE = 1000
            heuristic = H_SCALE * (self.score_threshold - word_score)
            # Priority is depth + heuristic
            priority = node.depth + heuristic
            return priority

        # Clear fringe
        self.clear_fringe()
        # Create root
        root = self.root_word
        # Insert confirmed letters into root word
        for i in self.confirmed_letters:
            # Replace letter at index i
            root = root[:i] + self.confirmed_letters[i] + root[i+1:]
        # Insert root into fringe
        root_node = Node(root)
        # Use score of 0 for root node
        self.fringe.put((0, 0, root_node))
        
        # Note: the fringe stores (priority, score, node) so that score doesn't have
        # to be calculated again when checking if the node is in the threshold after
        # removing it from the fringe

        # While there are nodes in the fringe
        while not self.fringe.empty():
            # Get node from fringe
            _, score, node = self.fringe.get()
            # If the node's score is above the threshold (priority queue holds negative score)
            if score > self.score_threshold:
                # Guess word
                return node.word
            # Else expand node
            successors = self.expand(node, prev_words)
            # Add successors to fringe
            for succ_node in successors:
                # Get word's score and calculate priority using heuristic
                score = self.get_score(succ_node.word)
                priority = get_priority(succ_node, score)
                # Push to fringe
                self.fringe.put((priority, score, succ_node))
        # No word was found outside the threshold
        print("No word found with score above threshold =", self.score_threshold)
        return None
        
    def tree_search_with_threshold(self) -> str:
        """ Repeatedly performs self.tree_search() while lowering the threshold until
            a word is found, or the threshold can't be lowered. Returns the found word,
            or None if no word is found. """
        # The threshold decreases by this amount when the search fails
        threshold_decrement = 0.3
        
        # If any letters have been confirmed
        if len(self.confirmed_letters) > 0:
            # Calculate new threshold based on number of confirmed letters
            self.score_threshold = self.get_threshold_alt()
        else:
            # Starting threshold
            self.score_threshold = 0.1
        
        # Repeat tree search while lowering threshold
        threshold_can_decrease = True
        while threshold_can_decrease: 
            guess = self.tree_search()
            # Search succeeded, return guess
            if guess is not None:
                return guess
            # Search failed
            # If threshold cannot decrease
            if self.score_threshold == 0:
                # Break, no guess found
                threshold_can_decrease = False
            else:
                # Decrease threshold
                self.score_threshold -= threshold_decrement
                # Prevent negative threshold
                if self.score_threshold < 0:
                    self.score_threshold = 0
        print("No guess found")
            
        

    