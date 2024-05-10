import Tester
from SearchAgent import SearchAgent
from BruteSearchAgent import BruteSearchAgent
from TreeSearchAgent import TreeSearchAgent
from StartWordFinder import StartWordFinder

from DataManager import DataManager

""" This file runs the program"""




def main():
    data = DataManager()
    
    print(data.start_words)
    
    # ToDo: SET THE SEARCH AGENT HERE
    
    # To add new agent type, have the agent's class inherit SearchAgent and implement the
    # abstract methods. Then add a condition for the new agent type to create_search_agent() 
    # in Tester.pys
    
    # Types
    # {'brute', 'bfs', 'dfs'}
    agent_type = 'astar'
    #agent_type = 'csp'

    test_words = data.get_random_answers(100)
    Tester.run(agent_type, test_words, data)
    
    

if __name__ == '__main__':
    main()
    
    
    
    # Not in use yet
        # # A list of commands and their descriptions
        # self.commands = [('play', 'Play Wordle without using the solver.'),
        #                  ('solve', 'Use the Wordle solver.')]

        # self.solve_commands = [('brute', 'Searches every word in the lexcion.'),
        #                        ('BFS', 'Searches using a breadth-first search'),
        #                        ('DFS', 'Searches using a depth-first search')]