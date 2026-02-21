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

I chose python becuase it's an abstract language that would allow me to focus on the higher-level logic since performance optimisation isn't currently my focus compared to efficacy (I'm relatively new to programming projects). I divided the code up into 4 main python files; `play.py`, `solver.py`, `util.py`, `wordle.py`. The names are self-explanatory; play manages the game loop, solver manages the functions for suggesting optimal guesses, wordle manages the game features itself and util manages general functions.

### Play.py

`play.py` is responsible for managing the overall game loop and user interaction. It ties everything together.

The core responsibilities are:

- Displaying the banner and available game modes.
- Initialising the `Wordle` and `Solver` classes.
- Handling user input.
- Passing guesses and feedback between the game and solver.
- Terminating the loop when the game ends.

There are several modes available:

- `c`  -> Classic mode (no suggestions).
- `th` -> Tips using heuristic scoring.
- `tm` -> Tips using minimax scoring.
- `mh` -> Manual mode using heuristic.
- `mm` -> Manual mode using minimax.

Manual mode allows the user to enter colour feedback manually rather than relying on the built-in `Wordle` engine. This makes it possible to use the solver against the official New York Times version.

The play loop is intentionally simple:

1. Generate a suggestion (if in tips/manual mode).
2. Obtain feedback (either computed or entered manually).
3. Update the solver state.
4. Repeat until player win or loss.

---

### Wordle.py

`wordle.py` contains the actual game mechanics.

Its main responsibilities are:

- Selecting a valid answer from the list of 5-letter words.
- Checking whether a guess is valid.
- Computing feedback for a guess.
- Tracking the number of turns taken.
- Determining whether the player has won or lost.

The key idea here is that feedback is deterministic. Given:

```
guess
answer
```

the result will always be the same pattern of greens, yellows, and greys.

Because of this determinism, the solver can simulate feedback without knowing the true answer — it simply treats each possible word as a hypothetical answer and partitions the remaining word list accordingly.

---

`solver.py` is the most interesting file in the project. It manages:

- The set of possible remaining words.
- The set of used guesses.
- The suggestion algorithm (heuristic or minimax).
- State updates after receiving feedback.

Conceptually, the solver works as follows:

1. Start with the full list of valid 5-letter words.
2. After each guess and feedback:
   - Remove all words that would not produce the same feedback.
3. Choose the next guess according to the selected algorithm.

Because feedback is deterministic, this process progressively shrinks the candidate set until only one word remains.

The solver does not "know" the correct word — it simply eliminates impossibilities Sherlock Holmes style.

---

### Util.py

`util.py` contains shared utility functions. These include:

- Converting feedback strings (`b/y/g`) into numeric lists.
- Computing feedback between two words.
- Loading the word list.
- Miscellaneous helpers used across files.

Separating this logic prevents duplication and keeps the other modules cleaner. Since both the Wordle engine and Solver would require some of these.

---

## Heuristic Algorithm

The heuristic approach assigns a score to each candidate word based on letter frequency.

Conceptually:

- Letters that appear frequently in the remaining candidate words are more valuable.
- Words containing many high-frequency letters are more informative.
- Duplicate letters are usually penalised early on, since discovering five unique letters is more efficient in narrowing the search space (my current penalty isn't very strong thus is rendered insignificant).

In short, the heuristic tries to maximise information gain indirectly by favouring statistically common letters.

### Why it works well

- Extremely fast.
- Requires only counting letter frequencies.
- Scales easily even with thousands of candidate words.
- Produces strong early-game guesses.

Time complexity per turn is roughly:

```
O(5n) -> O(n)
```

where `n` is the number of remaining words.

This makes it very practical. Note that in order to further increase efficiency, you could change the function into a "stream" like maximum finder ranther than storing every word and then finding the maximum. However the program already works so fast that the time savings felt here wouldn't be noticed until a much larger scale of words were processed than the current list.

### Weaknesses

- It does not explicitly consider worst-case outcomes.
- It may choose a word that looks informative statistically but splits the search space poorly.
- Performance can degrade late in the game when fine-grained partitioning matters more than raw letter frequency.

In practice, it is efficient but not theoretically optimal. For example consider the possibilty that we have a result of `bgggg`. We know we only need the last letter in order to find the correct word, however we also know that attempting different words with only the first letter changed can only reduce the possibility space by one word (since there are no duplicates). The program would search through all possible words and find they all have a roughly equal score (the last four letter appear in all of them and the first letter will only appear once unless it contains a duplicate within the word). Therefore it would constantly guess one word at a time only eliminating one word at a time. A human in this scenario might deliberately choose a word they knowis incorrect in order to gain more information from it (eliminate multiple letters). Such a strategy will be explained below.

---

## Minimax Algorithm

The minimax algorithm is significantly more computationally expensive but more principled.

For each candidate guess:

1. Simulate that guess against every possible remaining answer.
2. Partition the remaining word list by feedback pattern.
3. Determine the size of the largest partition (worst-case scenario).
4. Choose the guess that minimises this worst-case partition size.

In other words, minimax asks:

"If I play this word, what is the worst possible reduction in my search space?"

It then chooses the guess that keeps that worst-case as small as possible.

### Why it is powerful

- It explicitly minimises worst-case uncertainty.
- It produces strong mid- and late-game performance.
- It avoids guesses that leave large ambiguous partitions.

Conceptually, it is closer to an optimal decision strategy.

---

### Performance Trade-Off

The cost is significant.

If there are `n` possible words, minimax roughly requires:

```
O(n^2 * feedback cost)
```

On the first move, with ~3000 words: 3000 × 3000 ≈ 9,000,000 comparisons. Even though each feedback computation is small, this quickly dominates runtime. This is why the first minimax move is noticeably slower than the heuristic approach.

---

### Effectiveness Trade-Off

| Algorithm  | Speed       | Early Game | Late Game | Theoretical Soundness |
|------------|------------|------------|-----------|------------------------|
| Heuristic  | Very fast  | Strong     | Sometimes weaker | Indirect |
| Minimax    | Slow       | Good       | Very strong | Explicitly optimal (worst-case) |

In practice:

- The heuristic feels immediate and responsive.
- Minimax feels slower but more methodical.
- For most casual usage, the heuristic is sufficient.
- For guaranteed worst-case reduction, minimax is superior.

---

## Future Improvements

Some possible directions for improvement:

- Cache feedback results to avoid recomputing identical `(guess, word)` pairs.
- Precompute feedback partitions.
- Use entropy instead of minimax (expected information gain rather than worst-case).
- Parallelise minimax comparisons.
- Store word lists in more efficient structures.
- Add benchmarking tools to compare average guess counts across algorithms.
- Improve UI using the `rich` library further (tables, colours, animations).

---

## Closing Remarks

This project was primarily an exercise in structuring a small program cleanly and exploring different algorithmic approaches to the same problem.

The key takeaway is that even a simple game like Wordle can demonstrate:

- Deterministic state reduction
- Search-space partitioning
- Greedy heuristics vs adversarial optimisation
- Performance vs optimality trade-offs

While the code is not heavily optimised (I might have a crack at it in the future), the structure allows for future experimentation and refinement. I had a lot of fun making this as a beginner project.


