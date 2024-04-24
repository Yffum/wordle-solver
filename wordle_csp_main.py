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
        (answer, guess_count, guess_list) = CSPSolver(word).solve(starting_word)
        print(answer, guess_count, guess_list)

        if(guess_count <= 6):
            print(answer, " is correct! You win!")
        else:
            print(answer, " is correct! But, turn is over. You lose!")

    #    if(count == 100):
    #        break

if __name__ == '__main__':
    main()

