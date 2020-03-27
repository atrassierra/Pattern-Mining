import statistics as st
from individual import Individual
import argparse

class Registry():
    """
    This class is intended for retrieve summarize statistics from the elite at a given generation

        * Attributes
            @self.elite => Dict where the keys are the classes of population and the values are a list of
            the best individuals

            @self.args => Objeto de clase ArgParse, contine información sobre los comandos en línea.

            @self.registry => Diccionario donde se guarda el numero de generacion, dentro de ese numero
            hay otro diccionario con las distintas poblaciones y dentro de cada poblacion se encuentran
            las distintas estadísticas para la generacion dada

        * Methods
            @self.maxFitness => Retunr the gr and support of the best individual of the current
            generation

            @self.minFitness => Return the gr and support of the worst individual of the current
            generation

            @self.meanFitness => Return the mean gr and support of the current elite generation

            @self.medianFitness => Return the median gr and support of the current generation

            @self.stdevFitness => Calculate statistic deviation of gr and support across the
            current elite generation

            @self.updateRegistry => Create a new registry in self.registry dict with the stats of
            the current generation
    """
    def __init__(self, elite, args, items):
        '''
        Crea un diccionario con el numero de generacion, dentro de eso, las clases y de dentro las
        estadisticas
        '''
        self.elite = elite
        self.args = args
        self.registry = dict()
        self.items = items

        for generation in range(self.args.generation_number):
            self.registry[generation] = dict()
            for group in self.elite:
                self.registry[generation][group] = dict()

    def maxFitness(self, group, generation):
        '''
        Agrega al diccionario principal una lista con el fitness maximo para la generacion actual
        '''
        bestInd = self.elite[group][0]
        fitnessValues = []
        for comparison in bestInd.fitness.keys():
            if comparison[0] == group:
                fitnessValues.append(bestInd.fitness[comparison][0])
                support = bestInd.fitness[comparison][1]
        fitnessValues = list(fitnessValues, support)
        self.registry[int(generation)][group]["maxFitness"] = fitnessValues

    def minFitness(self, group, generation):
        '''
        Agrega al diccionario principal una lista con el fitness maximo para la generacion actual
        '''
        worstInd = self.elite[group][-1]
        fitnessValues = []
        for comparison in worstInd.fitness.keys():
            if comparison[0] == group:
                fitnessValues.append(worstInd.fitness[comparison][0])
                support = worstInd.fitness[comparison][1]
        fitnessValues = list(fitnessValues, support)
        self.registry[int(generation)][group]["minFitness"] = fitnessValues

    def meanFitness(self, group, generation):
        '''
        Agrega al diccionario principal la media del fitness de la generacion actual para el grupo dado
        '''
        grList = []
        supportList = []
        for individual in self.elite[group]:
            for comparison in individual.fitness.keys():
                if comparison[0] == group:
                    grList.append(individual.fitness[comparison][0])
                    support = individual.fitness[comparison][1]
            supportList.append(support)
        self.registry[int(generation)][group]["meanFitness"] = list(st.mean(grList), st.mean(supportList))

    def medianFitness(self, group, generation):
        fitnessValues = []
        medianInd = round(len(self.elite[group]) / 2)
        for comparison in self.elite[group][medianInd].fitness.keys():
            if comparison[0] == group:
                fitnessValues.append(self.elite[group][medianInd].fitness[comparison][0])
                support = self.elite[group][medianInd].fitness[comparison][1]
        fitnessValues = list(fitnessValues, support)
        self.registry[int(generation)][group]["medianFitness"] = fitnessValues

    def stdevFitness(self, group, generation):
        grList = []
        supportList = []
        for individual in self.elite[group]:
            for comparison in individual.fitness.keys():
                if comparison[0] == group:
                    grList.append(individual.fitness[comparison][0])
                    support = individual.fitness[comparison][1]
            supportList.append(support)
        self.registry[int(generation)][group]["stdevFitness"] = list(st.stdev(grList), st.stdev(supportList))

    def updateRegistry(self, generation):
        '''
        Se llama a este metodo y actualiza todo el registro para la generacion actual
        Hay que pasarle el grupo en formato AMR, no comparacion (AMR, EUR)
        Generation es un entero entre 0 y Nº de generaciones - 1
        '''
        for group in self.items:
            self.maxFitness(group, generation)
            self.minFitness(group, generation)
            self.meanFitness(group, generation)
            self.medianFitness(group, generation)
            self.stdevFitness(group, generation)