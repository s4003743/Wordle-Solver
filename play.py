from wordle import *
from solver import *


def play():
    """
    Playing the wordle game loop
    """

    print_banner()   
    print_mode_options()                       

    game = Wordle()
    solver = Solver()
    
    is_manaul = False
    valid_modes = ['c', 'th', 'tm', 'mm', 'mh']
    mode = None
    while mode not in valid_modes:
        mode = str(input("\nWhich mode? : ")).lower().strip()
 
    is_manaul = mode[0] == 'm'
    is_tips = 't' in mode
    is_minimax = mode[1] == 'm'
    
    while not game.game_over():
        suggestion = ""

        if solver.generate_suggestion() is None:
            print("Cannot provide suggestion.")
            exit()

        if is_tips or is_manaul:
            suggestion = solver.generate_suggestion(is_minimax)

            if len(solver.possible_words) > 1: 
                print("Suggested word : " + suggestion)
                print("Possible words remaining : " + str(len(solver.possible_words)))
            else:
                print("The word is : " + suggestion)
                exit()

        if not is_manaul:
            guess = str(input("Enter guess here (" + str(game.turn_counter + 1) + "/6) : ")).lower().strip()
            result = game.make_guess(guess)
        else:
            guess = suggestion
            result_str = str(input("Result (b/y/g) : ")).lower().strip()
            result = feedback_to_list(result_str)

        if result:
            display_feedback(guess, result)
            solver.update_state(guess, result)
    
    display_result(game.player_won, game.turn_counter, game.correct_word)


if __name__ == "__main__":
    play()