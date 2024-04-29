from wordle_csp_solver import Dictionary
from wordle_csp_solver import CSPSolver

def main():
    print("Let solve Wordle!")

    starting_word = "SLATE"

    count = 0

    words = Dictionary().answers
    for word in words:
        print("Running Wordle: ", count, word)
        count += 1
        datam = CSPSolver(word).test(starting_word)

        """
        data_row = {'Answer': guess,
                    'Guess Count': self.guess_count,
                    'Success' :  successful,
                    'Avg Guess Time (ms)': 1000 * avg_guess_time,
                    'Game Duration (ms)' : 1000 * game_duration}
                    #'Max RAM (MB)' : max_ram} 
        """

        if(count == 100):
            break

if __name__ == '__main__':
    main()

