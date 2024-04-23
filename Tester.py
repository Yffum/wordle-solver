import DataProcessing
from GameManager import GameManager
from SearchAgent import SearchAgent

import pandas as pd
import time
from datetime import datetime

def test_all_words():
    # Process lexicon and calculate letter probabilities
    lexicon = DataProcessing.import_lexicon()
    letter_probs = DataProcessing.calculate_letter_probability_distribution(lexicon)

    data = []
    for i, word in enumerate(lexicon):

        # Testing
        # if i > 100:
        #     break

        # Create new search agent and game
        agent = SearchAgent(lexicon, letter_probs)
        game = GameManager(lexicon, agent)
        # Play game using word as answer
        datum = game.test(answer=word)
        # Record data
        data.append(datum)

    # Convert data to DataFrame
    df = pd.DataFrame.from_records(data)

    # Count successes 
    max_guesses = 6
    df['Success'] = df['Guess Count'] <= max_guesses
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


def main():
    start_time = time.process_time()
    test_all_words()
    duration = time.process_time() - start_time

    print("Total test duration:", round(duration/60, 2), "minutes")


if __name__ == '__main__':
    main()