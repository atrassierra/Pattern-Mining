import random
import argparse
import statistics as st

def division(a, b):
    try:
        return float(a / b)
    except ZeroDivisionError:
        return float("inf")

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
            initialSet = group[random.choice(list(self.individual))]
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
                    self.fitness[(firstGroup, secondGroup)] = (division(1, division(self.calculateSupport(self.items[firstGroup]), self.calculateSupport(self.items[secondGroup]))),
                    self.calculateSupport(self.items[firstGroup]))

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
            for gr, support in individual.values():
                if self.args.support_threshold >= support:
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
            for gr, support in individual.values():
                if self.args.support_threshold >= support:
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

    def equalFitness(self, other):
        grCount  = []
        grMean = []

        for individual in (self.fitness, other.fitness):
            auxCount = 0
            auxMean = 0
            for gr, support in individual.values():
                if self.args.support_threshold >= support:
                    gr = 1
                auxCount += 1 if gr == 0 else 0
                auxMean += gr

            auxMean = auxMean / len(self.fitness)

            grCount.append(auxCount)
            grMean.append(auxMean)

        if grCount[0] == grCount[1] and grMean[0] == grMean[1]:
            return True
        else:
            return False


    def __repr__(self):
        toPrint = "\n".join([
            f"Individual: {self.fitness}",
            "\n".join(["\t" + element for element in self.individual])
            ]) + "\n"
        return toPrint