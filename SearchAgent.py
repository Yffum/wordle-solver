import queue
import copy

class SearchAgent:
    def __init__(self, vocab: set, letter_probability_distribution: list):
        # Words that can be guessed
        self.vocab = vocab
        # Set of previously guessed words
        self.prev_guesses = set()
        # List of adjusted letter probabilities
        self.letter_probs = copy.deepcopy(letter_probability_distribution)
        

    def adjust_letter_probs(self, guess: str, letter_ratings: list):
        """ Takes a guess and its corresponding ratings, and updates
            letter_probs for each character in the guess. """
        # Check every char and corresponding rating
        for i, rating in enumerate(letter_ratings):
            char = guess[i]
            # If letter is correct, set probability to 1
            if rating == '2':
                self.letter_probs[i][char] = 1
            # ToDo: adjust probabilities for '1' ratings
            # elif score == '1':
            #     self.letter_probs[i][char] += 0.2
            # If letter is incorrect, set probability to 0
            elif rating == '0':
                self.letter_probs[i][char] = 0
                # ToDo: adjust probabilities for char in every position
                # for table in self.letter_probs:
                #     if table[char] != 1:
                #         table[char] = 0


    def get_score(self, word: str) -> float:
        """ Returns a word score equal to the sum of the probability of each letter
            being in its respective position. """
        # If word was guessed previously, score is 0
        if word in self.prev_guesses:
            return 0
        score = 0
        # For each character
        for i, char in enumerate(word):
            # Get probability
            prob = self.letter_probs[i][char]
            # If any letter prob is 0, word score is 0
            if prob == 0:
                return 0
            # Add probability of character to score
            score += prob
        # Return rounded score
        return round(score, 3)

    def brute_force_search(self):
        """ Rates every word in the vocab based on letter probabilities, and 
            then returns the word with the best score """
        # Use priority queue to get best word quickly
        rated_words = queue.PriorityQueue()
        # Rate every word in vocab
        for word in self.vocab:
            score = self.get_score(word)
            # Use negative score because PriorityQueue is a min heap
            rated_words.put((-score, word))
        # Get best word from priority queue
        best_score, best_word = rated_words.get()

        # TESTING
        # print("Best Score:", best_score, "Best Guess:", best_word)

        # while not rated_words.empty():
        #      score, word = rated_words.get()
        #      if word == "LASER":
        #         print("Score:", score, "Word:", word)

        # Add best guess to previous guesses and return it
        self.prev_guesses.add(best_word)
        return best_word

