import random

import DataProcessing
from StartWordFinder import StartWordFinder

class DataManager:
    """ This class manages data that is initialized when starting the program 
        and then used every game. """
    def __init__(self):
        # All words that can be guessed (including possible answers)
        self.guess_words = set()
        # Words that can be answers (subset of guess_words)
        self.answer_words = set()
        # List of counters. Index of counter corresponds to the position of
        # the char in the word. The keys are the letters of the alphabet and the
        # counts are the probabilities each letter appears in it's corresponding position
        self.letter_probs = []
        # Sequence of words to guess first
        self.start_words = list()
        self.set_data()
        
    def set_data(self):
        """ Sets internal word sets from file and calculates letter probabilities """
        # Set data from file
        self.guess_words = DataProcessing.import_lexicon('Data/wordle_lexicon.txt')
        self.answer_words = DataProcessing.import_lexicon('Data/valid_solutions.csv')
        
        # Calculate letter probabilities with respect to each position in the word
        self.letter_probs = DataProcessing.calculate_letter_probability_distribution(self.answer_words)
        
        # Determine sequence of initial guesses using StartWordFinder
        general_letter_probs = DataProcessing.get_general_letter_probabilities(list(self.answer_words))
        word_finder = StartWordFinder(self.guess_words, general_letter_probs)
        self.start_words = word_finder.get_start_words() # Try 'AUDIO', 'ADIEU' as first words
             
    def get_random_answers(self, length: int) -> list:
        """ Returns a list of the given length with random answer words. """
        return random.sample(list(self.answer_words), length)
        
