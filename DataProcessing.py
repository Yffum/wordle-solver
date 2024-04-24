from collections import Counter

from GameManager import WORD_LENGTH



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
            else:
                print("Warning:", word, "is not a valid word, and was skipped.")
    return lexicon



def calculate_letter_probability_distribution(lexicon: set) -> list:
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
            # Number of decimal digits
            precision = 5
            # Divide count by lexicon length and round
            table[char] = round(table[char] / len(lexicon), precision)

    # Return probabilities
    return letter_counts

