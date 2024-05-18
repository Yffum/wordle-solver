# Approach

This file describes the implementation of our various search agents.

Our approach focuses on using a probability based solution enhanced with various search techniques. Rather than counting the frequency of each letter in the entire set of possible answer words, the frequencies are counted with respect to each character position. In other words, we created a map of probabilities for all 26 characters in the alphabet for each of the 5 character positions in the answer, giving us a map of 130 position-specific probabilities.

### Word Score
The word score is a sum of the probabilities for each letter in the word. For example, we can calculate the word score of the word "TOAST" like so:

First we calculate the probability that each letter will be in its respective position. For example, the probability that 'A' is the third letter is 0.1326 (i.e., the third letter of about 13% of the possible answer words is 'A')

```
p(1, T) = 0.0644
p(2, O) = 0.1205
p(3, A) = 0.1326
p(4, S) = 0.0739
p(5, T) = 0.1093

score("TOAST") = p(1, T) + p(2, O) + p(3, A) + p(4, S) + p(5, T) 
    = 0.5007
```

Thus the word “TOAST” has a score of 0.5007

## Brute Force
Our brute force search parses through every word in the possible answer set, calculating a word score for each word. Each word is then put in a heap structure with its score, in order to quickly find the word with the highest score. After each guess, the search agent takes the feedback from the game and changes the probabilities of each letter in the previously guessed word. If the letter was marked correct, it’s given a probability of 1 for its respective position; if the letter was marked incorrect, it’s given a probability of 0 for its respective position. Using these initial sequential adjustments, the brute force agent was able to find the answer, but tended to take more than six turns (i.e., most of the games it solved, it failed). 

To enhance brute force search, another sequential adjustment was added: When interpreting feedback from the game about a previous guess, if a letter is marked as incorrect-position, it is given a probability of 0 for its respective position, but the letter is added to a bag of known letters. When calculating the word score, letters in the bag of known letters are given a score boost equal to the inverse of the word length of 5. 

For example, say the agent’s first guess is “MAYBE”, and the letter ‘A’ is marked as incorrect-position and added to the bag of known letters. Then, when the agent is calculating all the word scores to find the next guess, the score for “TOAST” would be calculated like so:

```
 boost =  1 / (word length) = 1 / 5 = 0.2

 score("TOAST") =  p(1, T) + 0
+ p(2, O) + 0
+ p(3, A) + 0.2
+ p(4, S) + 0
+ p(5, T) + 0     =  0.7007
```

The agent checks if each character in “TOAST” is in the bag of known letters (eliminating matching letters to allow and account for duplicates). Because ‘A’ is in the bag after being marked as incorrect-position, it is given a score boost, significantly raising the score of the example word “TOAST”. The boost factor was chosen from the idea that there is a 1 in 5 chance that a known letter will be in any of the 5 positions of a 5-letter word. Of course one of the 5 positions will have been eliminated when the letter is marked as incorrect-position, but a 1/5 boost yielded slightly better results than a 1/4 boost. This is likely because adding this boost is a very crude estimation of the letter’s new probability, and 1/4 is too extreme of an adjustment. 

With these sequential updates to its letter probability map, the brute force agent is able to solve Wordle within 6 guesses fairly consistently.

## Tree Search
Our tree search algorithms create a tree of nodes, where each node contains a 5-letter string that may or may not be an actual word. The search agent maintains a fringe of nodes to expand, which starts with the root node. The word score of each node in the fringe is calculated and compared to a score threshold. If the word score is above the threshold, the 5-letter string is returned as a guess. If the word score is not above the threshold, the node is expanded by adjusting one letter in the 5-letter string and then adding the node to the fringe (if it has not appeared before).

### Threshold
The score threshold is determined using a function based on the number of confirmed letters. The base score threshold was determined experimentally by observing the word scores from brute force search. The function is linear with respect to the number of confirmed letters, because word score increases for words with confirmed letters. The function is scaled using a threshold increase factor, which was tuned experimentally, but not thoroughly.

If the tree search fails to find a word above the threshold, it lowers the threshold and repeats the search until no word is found above a threshold of 0, in which case no possible guess is found by the agent.

### Breadth-First Search (BFS)
The BFS algorithm uses a queue fringe, such that the children of the root node are all evaluated before any other descendents. When a node is expanded, its children are placed at the back of the queue fringe. Then the next node evaluated is removed from the front of the queue fringe.

