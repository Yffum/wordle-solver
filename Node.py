
class WordleState:
    """ Contains the information gathered from previous guesses """
    def __init__(self):
        # List  that tracks letters with confirmed positions. Each
        # index corresponds to one of the 5 characters in the answer.
        self.confirmed_letters = [None] * 5

        # Dictionary which tracks the count of letters with unconfirmed
        # positions, for example if it is determined that the letter 'Y' 
        # is not in the answer, then letter_counts['Y'] will be set to 0
        self.letter_counts = dict()

class  Node:
    """ A search tree node for Wordle """
    def __init__(self, state: WordleState, prev_node: 'Node'=None):

        self.state = state

        self.prev = prev_node
        self.depth = 0

        # Get depth from previous node
        if self.prev != None:
            self.depth = self.prev.depth + 1

