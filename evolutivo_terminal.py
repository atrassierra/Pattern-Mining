import random
import array
import numpy

from deap import base, creator, tools, algorithms

import argparse
import logging

def crossover(ind1, ind2):
    """
    crossover function:
    It produces a crossover between two random positions
    """
    while True:
        ind1_position = random.randint(0, len(ind1) - 1)
        ind2_position = random.randint(0, len(ind2) - 1)
        var_aux = ind2[ind2_position]
        ind2[ind2_position] = ind1[ind1_position]
        ind1[ind1_position] = var_aux

        if len(set(ind1)) == len(ind1) and len(set(ind2)) == len(ind2):
            return ind1, ind2

def run(args):
    random.seed(1234)
    infinito = float("inf")

    #Setting loggin level
    logging.basicConfig(level=logging.INFO)

    #Splitting and translating files
    with open(args.input_file, "r") as inp:
        class_type = []
        tracts = []
        count = 1
        number_to_name, name_to_number = dict(), dict()
        for line in inp:
            line = line.strip("\n").split(",")

            #Looking for classes
            if line[-1] not in class_type:
                class_type.append(line[-1])

            #Translating names to number and creating dictionaries
            for position in range(len(line[:-1])):
                if line[position] not in name_to_number:
                    name_to_number[line[position]] = count
                    number_to_name[count] = line[position]
                    count += 1

                line[position] = name_to_number[line[position]]

            #Splitting into diffents classes [[Europeans], [Americans], [...]]
            try:
                tracts[class_type.index(line[-1])].append(frozenset(line[:-1]))
            except:
                tracts.append([frozenset(line[:-1])])

        #Setting max number assigned as a variable. It reduces processing time
        max_num = max(number_to_name)
        print(len(number_to_name), len(name_to_number))
    def mutation(individual):
        """
        Mutation function:
        It changes one element to random int between 1 and max_numself
        Inside run() because it needs args values
        """
        while True:
            individual[random.randint(0, len(individual) - 1)] = random.randint(1, max_num)
            if len(set(individual)) == len(individual):
                return individual,


    def run_evolutive(main_set, comparison_set):

        def random_tract():
            """
            Extraction individuals function:
            Extract k random items from a random registry of the main_set
            Inside run() because it needs args values
            Inside run_evolutive because it needs main_set statement
            """

            while True:
                prov_selection = random.choices(list(random.choice(main_set)), k = random.randint(1,args.length_itemset))

                if len(set(prov_selection)) == len(prov_selection):
                    return sorted(prov_selection)


        def growth_ratio_evaluation(individual):
            """
            Individuals evaluation function:
            Calculate GR between main_sets and comparison_set
            Inside run() because it needs args values
            Inside run_evolutive because it needs main_set statement
            """

            support_set_a = 0
            support_set_b = 0
            set_individual = frozenset(individual)
            for registry in main_set:
                if set_individual.issubset(registry):
                    support_set_a += 1
            for registry in comparison_set:
                if set_individual.issubset(registry):
                    support_set_b += 1
            try:
                return float(support_set_a/support_set_b), support_set_a
            except ZeroDivisionError:
                if support_set_a != 0:
                    return float("inf"), support_set_a
                else:
                    return 0.0, support_set_a


        creator.create("FitnessMax", base.Fitness, weights=(1.0, 1.0))
        creator.create("Individual", array.array, typecode = "i", fitness=creator.FitnessMax)

        toolbox = base.Toolbox()
        toolbox.register("caracteristica", random_tract)
        toolbox.register("individual", tools.initIterate, creator.Individual,
                         toolbox.caracteristica)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        toolbox.register("evaluate", growth_ratio_evaluation)
        toolbox.register("mate", crossover)
        toolbox.register("mutate", mutation)
        toolbox.register("select", tools.selTournament, tournsize = args.tournament_size)

        pop = toolbox.population(n = args.population_size)

        fitnesses = list(map(toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        for generation in range(args.generation_number):
            logging.info(f"\t\tGeneration {str(generation + 1)}/{str(args.generation_number)}")
            # Select the next generation individuals
            offspring = toolbox.select(pop, len(pop))
            # Clone the selected individuals
            offspring = list(map(toolbox.clone, offspring))

            # Apply crossover on the offspring
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < args.crossover_rate:
                    toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            # Apply mutation on the offspring
            for mutant in offspring:
                if random.random() < args.mutation_rate:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values

            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)

            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            # Adding offsping
            pop = pop + offspring
            pop = sorted(pop, key=lambda x: x.fitness.values, reverse=True)

            rep_set = list()
            for individual_position in range(len(pop)):
                if set(pop[individual_position]) in rep_set:
                    pop[individual_position] = 0
                else:
                    rep_set.append(set(pop[individual_position]))

            new_pop = []
            for individual in pop:
                if individual != 0:
                    new_pop.append(individual)
            pop = new_pop[:args.population_size]
            logging.info(f"\t\tJumping Emerging Patterns: {str(list(map(lambda x: x.fitness.values[0], pop[:args.number_itemset])).count(infinito))}")

        #del creator.FitnessMax
        #del creator.Individual

        return pop[:args.number_itemset]

    with open(args.output_file, "w") as out:
        run_times = 0
        for main_set in class_type:
            logging.info(f"Class selected {main_set}")
            out.write(main_set + "\n")

            for comparison_set in class_type:
                if main_set != comparison_set:
                    run_times += 1
                    logging.info(f"\tRunning {main_set} vs. {comparison_set} ({run_times}/{len(tracts) * len(tracts) - len(tracts)})")
                    out.write(main_set + " -> " + comparison_set + "\n")
                    results = run_evolutive(tracts[class_type.index(main_set)],
                                            tracts[class_type.index(comparison_set)])
                    for element in results:
                        line = []
                        for item in element:
                            line.append(number_to_name[item])
                        out.write(" -> ".join(line)
                                  + ","
                                  + str(element.fitness.values[0])
                                  + ","
                                  + str(element.fitness.values[1])+ "\n")



def main():
    parser = argparse.ArgumentParser(
        description = "Evolutive frequent itemset mining algorithm."
    )

    parser.add_argument("-i", "--input_file",
                        help = "Input .csv file name.",
                        type = str, action = "store")
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
                        default = 50)
    parser.add_argument("-p", "--population_size",
                        help = "Set population size.",
                        type = int, action = "store",
                        default = 300)
    parser.add_argument("-t", "--tournament_size",
                        help = "Set tournament size.",
                        type = int, action = "store",
                        default = 2)
    parser.add_argument("-l", "--length_itemset",
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

    arguments = parser.parse_args()
    run(arguments)

if __name__ == "__main__":
    main()
