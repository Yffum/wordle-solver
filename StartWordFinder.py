
from collections import Counter
import queue



class StartWordFinder:
    """ Tool for finding a sequence of start words to eliminate/confirm as many characters
        as possible, without trying to guess the answer. This is a preprocessing tool, that
        can be run once without simulating Wordle, and the determined sequence of start
        words can be used every game. """
        
    def __init__(self, vocab:set, letter_probs:Counter):
        # The set of possible guess words
        self.vocab = vocab
        # The normalized frequencies of each letter in the possible answers
        self.letter_probs = letter_probs
        # The set of letters already eliminated or confirmed
        self.processed_letters = set()
    
    
    def get_start_words(self, first_word:str = None, max_length:int = 100) -> list[str]:
        """ Returns a sequence of start words
                max_length - the maximum length of the returned list
                first_word - option to manually set first word """
        start_words = list()
        # If first word is given, add it to sequence and track the chars
        if first_word is not None:
            # Add word to sequence
            start_words.append(first_word)
            # Track processed letters
            for char in first_word:
                self.processed_letters.add(char)
            # Decrement remaining length of sequence
            max_length -= 1
        
        # Iteratively find sequence of best words while eliminating chars
        for i in range(max_length):
            # Get best word
            word = self.get_best_word()
            # Stop searching if no word is found 
            if word is None:
                break
            # Track letters
            for char in word:
                self.processed_letters.add(char)
            # Add word to sequence
            start_words.append(word)
        
        # Return sequence
        return start_words
        
        
    def get_best_word(self) -> str:
        """ Returns the word in the vocabulary which eliminates or confirms the most chars """
        # Use priority queue to get best word quickly
        scored_words = queue.PriorityQueue()
        # Rate every word in vocab
        for word in self.vocab:
            score = 0
            prev_chars = set()
            for char in word:
                # If char is already eliminated/confirmed, skip word
                if char in self.processed_letters:
                    score = 0
                    break
                # Increase score by each letter's probability, not counting duplicates
                if char not in prev_chars:
                    score += self.letter_probs[char]
                prev_chars.add(char)
            # Skip words with 0 score
            if score > 0:
                # Use negative score because PriorityQueue is a min heap
                scored_words.put((-score, word))
        # Return None if no word is found
        if scored_words.empty():
            return None
        # Get best word from priority queue
        best_score, best_word = scored_words.get()
        return best_word
        