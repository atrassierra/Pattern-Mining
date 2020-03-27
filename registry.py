import statistics as st
from individual import Individual
import argparse

class Registry():
    """
    This class is intended for retrieve summarize statistics from the elite at a given generation

        * Attributes
            @self.elite => Objeto de clase elite

            @self.args => Objeto de clase ArgParse, contine información sobre los comandos en línea.

            @self.registry => Lista de diccionarios donde cada posicion es una generacion que contiene
            un diccionario con las clases y metricas de cada poblacion en la generacion X

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
    def __init__(self, elite):
        '''
        Crea un diccionario con el numero de generacion, dentro de eso, las clases y de dentro las
        estadisticas
        '''
        self.elite = elite
        self.registry = []

    def maxFitness(self, group):
        '''
        Agrega al diccionario principal una lista con el fitness maximo para la generacion actual
        '''
        bestInd = self.elite.elite[group][0]
        fitnessValues = []
        for comparison in bestInd.fitness.keys():
            if comparison[0] == group:
                fitnessValues.append(bestInd.fitness[comparison][0])
                support = bestInd.fitness[comparison][1]
        fitnessValues = list(fitnessValues, support)
        return fitnessValues

    def minFitness(self, group):
        '''
        Agrega al diccionario principal una lista con el fitness maximo para la generacion actual
        '''
        worstInd = self.elite.elite[group][-1]
        fitnessValues = []
        for comparison in worstInd.fitness.keys():
            if comparison[0] == group:
                fitnessValues.append(worstInd.fitness[comparison][0])
                support = worstInd.fitness[comparison][1]
        fitnessValues = list(fitnessValues, support)
        return fitnessValues

    def meanFitness(self, group):
        '''
        Agrega al diccionario principal la media del fitness de la generacion actual para el grupo dado
        '''
        grList = []
        supportList = []
        for individual in self.elite.elite[group]:
            for comparison in individual.fitness.keys():
                if comparison[0] == group:
                    grList.append(individual.fitness[comparison][0])
                    support = individual.fitness[comparison][1]
            supportList.append(support)
        return list(st.mean(grList), st.mean(supportList))

    def medianFitness(self, group):
        fitnessValues = []
        medianInd = round(len(self.elite.elite[group]) / 2)
        for comparison in self.elite.elite[group][medianInd].fitness.keys():
            if comparison[0] == group:
                fitnessValues.append(self.elite.elite[group][medianInd].fitness[comparison][0])
                support = self.elite.elite[group][medianInd].fitness[comparison][1]
        fitnessValues = list(fitnessValues, support)
        return fitnessValues

    def stdevFitness(self, group):
        grList = []
        supportList = []
        for individual in self.elite.elite[group]:
            for comparison in individual.fitness.keys():
                if comparison[0] == group:
                    grList.append(individual.fitness[comparison][0])
                    support = individual.fitness[comparison][1]
            supportList.append(support)
        return list(st.stdev(grList), st.stdev(supportList))

    def updateRegistry(self, elite):
        '''
        Se llama a este metodo y actualiza todo el registro para la generacion actual
        Hay que pasarle el grupo en formato AMR, no comparacion (AMR, EUR)
        Generation es un entero entre 0 y Nº de generaciones - 1
        '''

        generation = dict()
        for group in self.elite.elite:
            generation[group] = dict()

        for group in generation:
            generation[group]["maxFitness"] = self.maxFitness(group)
            generation[group]["minFitness"] = self.minFitness(group)
            generation[group]["meanFitness"] = self.meanFitness(group)
            generation[group]["medianFitness"] = self.medianFitness(group)
            generation[group]["stdevFitness"] = self.stdevFitness(group)

        self.registry.append(generation)