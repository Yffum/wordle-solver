import DataProcessing
from GameManager import GameManager
from SearchAgent import SearchAgent
from BruteSearchAgent import BruteSearchAgent
from TreeSearchAgent import TreeSearchAgent

import pandas as pd
import time
from datetime import datetime
from collections import Counter


def run(agent_type: str, lexicon: set, letter_probs: list[Counter]):
    # Record test time
    start_time = time.process_time()
    # Using lexicon as test set for now
    test(agent_type, lexicon, lexicon, letter_probs)
    duration = time.process_time() - start_time

    print("Total test duration:", round(duration/60, 2), "minutes")

    

def create_search_agent(agent_type: str, lexicon: set, letter_probs: list[Counter]) -> SearchAgent:
    """ Creats a search agent of the given type. Vocabulary is built from given lexicon, and 
        word scoring is determined by the given letter probability distribution. """
    if agent_type == 'brute':
        return BruteSearchAgent(lexicon, letter_probs)
    if agent_type == 'bfs' or 'dfs' or 'astar':
        # Pass agent type to tree agent to choose bfs/dfs/astar
        return TreeSearchAgent(lexicon, letter_probs, agent_type)



def test(agent_type: str, test_set: set, lexicon: set, letter_probs: list[Counter],):
    """ Runs the solver using the given agent, using each word in test_set as the answer
        (so the number of games tested is equal to the length of test_set) """
    data = []
    for i, word in enumerate(test_set):
        # Testing
        # if i > 100:
        #     break

        # Create new search agent of given type
        agent = create_search_agent(agent_type, lexicon, letter_probs)
        # Create new game
        game = GameManager(lexicon, agent)
        # Play game using word as answer
        datum = game.test(answer=word)
        
        # Interrupt if no data given
        if datum is None:
            print("Error: Data not found. Test stopped")
            return 
        
        # Record data
        data.append(datum)

    # Convert data to DataFrame
    df = pd.DataFrame.from_records(data)

    # Count successes 
    success_count = df['Success'].value_counts().get(True, 0)

    # Calculate stats
    win_percentage = success_count/len(lexicon)
    avg_guess_count = df['Guess Count'].mean()
    total_avg_guess_time = df['Avg Guess Time (s)'].mean()
    avg_game_duration = df['Game Duration (s)'].mean()

    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"test_results/wordle_test_{current_datetime}.txt"

    # Write overall statistics
    with open(filename, 'w') as f:
        f.write("Win Percentage: {}\n".format(win_percentage))
        f.write("Avg Guess Count: {}\n".format(avg_guess_count))
        f.write("Total Avg Guess Time (s): {}\n".format(total_avg_guess_time))
        f.write("Avg Game Duration(s): {}\n".format(avg_game_duration))

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

