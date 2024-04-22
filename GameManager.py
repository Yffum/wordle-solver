from collections import Counter


# The rules of Wordle
MAX_GUESS_COUNT = 6
WORD_LENGTH = 5


def get_AI_guess() -> str:
    
    # ToDo: Implement

    return None


def get_user_guess() -> str:
    """ Prompts the user for a guess in the terminal and returns their input """
    # Get user input
    print("Enter your guess: ", end="")
    guess = input()
    # Normalize to uppercase
    return guess.upper()


def get_guess(from_AI: bool) -> str:
    """ If the guess is not from_AI, then it will prompt the user """
    if from_AI:
        return get_AI_guess()
    else:
        return get_user_guess()


class GameManager:
    """ Runs the Wordle game loop """

    def __init__(self):
        """ The start() function sets the answer, and resets the guess_count to 0"""
        self.answer = None
        self.guess_count = 0


    def get_score(self, guess: str) -> list:
        """ Returns a list of five chars in {0,1,2}, where each char corresponds
            to a letter in the guess: 
                0 is incorrect,
                1 is incorrect postion,
                2 is correct,
            (For example, guessing the correct answer would return ['2','2','2','2','2']) """
        
        #ToDo: If guess is length 5 and guess in legal_words then return none
        
        # Start with five zeros (all incorrect)
        score = ['0'] * WORD_LENGTH
        # Keep track of chars in the answer that haven't been guessed 
        remaining_chars = Counter(self.answer) 

        # Check each char in guess for correctness
        for i, char in enumerate(guess):
            # If char is correct
            if char == self.answer[i]:
                # Set corresponding score digit
                score[i] = '2'
                # Remove from remaining chars
                remaining_chars.subtract(char)
        
        # Check each char in guess for membership in remaining chars
        for i, char in enumerate(guess):
            # If char was guessed correctly, skip it
            if score[i] == '2':
                continue
            # If char is in the remaining chars, that means it's in the word and hasn't
            # been correctly guessed, so it's in the incorrect position
            if remaining_chars[char] > 0:
                # Set corresponding score digit
                score[i] = '1'
                # Remove from remaining chars
                remaining_chars.subtract(char)
        
        # Remaining digits in score are left as '0'
        return score


    def start(self, answer: str, use_AI: bool) -> bool:
        """ Run a game of Wordle using the given answer. Returns true if game is won.
            If use_AI is False, then the user will be prompted for guesses """

        print("Starting Wordle Solver:")

        # Set up game
        self.guess_count = 0
        self.answer = answer
        
        # Run game loop until out of guesses
        while self.guess_count < MAX_GUESS_COUNT:
            # Get guess
            guess = get_guess(use_AI)
            self.guess_count += 1
            # Score each character
            score = self.get_score(guess)
            score_str = ''.join(score)

            # Print score aligned with guess
            print('Score:           ', score_str)

            # If correct
            if score_str == '22222':
                print(guess, "is correct! You win!")
                return True

        # Reached maximum number of guesses
        print("You ran out of guesses. You lose.")
        return False



def main():
    game = GameManager()
    game.start(answer="LASER", use_AI=False) # Try to guess LASER using the terminal



if __name__ == '__main__':
    main()
