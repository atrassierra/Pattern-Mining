import random
import argparse
import statistics as st

def division(a, b):
    try:
        return float(a / b)
    except ZeroDivisionError:
        return float("inf")

class Data:

    """
    Data class
    Generate a dictionary of dictionaries from a file:

    Dictionary "self.items":
        Group1:
            Item1 : Set("indexes of lines with item1")
            Item2 : Set("indexes of lines with item2")
            ...
        Group2:
            Item1 : Set("indexes of lines with item1")
            Item2 : Set("indexes of lines with item2")
            ...
        ...
    """

    def __init__(self, file):
        self.file = file
        self.items = dict()

        with open(self.file, "r") as inFile:

            for index, line in enumerate(inFile):
                line = line.strip("\r").strip("\n").split(",")
                self.extractData(index, line)

    def extractData(self, index, instance):
        group, instance = instance[-1], set(instance[:-1])

        if group not in self.items.keys():
            self.items[group] = dict()

        for item in instance:
            try:
                self.items[group][item].add(index)
            except KeyError:
                self.items[group][item] = {index}




class Population(Data):

    """
    Population class
    Data class is inherited to have Data.items attribute

    This class contains Indivuduals instances and methods where Individual interacts between them (crossover, tournament, etc...)
    """

    def __init__(self, args):
        self.args = args
        Data.__init__(self, self.args.input_file)

        self.population = []
        for _ in range(self.args.population_size):
            self.population.append(
                Individual(
                    self.items,
                    self.args
                    )
                )

    def crossover(self):
        auxPopulation = []

        for ind1, ind2 in zip(self.population[::2], self.population[1::2]):
            if self.args.crossover_rate >= random.random():
                crossoverPoint = random.randint(0, len(ind1) - 1) if len(ind1) <= len(ind2) else random.randint(0, len(ind2) - 1)

                auxPopulation.append(Individual(self.items, self.args, pattern = set(list(ind1.individual)[:crossoverPoint] + list(ind2.individual)[crossoverPoint:])))
                auxPopulation.append(Individual(self.items, self.args, pattern = set(list(ind2.individual)[:crossoverPoint] + list(ind1.individual)[crossoverPoint:])))

        self.population = auxPopulation


    def tournament(self):
        auxPopulation = [] # Para copiar sin apuntar al mismo sitio en memoria
        for _ in range(0, self.args.population_size):
            best = random.choice(self.population)
            for _ in range(self.args.tournament_size) - 1:
                ind = random.choice(self.population)
                if ind > best:
                    best = ind

            auxPopulation.append(best)
        self.population = auxPopulation

    def runGeneration(self):
        for i in range(self.args.generation_number):
            print("Estamos en la generacion {}").format(i)
            self.tournament()
            self.crossover()
            for individual in self.population:
                individual.mutation()


class Individual:

    def __init__(self, items, args, pattern = None):
        self.args = args
        self.items = items
        if pattern == None:
            self.generateRandomIndividual(self.items[random.choice(list(self.items.keys()))])
        else:
            self.individual = pattern

        self.calculateFitness()

    def generateRandomIndividual(self, items):

        self.individual = set(random.choices(
            list(items.keys()),
            k = random.randint(self.args.min_length_itemset, self.args.max_length_itemset)
            ))

    def calculateSupport(self, group):
        try:
            initialSet = group[random.choice(self.individual)]
        except KeyError:
            initialSet = set()

        for item in self.individual:
            try:
                initialSet.intersection(group[item])
            except KeyError:
                initialSet.clear()

        return len(initialSet)


    def calculateFitness(self):
        self.fitness = dict()

        for firstGroup in self.items:
            for secondGroup in self.items:
                if firstGroup != secondGroup:
                    self.fitness[(firstGroup, secondGroup)] = 1 / division(self.calculateSupport(self.items[firstGroup]), self.calculateSupport(self.items[secondGroup]))

    def mutation(self):
        auxIndividual = list(self.individual)
        while self.args.mutation_rate >= random.random():
            group = random.choice(list(self.items.keys()))
            item = random.choice(list(self.items[group].keys()))
            auxIndividual[random.randint(0, len(auxIndividual) - 1)] = item
            if len(set(auxIndividual)) == len(auxIndividual):
                self.individual = set(auxIndividual)
                self.calculateFitness()


    def __len__(self):
        return len(self.individual)


    def __gt__(self, other):
        grCount  = []
        grMean = []

        for individual in (self.fitness, other.fitness):
            auxCount = 0
            auxMean = 0
            for gr, support in individual:
                if gr == 0 and self.args.support_threshold >= support:
                    gr = 1
                auxCount += 1 if gr == 0 else 0
                auxMean += gr

            auxMean = auxMean / len(self.fitness)

            grCount.append(auxCount)
            grMean.append(auxMean)

        if grCount[0] > grCount[1]:
            return True
        else:
            if grCount[0] == grCount[1]:
                if grMean[0] < grMean[1]:
                    return True
                else:
                    return False
            else:
                return False

    def __lt__(self, other):
        grCount  = []
        grMean = []

        for individual in (self.fitness, other.fitness):
            auxCount = 0
            auxMean = 0
            for gr, support in individual:
                if gr == 0 and self.args.support_threshold >= support:
                    gr = 1
                auxCount += 1 if gr == 0 else 0
                auxMean += gr

            auxMean = auxMean / len(self.fitness)

            grCount.append(auxCount)
            grMean.append(auxMean)

        if grCount[0] < grCount[1]:
            return True
        else:
            if grCount[0] == grCount[1]:
                if grMean[0] > grMean[1]:
                    return True
                else:
                    return False
            else:
                return False


    def __repr__(self):
        toPrint = "\n".join([
            f"Individual: {self.fitness}",
            "\n".join(["\t" + element for element in self.individual])
            ]) + "\n"
        return toPrint



def run(args):
    population = Population(args)
    print(population.population)


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
                        default = 50)

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

    arguments = parser.parse_args()
    run(arguments)


if __name__ == "__main__":
    main()