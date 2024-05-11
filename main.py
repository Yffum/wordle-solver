import Tester
from GameManager import GameManager
from DataManager import DataManager
from constants import AGENT_TYPES, SINGLE_TEST_WORD

import sys

""" This file runs the Wordle Solver """


def test_wordle(data: DataManager, agent_type: str, test_length: int):
    """ Runs series of tests using given search type
    Args:
        agent_type (str): The type of search: ('brute', 'csp', 'bfs', 'dfs', 'greedy', 'astar')
        test_length (int): The number of games to run tests on
    """
    # Check for single test word
    if SINGLE_TEST_WORD != None:
        Tester.run(agent_type, [SINGLE_TEST_WORD], data)
    else: 
        test_words = data.get_random_answers(test_length)
        Tester.run(agent_type, test_words, data)
    
    
def print_how_to():
    print("Run the program with two arguments like so:")
    print("$python main.py <agent_type> <test_length>")
    print("    <agent_type>  - The search agent type (brute, csp, bfs, dfs, greedy, astar)")
    print("    <test_length> - The number of games to solve (1 to 1000)")


def main():
    # Get system arguments
    args = sys.argv

    # Check number of arguments
    if len(args) != 3:
        print_how_to()
        return
    
    # Check arguments
    agent_type = args[1]
    test_length =  int(args[2])
    
    if (agent_type not in AGENT_TYPES
        or test_length < 1
        or test_length > 1000):
        print_how_to()
        return
    
    # Run tests
    data = DataManager()
    test_wordle(data, agent_type, test_length)
    

if __name__ == '__main__':
    main()
    
