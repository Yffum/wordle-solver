from GameManager import WORD_LENGTH

from collections import Counter
import queue
import copy

class SearchAgent:
    """ A SearchAgent must be instantiated with a vocabulary of words it can guess, 
        and a letter probability distribution (a list of Counters), from which it 
        calculates its guesses. A new agent should be instantiated for each game, as 
        the vocab and probability distribution are adjusted each search. """
    def __init__(self, vocab: set, letter_probability_distribution: list):
        # Words that can be guessed
        self.vocab = set(vocab)
        # List of adjusted letter probabilities
        self.letter_probs = copy.deepcopy(letter_probability_distribution)
        # These letters are known to be in the word, but we don't know the position
        self.known_letters = Counter()
        # Words to be removed from the vocab after iterating through the vocab
        self.words_to_remove = set()

    def adjust_letter_probs(self, guess: str, letter_ratings: list):
        """ Takes a guess and its corresponding ratings, and updates
            letter_probs for each character in the guess. """
        # Track letters that are in the word, but we don't know the position
        new_known_letters = Counter()
        # Check every char and corresponding rating
        for i, rating in enumerate(letter_ratings):
            char = guess[i]
            # If letter is correct, set probability to 1
            if rating == '2':
                # If letter was known without position, remove it from the tracker
                if char in self.known_letters:
                    del self.known_letters[char]
                # Set proability to 1
                self.letter_probs[i][char] = 1
            # If letter is known, but in the wrong position, track it
            elif rating == '1':
                new_known_letters[char] += 1
            # If letter is incorrect, set probability to 0
            elif rating == '0':
                self.letter_probs[i][char] = 0
                # Adjust probabilities of other positions to 0
                # ToDo: I'm not sure whether this accounts for all edge cases
                # Make sure letter is not already known (without position)
                if char not in new_known_letters:
                    # Loop through tables for every char position
                    for table in self.letter_probs:
                        # Make sure letter is not already known (with position)
                        if table[char] != 1:
                            # Set probability to 0
                            table[char] = 0
        # Add new known letters to persistent list
        for char, count in new_known_letters.items():
            # Only add if the count in the new list is greater
            # E.g., if the letter was not previously known, or if only 1 was known,
            # but now there are 2.
            if count > self.known_letters[char]:
                # Update count
                self.known_letters[char] = count


    def get_score(self, word: str) -> float:
        """ Returns a word score equal to the sum of the probability of each letter
            being in its respective position. """
        score = 0
        # For each character
        for i, char in enumerate(word):
            # Get probability
            prob = self.letter_probs[i][char]
            # If any letter prob is 0, then the entire word score is 0
            if prob == 0:
                # Remove word from vocab after iterating through it
                self.words_to_remove.add(word)
                return 0
            
            # Increase probability if letter is known
            factor = 1/WORD_LENGTH # chance to be in that position
            prob += factor * self.known_letters[char]
            # Example: If we know a 5-letter word has 2 'a', then we increase the
            #          probability of 'a' in this position by 0.2 * 2 = 0.4

            # Add probability of character to score
            score += prob
        # Return rounded score
        return round(score, 3)

    def brute_force_search(self):
        """ Scores every word in the vocab based on the sum of letter probabilities, 
            and then returns the word with the best score """
        # Use priority queue to get best word quickly
        rated_words = queue.PriorityQueue()
        # Rate every word in vocab
        for word in self.vocab:
            score = self.get_score(word)
            # Use negative score because PriorityQueue is a min heap
            rated_words.put((-score, word))
        # Remove impossible words which have a score of 0 from vocab
        self.vocab -= self.words_to_remove
        self.words_to_remove.clear()
        # Get best word from priority queue
        best_score, best_word = rated_words.get()

        # TESTING
        print("Best Score:", best_score, "Best Guess:", best_word)

        # while not rated_words.empty():
        #      score, word = rated_words.get()
        #      if word == "LASER":
        #         print("Score:", score, "Word:", word)

        # Remove word from vocab to prevent repetition
        self.vocab.remove(best_word)
        return best_word

