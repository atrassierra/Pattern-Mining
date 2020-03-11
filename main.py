import random
import argparse
import statistics as st

from population import Population

def division(a, b):
    try:
        return float(a / b)
    except ZeroDivisionError:
        return float("inf")


def run(args):
    population = Population(args)


def main():
    parser = argparse.ArgumentParser(
        description = "Evolutive frequent itemset mining algorithm."
    )

    parser.add_argument("-i", "--input_file",
                        help = "Input .csv file name.",
                        type = str, action = "store",
                        default = "prueba.csv")

    parser.add_argument("-o", "--output_file",
                        help = "Output .csv file name.",
                        type = str, action = "store")

    parser.add_argument("-n", "--number_itemset",
                        help = "Return top n itemsets.",
                        type = int, action = "store",
                        default = 10)

    parser.add_argument("-g", "--generation_number",
                        help = "Number of generations to run.",
                        type = int, action = "store",
                        default = None)

    parser.add_argument("-p", "--population_size",
                        help = "Set population size.",
                        type = int, action = "store",
                        default = 300)

    parser.add_argument("-t", "--tournament_size",
                        help = "Set tournament size.",
                        type = int, action = "store",
                        default = 2)

    parser.add_argument("-l", "--min_length_itemset",
                        help = "Minimum itemset length.",
                        type = int, action = "store",
                        default = 2)

    parser.add_argument("-L", "--max_length_itemset",
                        help = "Maximum itemset length.",
                        type = int, action = "store",
                        default = 10)

    parser.add_argument("-c", "--crossover_rate",
                        help = "Set crossover rate (float).",
                        type = float, action = "store",
                        default = 0.5)

    parser.add_argument("-m", "--mutation_rate",
                        help = "Set mutation rate (float).",
                        type = float, action = "store",
                        default = 0.5)

    parser.add_argument("-s", "--support_threshold",
                        help = "Set minimum support threshold (integer).",
                        type = int, action = "store",
                        default = 50)

    parser.add_argument("-r", "--reset_population",
                        help = "Set numbers of resets",
                        type = int, action = "store",
                        default = 3)

    parser.add_argument("-it", "--improvement_threshold",
                        help = "Set minimum improvement threshold to reset",
                        type = float, action = "store",
                        default = 0.01)

    parser.add_argument("-gc", "--generation_chance",
                        help = "Set max number of generation without an improvement of -t",
                        type = int, action = "store",
                        default = 20)

    parser.add_argument("-es", "--elite_size",
                        help = "Set the size of the elite",
                        type = int, action = "store",
                        default = 10)

    arguments = parser.parse_args()
    run(arguments)


if __name__ == "__main__":
    main()