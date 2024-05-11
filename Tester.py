import DataProcessing
from GameManager import GameManager
from SearchAgent import SearchAgent
from BruteSearchAgent import BruteSearchAgent
from TreeSearchAgent import TreeSearchAgent
from wordle_csp_solver import Dictionary
from wordle_csp_solver import CSPSolver
from DataManager import DataManager

import pandas as pd
import time
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt

def run(agent_type: str, test_words: list, data_manager:DataManager):
    """ Run test() and record/report duration"""
    # Record test time
    start_time = time.process_time()
    # Using lexicon as test set for now

    if(agent_type == 'csp'):
        # run basic CSP test routine
        data = test_csp(agent_type, test_words, data_manager.guess_words)
    else:
        # run 'brute', 'bfs', 'dfs' and 'ast'
        data = test(agent_type, test_words, data_manager)

    # Round duration to minutes
    duration = time.process_time() - start_time
    duration = round(duration/60, 2)
    # Write to file
    process_data(data, agent_type, duration)

    # Generate plot
    #process_plot(data, agent_type, duration)

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



def test(agent_type: str, test_words: list, data_manager: DataManager):
    """ Runs the solver using the given agent, using each word in test_set as the answer
        (so the number of games tested is equal to the length of test_set) """
    data = []
    for i, word in enumerate(test_words):
        # Create new search agent of given type
        agent = create_search_agent(agent_type, data_manager.answer_words, data_manager.letter_probs, data_manager.start_words)
        # Create new game
        game = GameManager(data_manager.guess_words, agent)
        # Play game using word as answer
        datum = game.test(answer=word)
        
        # Interrupt if no data given
        if datum is None:
            print("Error: Data not found. Test stopped")
            return 
        
        # Record data
        data.append(datum)
    return data

def test_csp(gaent_type: str, test_set: set, lexicon: set):
    """ Runs toe csp solver using the given agent, using each word in test_set as the answer
        (so the number of games tested is equal to the length of test_set) """
    data = []

    starting_word = "SLATE"

    count = 0

    for word in test_set:
    #    print("Running Wordle", count, ": ", word)
        print("Running Wordle")
        count += 1

        datum = CSPSolver(word).test(starting_word)

        # Interrupt if no data given
        if datum is None:
            print("Error: Data not found. Test stopped")
            return 

        # Record data
        data.append(datum)

    #    if(count == 100):
    #        break
        
    return data

def process_data(data: list[dict], agent_type: str, duration: float):
    """ Writes data to file and prints test duration. """
    # Convert data to DataFrame
    df = pd.DataFrame.from_records(data)

    # Count successes 
    success_count = df['Success'].value_counts().get(True, 0)
    
    # Precision
    p = 2 # num of digits after decimal

    # Calculate stats
    win_percentage = round(100 * success_count/len(data), p)
    avg_guess_count = round(df['Guess Count'].mean(), p)
    total_avg_guess_time = round(df['Avg Guess Time (ms)'].mean(), p)
    avg_game_duration = round(df['Game Duration (ms)'].mean(), p)
    
    # Round stats
    df = df.round(p)

    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"test_results/wordle_test_{current_datetime}.txt"
    
    with open(filename, 'w') as f:
        f.write("")

    # Write overall statistics
    with open(filename, 'w') as f:
        f.write("Date: {}\n".format(datetime.now().strftime("%Y-%m-%d")))
        f.write("Search Mode: {}\n".format(agent_type))
        f.write("Test Size: {}\n".format(len(data)))
        f.write("Test Duration (min): {}\n".format(duration))
        f.write("Win Percentage (%): {}\n".format(win_percentage))
        f.write("Avg Guess Count: {}\n".format(avg_guess_count))
        f.write("Total Avg Guess Time (ms): {}\n".format(total_avg_guess_time))
        f.write("Avg Game Duration (ms): {}\n".format(avg_game_duration))

    # Sort by easiest games (fewest guesses)
    df.sort_values(by='Guess Count', ascending=True, inplace=True)
    # Write to file
    with open(filename, 'a') as f:
        f.write("\n")
        f.write("Top 10 Easiest Games (fewest guesses):\n")
    df.head(10).to_csv(filename, mode='a', index=False)

    # Sort by hardest games (most guesses)
    df.sort_values(by='Guess Count', ascending=False, inplace=True)
    # Write to file
    with open(filename, 'a') as f:
        f.write("\n")
        f.write("Top 10 Hardest Games (most guesses):\n")
    df.head(10).to_csv(filename, mode='a', index=False)

def process_plot(data: list[dict], agent_type: str, duration: float):
    """ generate plot with guess count. """
    # Convert data to DataFrame
    df = pd.DataFrame.from_records(data)

    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename2 = f"test_results/wordle_test_plot_{current_datetime}.png"
    
    counts = df['Guess Count'].value_counts().to_dict()

    x_axis = list(counts.keys())
    y_axis = list(counts.values())
    plt.bar(x_axis, y_axis, edgecolor='black')

    plt.title(('Distribution of Game Results [' + agent_type + ']'))
    plt.xlabel('Number of Guesses')
    plt.ylabel('Number of Games')

    # save the plot
    plt.savefig(filename2)
    #show the plot
    plt.show()    
