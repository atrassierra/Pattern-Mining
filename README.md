# Evolutive Emerging Pattern algorithm
## Evolutive emerging pattern algorithm for transactional databases.

**evolutivo_terminal.py HELP**: python evolutivo_terminal.py --help

~~~
usage: evolutivo_terminal.py [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                             [-n NUMBER_ITEMSET] [-g GENERATION_NUMBER]
                             [-p POPULATION_SIZE] [-t TOURNAMENT_SIZE]
                             [-l LENGTH_ITEMSET] [-c CROSSOVER_RATE]
                             [-m MUTATION_RATE]

Evolutive frequent itemset mining algorithm.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input_file INPUT_FILE
                        Input .csv file name.
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Output .csv file name.
  -n NUMBER_ITEMSET, --number_itemset NUMBER_ITEMSET
                        Return top n itemsets.
  -g GENERATION_NUMBER, --generation_number GENERATION_NUMBER
                        Number of generations to run.
  -p POPULATION_SIZE, --population_size POPULATION_SIZE
                        Set population size.
  -t TOURNAMENT_SIZE, --tournament_size TOURNAMENT_SIZE
                        Set tournament size.
  -l LENGTH_ITEMSET, --length_itemset LENGTH_ITEMSET
                        Maximum itemset length.
  -c CROSSOVER_RATE, --crossover_rate CROSSOVER_RATE
                        Set crossover rate (float).
  -m MUTATION_RATE, --mutation_rate MUTATION_RATE
                        Set mutation rate (float).
~~~
