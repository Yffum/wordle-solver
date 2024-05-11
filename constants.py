# Global Variables

# Scale for the astar heuristic function.
    # this constant scales the difference between a current word's score and
    # the current score threshold in astar, in order to estimate the number
    # of nodes until a word above the threshold is reached
H_SCALE = 1000 
# Starting threshold for word score
BASE_THRESHOLD = 0.5
# The value the threshold decreases by if no word is found
THRESHOLD_DECREMENT = 0.3
# The factor by which the treshold scales with the number of confirmed letters
THRESHOLD_INCREASE_FACTOR = 0.3
# Number of decimal places to round to when performing calculations
PRECISION = 4


# The internal max guess limit to identify errors
MAX_GUESS_LIMIT = 100
# The types of agents that can be used
AGENT_TYPES = ('brute', 'csp', 'bfs', 'dfs', 'greedy', 'astar')


# English alphabet
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
# If solver takes more than this number of guesses, it's unsuccessful
MAX_GUESS_COUNT = 6
# The length of words
WORD_LENGTH = 5
