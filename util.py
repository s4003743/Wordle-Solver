from rich.console import Console
from rich.text import Text
from rich.table import Table
from rich.panel import Panel
from rich.traceback import install
from collections import Counter

install()   # For better tracebacks

def print_mode_options() -> None:
    """
    Prints table of mode options for the user.
    """

    console = Console()

    table = Table(title="Wordle Game Modes", show_lines=True)

    table.add_column("Code", style="cyan", justify="center")
    table.add_column("Mode", style="bold magenta")
    table.add_column("Description", style="green")

    table.add_row("c", "Classic", "No hints, just play")
    table.add_row("th", "Tips Heuristic", "Uses frequency-based word scoring")
    table.add_row("tm", "Tips Minimax", "Uses minimax scoring to reduce possibilities")
    table.add_row("mh", "Manual Heuristic", "You enter the colors; program guesses using Heuristic")
    table.add_row("mm", "Manual Minimax", "You enter the colors; program guesses using Minimax")

    console.print(Panel(table, border_style="bright_blue"))

def print_banner() -> None:
    """
    Prints banner for game.
    """
    banner = r"""
 __          __           _ _           _____       _                
 \ \        / /          | | |         / ____|     | |               
  \ \  /\  / /__  _ __ __| | | ___    | (___   ___ | |_   _____ _ __ 
   \ \/  \/ / _ \| '__/ _` | |/ _ \    \___ \ / _ \| \ \ / / _ \ '__|
    \  /\  / (_) | | | (_| | |  __/    ____) | (_) | |\ V /  __/ |   
     \/  \/ \___/|_|  \__,_|_|\___|   |_____/ \___/|_| \_/ \___|_|                                                                                             
    """
    print(banner)  


def validate_feedback(feedback : str) -> bool:
    """
    Takes a string of 5 letters and ensures it can be converted into the feedback list.
    """

    valid_char = ['y','b','g']
    length = len(feedback) == 5
    chars = True

    for char in feedback:
        if char not in valid_char:
            chars = False
            break

    return length and chars


def feedback_to_list(feedback : str) -> list:
    """
    Converts text into result list. For example `"yybgb"` becomes `[0, 0, -1, 1, -1]`
    """

    if not validate_feedback(feedback):
        return None
    
    result = []
    
    for char in feedback:
        if char == 'b':
            result.append(-1)
        elif char == 'y':
            result.append(0)
        elif char == 'g':
            result.append(1)
    
    return result


def get_letter_freq(words : set) -> dict:
        """
        Counts letter frequency. Returns a dict with key, value pairs for 
        letters and their respective frequency.
        """

        result = dict()
        for w in words:
            for char in w:
                if char in result.keys():
                    result[char] += 1
                else:
                    result[char] = 1    
        return result


def display_result(player_won : bool, turn_counter : int, correct_word : str) -> None:
    """
    Display result message depending on whether the player has won or lost.
    """
    if player_won and turn_counter < 4:
        print("Wow!")
    elif player_won and turn_counter == 6:
        print("Phew!")
    elif player_won:
        print("Good Job!")
    else:
        print("Better Luck Next Time!")
        print("Answer: " + correct_word)


def display_feedback(guess : str, result : list) -> None:
    """
    Display feedback in a similar fashion to NYT Wordle using the `rich` library.
    """

    console = Console()

    text = Text()
    for letter, fb in zip(guess, result):
        if fb == 1:
            text.append(letter.upper(), style="bold white on green")
        elif fb == 0:
            text.append(letter.upper(), style="bold white on yellow")
        else:
            text.append(letter.upper(), style="bold white on grey37")
        text.append(" ")
    console.print(text)


def load_data(filename : str) -> set:
        """
        Takes in String `filename` and reads a set of valid words into `valid_words`. 
        """  

        valid_words = set() 

        try:
            with open(filename) as f: 
                for line in f:
                    word = line.strip().lower()
                    if len(word) == 5 and word.isalpha():
                        valid_words.add(word)

        except FileNotFoundError:
            print("Cannot find file.")
        
        return valid_words


def compute_feedback(guess, answer) -> list:
        """
        Compute feedback as a list for each index in the `guess` word. Values range from 
        -1 to 1 (int) for each letter where -1 -> incorrect, 0 -> wrong index 1 -> correct 
        letter in correct index.
        """
        
        correct_counter = Counter(answer)
        result = [-1, -1, -1, -1, -1]
        
        for index in range(len(guess)):
            if guess[index] == answer[index]:
                result[index] = 1
                correct_counter[guess[index]] -= 1

        for index, char in enumerate(guess):
            if correct_counter[char] > 0 and result[index] != 1: 
                result[index] = 0
                correct_counter[char] -= 1
        
        return result
