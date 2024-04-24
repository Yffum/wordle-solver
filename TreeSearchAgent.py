from GameManager import WORD_LENGTH, ALPHABET

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



class TreeSearchAgent:
    """ A SearchAgent must be instantiated with a vocabulary of words it can guess, 
        and a letter probability distribution (a list of Counters), from which it 
        calculates its guesses. A new agent should be instantiated for each game, as 
        the vocab and probability distribution are adjusted each search. """
    def __init__(self, vocab: set, letter_probability_distribution: list):
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
        # Words to be removed from the vocab after iterating through the vocab
        self.words_to_remove = set()
        # Starting word for tree search, copied from brute force search's first guess
        self.root_word = 'SORES'
        # Agent guesses the first word found with a score above the threshold
        self.score_threshold = 0


    def adjust_letter_probs(self, guess: str, letter_ratings: list):
        """ Takes a guess and its corresponding ratings, and updates
            letter_probs for each character in the guess. """
        # Track letters that are in the word, but we don't know the position
        new_known_letters = Counter()
        # Check every char and corresponding rating
        for i, rating in enumerate(letter_ratings):
            char = guess[i]
            # If letter is correct, set probability to 1
            if rating == '2':
                # If letter was known without position, remove it from the tracker
                if char in self.known_letters:
                    self.known_letters[char] -= 1
                # Track confirmed letter
                self.confirmed_letters[i] = char
                # Set proability to 1
                self.letter_probs[i][char] = 1
            # If letter is known, but in the wrong position, track it
            elif rating == '1':
                new_known_letters[char] += 1
            # If letter is incorrect, set probability to 0
            elif rating == '0':
                self.letter_probs[i][char] = 0
                # Adjust probabilities of other positions to 0
                # ToDo: I'm not sure whether this accounts for all edge cases
                # Make sure letter is not already known (without position)
                if char not in new_known_letters:
                    # Loop through probability tables for every char position
                    for table in self.letter_probs:
                        # Make sure letter is not already known (with position)
                        if table[char] != 1:
                            # Set probability to 0
                            table[char] = 0
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
        # Make sure word is a legal
        if word not in self.vocab:
            return 0

        # For each character
        for i, char in enumerate(word):
            # Get probability
            prob = self.letter_probs[i][char]
            # If any letter prob is 0, then the entire word score is 0
            if prob == 0:
                # Remove word from vocab after iterating through it
                self.words_to_remove.add(word)
                return 0
            
            # Increase probability if letter is known
            factor = 1/WORD_LENGTH # chance to be in that position
            prob += factor * self.known_letters[char]
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
            # Try changing the char to each letter in alphabet
            for letter in ALPHABET:
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
        base_threshold = 0.7
        increase_factor = 0.3
        
        # Calculate threshold using linear function on confirmed letter count
        threshold = base_threshold + increase_factor * len(self.confirmed_letters)
        return threshold
        
        
    def tree_search(self) -> str:
        # Track words already parsed
        prev_words = set()

        # Create fringe
        fringe = queue.LifoQueue()
        # Create and insert root
        root = Node(self.root_word)
        fringe.put(root)

        # While there are nodes in the fringe
        while not fringe.empty():
            # Get node from fringe
            node = fringe.get()
            # If the node's score is above the threshold
            if self.get_score(node.word) > self.score_threshold:
                # Adjust root node for next search
                self.root_word = node.word
                # Remove impossible words from vocab
                self.vocab -= self.words_to_remove
                self.words_to_remove.clear()
                # Remove guess from vocab
                self.vocab.remove(node.word)
                # Guess word
                return node.word
            # Else expand node
            successors = self.expand(node, prev_words)
            # Add successors to fringe
            for succ_node in successors:
                fringe.put(succ_node)
        # No word was found outside the threshold
        print("No word found with score above threshold")
        return None
        
        
    def tree_search_with_threshold(self) -> str:
        # The threshold decreases by this amount when the search fails
        threshold_decrement = 0.2
        # Calculate word score threshold based on number of confirmed letters
        self.score_threshold = self.get_threshold()
        # Repeat tree search while lowering threshold
        threshold_can_decrease = True
        while threshold_can_decrease:
            guess = self.tree_search()
            # Search succeeded, return guess
            if guess is not None:
                return guess
            # Search failed, check if threshold can decrease
            if self.score_threshold < 0:
                # Break, no guess found
                threshold_can_decrease = False
            else:
                # Decrease threshold
                self.score_threshold -= threshold_decrement
        print("No guess found")
            
        

    