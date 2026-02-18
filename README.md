# Wordle Solver (Version 1.0)

This is a general overview of the program as well as the logic behind its most important components. Its a relatively small project (took about a day to complete) so there isn't a great deal to talk about. Hopefully I will have covered enough that everything can be understood.

## Setup

For reference I used Python 3.8 for this one. To install the necessary libraries, run the following command in the terminal:

```
pip install -r requirements.txt
```

## General Overview

Wordle is a fun (debatable) game featured by the New York Times. The rules are simple to follow and the actual game can be found [here](https://www.nytimes.com/games/wordle/index.html). I recommend you play the original game before attempting to understand the above code. The game loop is quite simple and is as follows:

```
grey   -> -1
yellow -> 0
green  -> 1

R E A L S -> [0 , 0, -1, 0, -1]
L O G I C -> [1, -1, -1, 0, -1]
A N K L E -> [-1, -1, -1, 0, 0]
L I V E R -> [1, 1, 1, 1, 1] -> Player Won
```

 - Guess a valid 5 letter word.
 - The game goes character by character and colours them according to correctness:
   - If the square has the correct letter in the correct position then it lights up **green**.
   - If the square has the correct letter but not in that postion then it lights up **yellow**.
   - If the square has a letter that isn't found in the correct word it remains **grey**.     
 - If you guess the correct word then the game ends.
 - If you have made 6 guesses without having guessed the correct word, the game is over and the player has lost.

We can infer the more abstract structure based off this game loop:

 - There is a finite amount of 5 letter words in the english language.
 - The feedback we get from each guess is deterministic; the feedback will always be the same for each word and answer pair.
 - The answer is always within the list of 5 letter words.

## Structural Breakdown

I chose python becuase it's an abstract language that would allow me to focus on the higher-level logic since performance optimisation isn't currently my focus compared to efficacy (I'm relatively new to programming projects). I divided the code up into 4 main python files; play.py, solver.py, util.py, wordle.py. The names are self-explanatory; play manages the game loop, solver manages the functions for suggesting optimal guesses, wordle manages the game features itself and util manages general functions.

### Play.py

### Wordle.py

### Solver.py

### Util.py

## Heuristic Algorithm

## Minimax Algorithm

## Future Improvements

