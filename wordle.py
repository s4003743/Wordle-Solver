import random
from util import *

FILENAME = "5-letter-words.txt"

class Wordle():

    def __init__(self):
        """
        Inititalise game state for Wordle. Behaves similarly to the NYT game.
        """
        
        self.valid_words = load_data(FILENAME)
        self.turn_counter = 0
        self.player_won = False
        self.correct_word : str
        self.used_words = set()

        self.generate_word()


    def generate_word(self) :
        """
        Randomly picks out a word from the valid list and assigns it to `self.correct_word`.
        """

        self.correct_word = random.choice(tuple(self.valid_words))

    def make_guess(self, guess : str) -> list:
        """
        Player makes guess. Check validity, check game over, remove from `valid_words`.
        """

        if self.is_valid_word(guess):
            self.used_words.add(guess)
            self.turn_counter += 1
        else:
            return None

        if self.correct_word == guess:
            self.player_won = True
        
        return compute_feedback(guess, self.correct_word)

        
    def game_over(self) -> bool:
        """
        Takes in current game state and returns a boolean value if the player 
        has run out of turns or has guessed the correct word.
        """
        
        if self.turn_counter >= 6:
            return True
        
        return self.player_won

    def is_valid_word(self, word : str) -> bool:
        """
        Checks whether the inputted `word` is valid.
        """

        is_word = word.isalpha()
        correct_length = len(word) == 5
        valid = word in self.valid_words and word not in self.used_words
        
        return is_word and correct_length and valid