### Depth First Search (DFS)
The DFS algorithm uses a stack fringe, such that the agent keeps expanding down one path, rather than evaluating each node at each level of the tree. When a node is expanded, its children are pushed to the top of the stack fringe. The next node is popped from the top of the stack fringe, such that the last child node pushed is evaluated first.

### First Guesses
Our first implementations of tree search took a very long time to run (up to several minutes for a single problem). This is in part because of the size of the tree. Initially, the root node would have 125 child nodes (25 possible letters for each of the 5 positions in the string). But, by using a sequence of starting words, the domain of possible letters for the 5 positions can be significantly limited, making the tree smaller.

We created a module which finds a sequence of starting guesses to eliminate or confirm as many letters as possible. Because these words intentionally do not repeat letters, the module runs as a preprocess and creates a list of starting guesses that the tree search algorithms use for every game. The module determines the frequency of each letter in the answer word set, regardless of position. Then it finds a guess word which contains the 5 most common letters. For the following guess, it excludes the letters from the previous guesses and repeats the search. The first word can be set manually in order to execute specific strategies like eliminating vowels using “AUDIO”.

After finding three starting words and eliminating or confirming 15 of the most common letters in the alphabet, the module was unable to find another word with 5 new unique letters to eliminate/confirm. Thus we decided to only use the first three guesses to eliminate letters, and further guesses are then searched for using word score. More testing needs to be done for the effectiveness of using fewer than three starting guesses before searching for correct guesses. Also, while using a fourth starting guess may not eliminate another 5 letters, it could be worth it just to eliminate 3 or 4 more letters.

A more advanced brute force module might parse through the possible answer words after each guess, eliminating words based on feedback given, and then recalculating the letter probabilities based on the updated answer set. This was not in the scope of our project, and because the letter probabilities are not recalculated each game, we can determine the start sequence as a preprocess, as explained previously. This significantly improved the performance of tree search algorithms, making them tractable.

Ideally, a search agent would begin with guesses that eliminate as many characters as possible and then transition smoothly into guessing words that are most likely to be the answer. Our tree agents simply transition after three guesses. Perhaps reinforced learning could train an agent to transition at the ideal time. Or perhaps it could train an agent to begin integrating elements of answer-guesses into the character-elimination-guesses, rather than making a hard transition.

### Greedy Search
Greedy search is an obvious approach for our search because we are already evaluating the word score for every node. Rather than using a stack or queue for the fringe, greedy search uses a priority queue based on the word score of each node. Thus the node with the highest word score is removed from the queue, allowing the agent to more quickly find a word with a score above the threshold.

### A* Search
A* search expands on greedy search by not only considering the word score of each node, but also its depth. In order to make the word score heuristic more comparable to depth, we scale the difference between a given word score and the threshold by a constant to estimate the distance of a goal node. This heuristic is added to the depth to determine the priority of each node in the priority queue. The scaling constant was determined experimentally, to minimize search time, but more testing is required to find an optimal constant in terms of both search time, and guess count.

### CSP
CSP module defines three elements:
    Variables: letter positions: GuessStatus: Green, Yellow, Gray letter Info
    Domains: possible letters: {A,B,C, …, X,Y,Z}
    Constraints are based on feedback from the game

    For example, when the answer is "SNAKE," constraints can be updated at each step as follows.
    First guess word (SLATE)
        : Green: S****, Yellow: {2: 'A', 4: 'E'}, Gray: LT, 
        : Unused: BCDFGHIJKMNOPQRUVWXYZ
    2nd guess word (BIDDY)
        : Green: S****, Yellow: {2: 'A', 4: 'E', 1: 'A', 3: 'E'}, Gray: FLRT, 
        : Unused: BCDGHIJKMNOPQUVWXYZ
    3rd guess word (CHOCK)
        : Green: S**A*, Yellow: {2: 'A', 4: 'E,N', 1: 'A,E', 3: 'E'}, Gray: DFLRT, 
        : Unused: BCGHIJKMOPQUVWXYZ
    4th guess word (SNAKE) -> Answer
        : Green: SNAKE, Yellow: {2: 'A', 4: 'E,N', 1: 'A,E', 3: 'E'}, Gray: DFLRT, 
    : Unused: BCGHIJMOPQUVWXYZ

The Solver Class initializes a game with the first guessed word. The Dictionary Class receives the first guessed word and communicates with the GuessState Class to obtain feedback and determine the next guessed word. The GuessStatus Class maintains constraints based on guessed words. The Solver Class ends a game when the guessed word matches the answer.
