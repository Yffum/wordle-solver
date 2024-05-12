import DataProcessing
from GameManager import GameManager
from SearchAgent import SearchAgent
from BruteSearchAgent import BruteSearchAgent
from TreeSearchAgent import TreeSearchAgent
from CSPAgent import Dictionary
from CSPAgent import CSPSolver
from DataManager import DataManager

import time
from datetime import datetime
from collections import Counter
from ReportDataCollector import ReportDataCollector

def run(agent_type: str, test_words: list, data_manager:DataManager, test_mode:str):
    """ Run test() and record/report duration"""
    dataCollector = ReportDataCollector()

    # Record test time
    start_time = time.process_time()
    # Using lexicon as test set for now

    if(agent_type == 'csp'):
        # run basic CSP test routine
        data = test_csp(agent_type, test_words, data_manager.guess_words, dataCollector)
    else:
        # run 'brute', 'bfs', 'dfs' and 'ast'
        data = test(agent_type, test_words, data_manager, dataCollector)

    # Round duration to minutes
    duration = time.process_time() - start_time
    duration = round(duration/60, 2)
    
    # Write to file
    dataCollector.generateReportFile(agent_type, duration, test_mode)

    # Generate plot
    dataCollector.generateReportPlot()

    print("Total test duration:", duration, "minutes")

    

def create_search_agent(agent_type: str, lexicon: set, letter_probs: list[Counter], start_guesses: list[str]) -> SearchAgent:
    """ Creates a search agent of the given type. Vocabulary is built from given lexicon, and 
        word scoring is determined by the given letter probability distribution. """
    if agent_type == 'brute':
        return BruteSearchAgent(lexicon, letter_probs)
    if agent_type in ('bfs', 'dfs', 'greedy', 'astar'):
        # Pass agent type to tree agent to choose bfs/dfs/astar
        return TreeSearchAgent(lexicon, letter_probs, start_guesses, agent_type)
    # If agent_type isn't handled
    print("Error: agent_type", agent_type, "was not found.")



def test(agent_type: str, test_words: list, data_manager: DataManager, dataCollector: ReportDataCollector):
    """ Runs the solver using the given agent, using each word in test_set as the answer
        (so the number of games tested is equal to the length of test_set) """
    
    for i, word in enumerate(test_words):
        # Create new search agent of given type
        agent = create_search_agent(agent_type, data_manager.answer_words, data_manager.letter_probs, data_manager.start_words)
        # Create new game
        game = GameManager(data_manager.guess_words, agent)
        game.attachDataCollector(dataCollector)
        # Play game using word as answer
        datum = game.test(answer=word)
        
        # Interrupt if no data given
        if datum is None:
            print("Error: Data not found. Test stopped")
            return 
        
    return []

def test_csp(gaent_type: str, test_set: set, lexicon: set, dataCollector: ReportDataCollector):
    """ Runs toe csp solver using the given agent, using each word in test_set as the answer
        (so the number of games tested is equal to the length of test_set) """

    starting_word = "SLATE"

    count = 0

    for word in test_set:
    #    print("Running Wordle", count, ": ", word)
        print("Running Wordle")
        count += 1

        game = CSPSolver(word)
        game.attachDataCollector(dataCollector)
        datum = game.test(starting_word)
        # Interrupt if no data given
        if datum is None:
            print("Error: Data not found. Test stopped")
            return 

    #    if(count == 100):
    #        break
        
    return []