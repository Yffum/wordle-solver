import queue

class SearchAgent:
    def __init__(self, vocab: list, letter_probability_distribution: list):
        # Words that can be guessed
        self.vocab = vocab
        # List of original letter probabilities
        self.original_letter_probs = letter_probability_distribution
        # List of adjusted letter probabilities
        self.letter_probs = list(self.original_letter_probs)

        # ToDo: this list contains pointers to the letters in letter_probs, rather than copies
        #       Maybe create new data type for letter_probs

    def adjust_letter_probs(self, guess: str, letter_ratings: list):
        """ Takes a guess and its corresponding word score, and updates
            letter_probs for each character in the guess. """
        # Check every char and corresponding score
        for i, rating in enumerate(letter_ratings):
            char = guess[i]
            # If letter is correct, set probability to 1
            if rating == '2':
                self.letter_probs[i][char] = 1
            # elif score == '1':
            #     self.letter_probs[i][char] += 0.2
            # If letter is incorrect, set probability to 0 for every position
            elif rating == '0':
                for table in self.letter_probs:
                    table[char] = 0


    def get_score(self, word: str) -> float:
        """ Returns a word score equal to the sum of the probability of each letter
            being in its respective position. """
        score = 0
        # For each character
        for i, char in enumerate(word):
            # Get probability
            prob = self.letter_probs[i][char]
            # If letter prob is 0, word score is 0
            if prob == 0:
                return 0
            # Add probability of character to score
            score += prob
        return score

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
        return best_word

