from collections import Counter
#import resource
import time
import os

from SearchAgent import SearchAgent
import DataProcessing

# Global Variables
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
MAX_GUESS_COUNT = 100
WORD_LENGTH = 5


class GameManager:
    """ Runs the Wordle game loop """

    def __init__(self, lexicon: set, agent: SearchAgent=None):
        """ The start() function sets the answer, and resets the guess_count to 0"""
        self.answer = None
        self.guess_count = 0
        self.legal_words = lexicon
        self.agent = agent

        # Stats
        self.guess_durations = []

    def get_AI_guess(self, agent: SearchAgent) -> str:
        """ Returns a guess word from the given search agent """
        # Track time
        start_time = time.process_time()
        # Get guess from agent
        guess = agent.brute_force_search()
        # Record time
        guess_duration = time.process_time() - start_time
        self.guess_durations.append(guess_duration)
        # Print and return
        print('Agent guess:     ', guess)    
        return guess


    def get_user_guess() -> str:
        """ Prompts the user for a guess word in the terminal and returns their input """
        # Get user input
        print("Enter your guess: ", end="")
        guess = input()
        # Normalize to uppercase
        return guess.upper()


    def get_guess(self, agent: SearchAgent=None) -> str:
        """ If the guess is not from_AI, then it will prompt the user """
        if agent is None:
            return self.get_user_guess()
        else:
            return self.get_AI_guess(agent)


    def get_letter_ratings(self, guess: str) -> list:
        """ Takes a guess and returns a list of five chars in {0,1,2}, where each 
            char corresponds to a letter in the guess: 
                0 is incorrect,
                1 is incorrect postion,
                2 is correct,
            (For example, guessing the correct answer would return ['2','2','2','2','2']) """
        
        # Make sure guess is legal
        if len(guess) != 5:
            print("The length of the guess must be five letters.")
            return None
        if guess not in self.legal_words:
            print(guess, "is not in the game dictionary.")
            return None
        
        # Start with five zeros (all incorrect)
        letter_ratings = ['0'] * WORD_LENGTH
        # Keep track of chars in the answer that haven't been guessed 
        remaining_chars = Counter(self.answer) 

        # Check each char in guess for correctness
        for i, char in enumerate(guess):
            # If char is correct
            if char == self.answer[i]:
                # Set corresponding rating
                letter_ratings[i] = '2'
                # Remove from remaining chars
                remaining_chars.subtract(char)
        
        # Check each char in guess for membership in remaining chars
        for i, char in enumerate(guess):
            # If char was guessed correctly, skip it
            if letter_ratings[i] == '2':
                continue
            # If char is in the remaining chars, that means it's in the word and hasn't
            # been correctly guessed, so it's in the incorrect position
            if remaining_chars[char] > 0:
                # Set corresponding rating
                letter_ratings[i] = '1'
                # Remove from remaining chars
                remaining_chars.subtract(char)
        
        # Remaining letter ratings are left as '0'
        return letter_ratings


    def start(self, answer: str, use_AI: bool=True) -> bool:
        """ Run a game of Wordle using the given answer. Returns true if game is won.
            If use_AI is False, then the user will be prompted for guesses """

        print("Running Wordle:")

        # Set up game
        self.guess_count = 0
        self.answer = answer
        
        # Run game loop until out of guesses
        while self.guess_count < MAX_GUESS_COUNT:
            # Get guess
            guess = self.get_guess(self.agent)
            # Rate each character
            letter_ratings = self.get_letter_ratings(guess)

            # If letter_ratings is None, the guess didn't work so try again
            if letter_ratings is None:
                continue

            self.guess_count += 1
            
            # Convert to string format
            rating_str = ''.join(letter_ratings)

            # Print letter ratings aligned with guess
            print('Ratings:         ', rating_str)

            # Inform AI of letter ratings
            if use_AI:
                self.agent.adjust_letter_probs(guess, letter_ratings)

            # If correct, inform user and return true
            if rating_str == '22222':
                print(guess, "is correct! You win!")
                return True

        # Reached maximum number of guesses
        print("You ran out of guesses. You lose.")
        return False
    

    def test(self, answer: str) -> dict:
        """ Runs solver and returns dictionary of statistics """
        # Track time
        start_time = time.process_time()
        # Run game
        self.start(answer)
        # Record game time
        game_duration = time.process_time() - start_time

        # Calculate avg guess time
        avg_guess_time = sum(self.guess_durations)/len(self.guess_durations)
        # Get maximum RAM usage
        #max_ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        #max_ram = round(max_ram/1024, 8)  # Convert to megabytes and round

        # Create row for DataFrame
        data_row = {'Answer': answer,
                    'Guess Count': self.guess_count, 
                    'Avg Guess Time (s)': avg_guess_time,
                    'Game Duration (s)' : game_duration}
                    #'Max RAM (MB)' : max_ram} 

        return data_row



def main():
    # Process lexicon and calculate letter probabilities
    lexicon = DataProcessing.import_lexicon()
    letter_probs = DataProcessing.calculate_letter_probability_distribution(lexicon)

    # Create search agent using probabilities
    agent = SearchAgent(lexicon, letter_probs)


    game = GameManager(lexicon, agent)
    game.start(answer="GALES", use_AI=True) # Try to guess LASER using the terminal



if __name__ == '__main__':
    main()
