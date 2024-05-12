import random

import DataProcessing
from StartWordFinder import StartWordFinder
from constants import FIRST_GUESS

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
        self.answer_words_ordered = DataProcessing.import_lexicon_as_list('Data/valid_solutions_ordered.csv')
        
        # Calculate letter probabilities with respect to each position in the word
        self.letter_probs = DataProcessing.calculate_letter_probability_distribution(self.answer_words)
        
        # Determine sequence of initial guesses using StartWordFinder
        general_letter_probs = DataProcessing.get_general_letter_probabilities(list(self.answer_words))
        word_finder = StartWordFinder(self.guess_words, general_letter_probs)
        self.start_words = word_finder.get_start_words(FIRST_GUESS)
             
    def get_random_answers(self, length: int) -> list:
        """ Returns a list of the given length with random answer words. """
        return random.sample(list(self.answer_words), length)

    def get_specific_answers(self, length: int, test_mode: str) -> list:
        """ Return a list of the given length with easy and hard words. """
        sorted_list = []
        total_len = len(self.answer_words_ordered) - 1
        for i in range (length):
            if test_mode == 'easy':
                sorted_list.append(self.answer_words_ordered[i])
            else:
                sorted_list.append(self.answer_words_ordered[total_len - i])

        
        return sorted_list

    def get_answers(self, length: int, test_mode:str) -> list:
        if(test_mode == 'random'):
            return self.get_random_answers(length)
        else:
            return self.get_specific_answers(length, test_mode)        
