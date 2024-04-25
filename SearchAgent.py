
from collections import Counter
from abc import ABC, abstractmethod


class SearchAgent(ABC):
    
    @abstractmethod
    def get_guess(self) -> str:
        """ Returns a guess word """
        pass
    
    @abstractmethod
    def process_feedback(guess: str, letter_ratings: list[int]):
        """ Adjusts agent's internal information based on the given letter ratings for
            the given guess. Each index in the letter_ratings corresponds to a character
            in the guess.
                0 is incorrect,
                1 is incorrect postion,
                2 is correct,
            (For example, the correct guess would have letter_ratings = ['2','2','2','2','2']) """
        pass



    

