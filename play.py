from DataManager import DataManager
from GameManager import GameManager


def play_wordle(data: DataManager) -> bool:
    """ Play Wordle using user input (without the AI solver). Returns true iff user wins. """
    random_answer = data.get_random_answers(1)[0]
    print(random_answer)
    game = GameManager(data.guess_words)
    is_win = game.start(random_answer, use_AI=False)
    return is_win


def main():
    data = DataManager()
    play_wordle(data)
    

if __name__ == '__main__':
    main()
    