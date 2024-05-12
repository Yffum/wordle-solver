from collections import Counter

from constants import WORD_LENGTH, PRECISION



def import_lexicon(filepath: str='Data/wordle_lexicon.txt') -> set:
    """ Returns a set of words, read from each line in the given file """
    lexicon = set()
    # Open the .csv file
    with open(filepath, 'r') as file:
        # Read each line
        for line in file:
            # Remove any leading or trailing whitespace and capitalize letters
            word = line.strip().upper()
            # If word is valid
            if len(word) == WORD_LENGTH:
                # Add the word to the lexicon
                lexicon.add(word)
            elif not word == '':
                print("Warning:", word, "is not a valid word, and was skipped.")
    return lexicon

def import_lexicon_as_list(filepath: str='Data/wordle_lexicon.txt') -> list:
    """ Returns a set of words, read from each line in the given file """
    lexicon = []
    # Open the .csv file
    with open(filepath, 'r') as file:
        # Read each line
        for line in file:
            # Remove any leading or trailing whitespace and capitalize letters
            word = line.strip().upper()
            # If word is valid
            if len(word) == WORD_LENGTH:
                # Add the word to the lexicon
                lexicon.append(word)
            elif not word == '':
                print("Warning:", word, "is not a valid word, and was skipped.")
    return lexicon

def calculate_letter_probability_distribution(lexicon: set) -> list[Counter]:
    """ Returns a list of Counters. The list index corresponds to the position of the char.
        The Counter keys are letters in the alphabet, and the values are the probability
        of the letter being in that position for the given lexicon. """
    # Each index of letter_counts corresponds to a character position
    # For each position, there is a table of character counts
    letter_counts = [Counter() for i in range(WORD_LENGTH)] 

    # Count characters
    for word in lexicon:
        # Parse each letter in each word
        for position, char in enumerate(word):
            # Add count for corresponding position and letter
            letter_counts[position][char] += 1 

    # Normalize counts by lexicon length to get probabilites
    for table in letter_counts:
        # Calculate probability of each letter at position i
        for char in table: 
            # Divide count by lexicon length and round
            table[char] = round(table[char] / len(lexicon), PRECISION)

    # Return probabilities
    return letter_counts



def get_general_letter_probabilities(words: list[str]) -> Counter:
    """ Returns a Counter containing the normalized frequency of each character
        in the given list of strings (i.e., the number of occurences of each
        character divided by the total number of characters)
        character in the given list of words """ 
    char_counts = Counter()
    total = 0
    # Parse each letter in each word
    for word in words:
        for char in word:
            # Count letter
            char_counts[char] += 1 
            total += 1
            
    # Normalize each count by total number of characters
    for char in char_counts: 
        # Divide count by lexicon length and round
        char_counts[char] = round(char_counts[char] / total, PRECISION)
        
    # char_counts now contains the counts divided by the total number of characters
    return char_counts
