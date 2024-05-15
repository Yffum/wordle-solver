# Wordle Solver

## Description
This program uses its own Wordle engine, modeled to perform exactly like the New York Times Wordle game. The program features a variety of Wordle-solving search agents with varying speed and accuracy for testing and comparison.

See [How to Play Wordle](https://www.nytimes.com/2023/08/01/crosswords/how-to-talk-about-wordle.html).

## Interface
Our program uses the numbers (0, 1, 2) as feedback, instead of the colors (gray, yellow, green). This how they correspond:

    0 - gray   - incorrect letter  
    1 - yellow - correct letter, incorrect position
    2 - green  - correct letter, correct position

## Usage
Navigate to the program directory.

To run the Wordle Solver, you can run `main.py` like so:

`$ python main.py <agent_type> <test_length> <test_mode>`

where the three bracketed arguments are replaced like so:

`<agent_type>`  - The search agent type (`brute`, `csp`, `bfs`, `dfs`, `greedy`, `astar`)  
`<test_length>` - The number of games to solve (`1` to `1000`)  
`<test_mode>`   - The difficulty level of games  (`hard`, `easy`, `random`)

To play Wordle using terminal input, run `play.py` with no arguments like so:

`$ python play.py`

This will run a game of Wordle using a random answer word that the user has to guess. This can be used to manually test our Wordle engine.

## Data
All of our data can be found in the `Data` folder. 

We use a [Kaggle dataset](https://www.kaggle.com/datasets/bcruise/wordle-valid-words) containing valid guesses and valid answers extracted from the New York Times Wordle webpage.

`valid_guesses.csv` contains valid guess words that are not possible answers. This is used by the CSP module.

`valid_solutions.csv` contains valid answer words. This is used by the `Tester` module to generate games.

`valid_solutions_ordered.csv` contains valid answer words, ordered from easy to hard, based on the number of guesses taken by the brute force agent.

`wordle_lexicon.csv` contains all valid guesses that the game will accept (including possible answers). This is used by the `GameManager` module to make sure guesses are valid.

## Word Score
All of our algorithms use word scores based on the sum of probabilities that each letter will be in its given position. These probabilities are calculated from the solution set when the program starts using `calculate_letter_probability_distribution()` in `DataProcessing.py`.

## Agents
For detailed descriptions of how our agents are implemented, see `Approach.md`

## Testing
Test results can be found in the `test_results` folder with date-time stamps. 


