from DataManager import DataManager
from GameManager import GameManager
from constants import MAX_GUESS_COUNT


def play_wordle(data: DataManager) -> bool:
    """ Play Wordle using user input (without the AI solver). Returns true iff user wins. """
    random_answer = data.get_random_answers(1)[0]
    game = GameManager(data.guess_words)
    # Uses max guess count of 6 to end game after 6 tries.
    is_win = game.start(random_answer, use_AI=False, guess_limit=MAX_GUESS_COUNT)
    return is_win


def main():
    data = DataManager()
    play_wordle(data)
    

if __name__ == '__main__':
    main()
    