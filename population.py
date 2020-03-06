import random
import argparse
import statistics as st

from data import Data
from individual import Individual

def division(a, b):
    try:
        return float(a / b)
    except ZeroDivisionError:
        return float("inf")

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
        print(self.population[:5])