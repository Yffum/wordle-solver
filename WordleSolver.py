import DataProcessing
import Tester
from SearchAgent import SearchAgent
from BruteSearchAgent import BruteSearchAgent
from TreeSearchAgent import TreeSearchAgent

class WordleSolver:
    """ This class manages the entire program. """
    def __init__(self):
        self.lexicon = set()
        self.letter_probs = []
        self.update_lexicon()
        
        
    def update_lexicon(self):
        """ Updates the currently used lexicon, and the letter probability distribution """
        self.lexicon = DataProcessing.import_lexicon()
        self.letter_probs = DataProcessing.calculate_letter_probability_distribution(self.lexicon)



def main():
    wordle = WordleSolver()
    
    # ToDo: SET THE SEARCH AGENT HERE
    
    # To add new agent type, have the agent's class inherit SearchAgent and implement the
    # abstract methods. Then add a condition for the new agent type to create_search_agent() 
    # in Tester.py
    
    # Types
    # {'brute', 'bfs', 'dfs'}
    agent_type = 'bfs'
    #agent_type = 'dfs'
    #agent_type = 'csp'
    #agent_type = 'astar'


    Tester.run(agent_type, wordle.lexicon, wordle.letter_probs)
    
    

if __name__ == '__main__':
    main()
    
    
    
    # Not in use yet
        # # A list of commands and their descriptions
        # self.commands = [('play', 'Play Wordle without using the solver.'),
        #                  ('solve', 'Use the Wordle solver.')]

        # self.solve_commands = [('brute', 'Searches every word in the lexcion.'),
        #                        ('BFS', 'Searches using a breadth-first search'),
        #                        ('DFS', 'Searches using a depth-first search')]