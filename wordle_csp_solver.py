
import functools


WORD_LENGTH = 5

class LetterInfo:
    def __init__(self, letter, position):
        self.letter = letter
        self.by_position = {0:0,1:0,2:0,3:0,4:0}
        self.total = 0
        self.by_position[position] = 1

    def add(self, position):
        self.by_position[position] += 1
        self.total += 1

    def __getitem__(self, item):
        return self.by_position[item]
    
class GuessStatus:
    def __init__(self):
        # letters in known position (key:index, value:letter)
        self.green = dict()

        # letters in the answer but in the wrong position (key:index, value:letter)
        self.yellow = dict()

        # letters not in the word
        self.gray = set()

        # letters used in guesses
        self._used = set()

        # letters not used in guesses
        self._unused = set([letter for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"])

    def update_use(self, letter):
        self._used.add(letter)
        if letter in self._unused:
            self._unused.remove(letter)

    def get_used(self):
        return self._used

    def update_green(self, letter, position):
        self.update_use(letter)
        self.green[position] = letter

    def update_yellow(self, letter, position):
        self.update_use(letter)
        if position not in self.yellow:
            self.yellow[position] = [letter]
        elif letter not in self.yellow[position]:   # don't add the same letter twice in the same index
                self.yellow[position].append(letter)

    def update_gray(self, letter):
        self.gray.add(letter)
        self.update_use(letter)

class Dictionary:
    def __init__(self):

        self.feedback = GuessStatus()

        self.guesses = self.get_words_from_file('Data/valid_guesses.csv')
        self.answers = self.get_words_from_file('Data/valid_solutions.csv')
    #    self.answers = self.get_words_from_file('Data/valid_guesses.csv')

        self.frequency = self.generate_letter_frequency(self.answers)
    #    self.word_scores = self.calculate_word_scores(self.guesses + self.answers, False)

    def get_words_from_file(self, filename):
        word_arr = []
        with open(filename, 'r') as words:
            for word in words:
                word_arr.append(word.strip().upper())

        return word_arr

    def generate_letter_frequency(self, answers):

        frequency = dict()
        for word in answers:
            for position, letter in enumerate(word):
                if letter not in frequency:
                    frequency[letter] = LetterInfo(letter, position)
                else:
                    lett = frequency[letter]
                    lett.add(position)
        return frequency

    def get_word_score(self, word, by_position = True):

        scores = dict()
        if by_position:
            for i, letter in enumerate(word):
                this_score = self.frequency[letter][i]
                if letter not in scores or scores[letter] < this_score:
                    scores[letter] = this_score
        else:
            for letter in word:
                scores[letter] = self.frequency[letter].total
        score = functools.reduce(lambda a, b: a + b, scores.values())
        return score

    def calculate_word_scores(self, words, by_position = True):
        
        word_dict = dict()
        count = 0
        for word in words:
                word_dict[word] = self.get_word_score(word, by_position)
                count += 1

        sorted_word_dict = sorted(word_dict.items(), key = lambda item: item[1], reverse = True)
        return sorted_word_dict

    def register_guess(self, guess):
        if guess in self.answers:
            self.answers.remove(guess)
        if guess in self.guesses:
            self.guesses.remove(guess)

    def filter_answers(self, word):
        # Remove words that have yellow letters in yellow spots         
        for position, letters in self.feedback.yellow.items():
            for letter in letters:
                if letter not in word or word[position] == letter:
                    return False
        
        # Remove words that have gray letters
        for letter in self.feedback.gray:
            if letter in word:
                return False
            
        # Remove words that don't have green letters in green spots
        for position, letter in self.feedback.green.items():
            if word[position] != letter:
                return False

        return True

    def update_answers(self, answers):
        filtered_word = list()

        for i in range(len(answers)):
            if(self.filter_answers(answers[i]) == True):
                filtered_word.append(answers[i])

        return filtered_word
    
    def get_next_guess(self):
        if self.feedback.get_used() == 0:
            return
        
        # always update answers first
        self.answers = self.update_answers(self.answers)

        # first word in answers    
        return self.answers[0]

class CSPSolver:
    def __init__(self, target):
        self.dictionary = Dictionary()

        # store guessed words
        self.guess_list = list()
        self.target = target.upper()

        self.is_solved = False

    def generate_feedback(self, guess):
        for (index, letter) in enumerate(guess):
            if letter in self.target:
                if self.target[index] == letter:
                    # letter is in correct position: green
                    self.dictionary.feedback.update_green(letter, index)
                else:
                    # letter is not in the correct position: yellow
                    self.dictionary.feedback.update_yellow(letter, index)
            else:
                # letter is not in the word: gray
                self.dictionary.feedback.update_gray(letter)

    def solve(self, starting_word = "SALET"):
        guess = starting_word if starting_word else self.dictionary.get_next_guess()

        while not self.is_solved:
            # Keep track of words and letters guessed
            self.guess_list.append(guess)
            self.dictionary.register_guess(guess)

            if guess == self.target:
                self.is_solved = True
                break
            else:
                self.generate_feedback(guess)
                guess = self.dictionary.get_next_guess()

        return (guess, len(self.guess_list), self.guess_list)
    