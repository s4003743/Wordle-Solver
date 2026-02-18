from util import *
import math

FILENAME = "5-letter-words.txt"

class Solver():

    def __init__(self):
        """
        Initialises solver class.
        """
        self.all_words = load_data(FILENAME)
        self.possible_words = self.all_words
        self.used_words = set()
    
    def update_state(self, guess : str, feedback : list) -> None:
        """
        Takes in a `guess` and list of `feedback` in order to reduce the 
        possible words in `self.possible_words`
        """

        result = set()
        
        for word in self.possible_words:
            if compute_feedback(guess, word) == feedback:
                result.add(word)
        
        self.used_words.add(guess)
        self.possible_words = result
        
    def generate_suggestion(self, minimax = False) -> str:
        """
        Returns a suggested word based on prior computation.
        """

        word = (
            self.get_max_freq_word() if not minimax 
            else self.get_best_minimax_word()
        )

        return word if word else None
    
    def get_best_minimax_word(self) -> str:
        """
        Returns the word in `self.all_words` with the smallest max partition. 
        This score is being derived from the reduction power in the state space.
        Since a higher reduction means fewer word possiblilities remaining.
        """

        if len(self.possible_words) <= 2:
            return next(iter(self.possible_words))

        best_word : str = None
        min_score = math.inf
        
        for word in self.all_words:
            
            # Avoids repeating previously guessed words
            if word in self.used_words:
                continue

            partition = dict()

            for answer in self.possible_words:
                feedback = tuple(compute_feedback(word, answer))

                if feedback in partition:
                    partition[feedback] += 1
                else:
                    partition[feedback] = 1
            
            score = max(partition.values())

            if score < min_score:
                best_word, min_score = word, score
        
        return best_word

    
    def get_max_freq_word(self) -> str:
        """
        Returns the word in `self.possible_words` with the highest score. 
        The score being derived from the frequency count of each letter.
        Since a higher score means the word elimates more possiblilities.
        """

        letter_freq = get_letter_freq(self.possible_words)
        word_scores = dict()

        for word in self.possible_words:
            score = 0
            for char in word:
                score += letter_freq[char]
            
            if len(set(word)) < len(word):
                score -= len(set(word)) < len(word)

            word_scores[word] = score
        
        return max(word_scores, key=word_scores.get) if self.possible_words else None

    