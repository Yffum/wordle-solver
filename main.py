import DataProcessing
import Tester
from SearchAgent import SearchAgent
from BruteSearchAgent import BruteSearchAgent
from TreeSearchAgent import TreeSearchAgent

import random

""" This file runs the program"""


class DataManager:
    """ This class manages data that is initialized when starting the program 
        and then used every game. """
    def __init__(self):
        self.guess_words = set()
        self.answer_words = set()
        self.letter_probs = []
        self.set_data()
        
    def set_data(self):
        """ Sets internal word sets from file and calculates letter probabilities """
        self.guess_words = DataProcessing.import_lexicon('Data/wordle_lexicon.txt')
        self.answer_words = DataProcessing.import_lexicon('Data/valid_solutions.csv')
        
        self.letter_probs = DataProcessing.calculate_letter_probability_distribution(self.guess_words)
        
    def get_random_answers(self, length: int) -> list:
        """ Returns a list of the given length with random answer words. """
        return random.sample(list(self.answer_words), length)
        


def main():
    data = DataManager()
    
    # ToDo: SET THE SEARCH AGENT HERE
    
    # To add new agent type, have the agent's class inherit SearchAgent and implement the
    # abstract methods. Then add a condition for the new agent type to create_search_agent() 
    # in Tester.py
    
    # Types
    # {'brute', 'bfs', 'dfs'}
    agent_type = 'bfs'
    #agent_type = 'csp'

    test_words = data.get_random_answers(10)
    Tester.run(agent_type, test_words, data.guess_words, data.letter_probs)
    
    

if __name__ == '__main__':
    main()
    
    
    
    # Not in use yet
        # # A list of commands and their descriptions
        # self.commands = [('play', 'Play Wordle without using the solver.'),
        #                  ('solve', 'Use the Wordle solver.')]

        # self.solve_commands = [('brute', 'Searches every word in the lexcion.'),
        #                        ('BFS', 'Searches using a breadth-first search'),
        #                        ('DFS', 'Searches using a depth-first search')]