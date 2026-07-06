# Crossword CSP Solver: Word vs. Letter Backtracking

## Overview
This project is an Artificial Intelligence solver for crossword puzzles. It models crossword generation and solving as a **Constraint Satisfaction Problem (CSP)** and solves it using **Backtracking Search** combined with inference algorithms.

This repository contains the final project for the **Artificial Intelligence** (*Intelligenza Artificiale*) exam at the **University of Florence** (*Università degli Studi di Firenze*). The implementation is inspired by the constraint satisfaction exercises from the textbook *Artificial Intelligence: A Modern Approach (AIMA)*.
> **Note:** Imported from [https://codeberg.org/samuele_ruotolo/Samuele-Ruotolo](https://codeberg.org/samuele_ruotolo/Samuele-Ruotolo) as the original project submission was required on Codeberg.

The core feature of this repository is the **comparative analysis** of two distinct CSP formulations:
1. **Word-Based CSP:** Variables are the sequences of blank cells (horizontal or vertical), and the domain consists of full words from a dictionary.
2. **Letter-Based CSP:** Variables are the individual blank cells in the grid, and the domain consists of the letters of the alphabet (a-z).

The program runs both models across datasets of randomly generated grids (dimensions: 5x6, 6x7, 7x8) and dictionaries of varying sizes (50k, 100k, 150k words) to compare their efficiency, execution times, and computational steps.

## AI Concepts & Algorithms
Both CSP models implement the following algorithms to optimize the search space:
* **Arc Consistency (AC-3):** Used as a preprocessing step and for inference during the backtracking search to reduce domain sizes early.
* **Backtracking Search:** A depth-first search that tests assignments and backtracks upon constraint violations. To handle computationally expensive grids, a cutoff limit of `20,000` steps is enforced.
* **Heuristics:**
  * **Minimum Remaining Values (MRV):** Selects the next unassigned variable that has the fewest valid options remaining in its domain.
  * **Least Constraining Value (LCV):** Orders the domain values by prioritizing the ones that rule out the fewest options for neighboring variables.

## Project Structure
The repository is organized into the main Python scripts at the root level and a `Files/` directory for datasets and outputs.

```text
.
├── Files/
│   ├── 50000_words.txt, 100000_words.txt, 150000_words.txt  # Dictionaries
│   ├── Dataset.txt                                          # Saved crossword grid datasets
│   ├── Word Solutions.txt, Letter Solutions.txt             # Output solution logs
│   └── Results.png                                          # Matplotlib comparison graphs
├── Relazione.pdf               # Detailed project report (in Italian)
├── main.py                     # Entry point of the application
├── test.py                     # Test runner and matplotlib graphing logic
├── constants.py                # Configuration (dimensions, paths, probabilities)
├── crosswordGrid.py            # Grid generation logic
├── wordBacktrack.py / letterBacktrack.py                    # Backtracking & AC-3 logic
└── wordCrosswordProblem.py / letterCrosswordProblem.py      # CSP problem definitions
```
*(Note: additional helper classes like `wordVariable.py`, `letterCSPConstraint.py`, etc., are also included in the root).*

## Documentation
For a deeper theoretical explanation, methodology, and detailed performance comparisons across different grid dimensions and dictionary sizes, please consult the official report (written in Italian): **[`Relazione.pdf`](Relazione.pdf)**.

## Prerequisites
To run this project, you need **Python 3.12+** installed, along with the `matplotlib` library for generating the results graph.

```bash
pip install matplotlib
```

## How to Run
To execute the tests and generate the performance comparison:

```bash
# 1. Clone the repository
git clone [https://github.com/sruotolo/crossword_backtracking_search.git](https://github.com/sruotolo/crossword_backtracking_search.git)
cd crossword_backtracking_search

# 2. Run the main script
python main.py
```

Upon execution, the program will load or generate the crossword grids, solve them, output the textual results into `Files/`, and generate a comparative chart saved as `Results.png`.
