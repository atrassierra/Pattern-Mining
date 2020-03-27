import random
import argparse
import statistics as st

from data import Data
from individual import Individual
from elite import Elite
from registry import Registry

def division(a, b):
    try:
        return float(a / b)
    except ZeroDivisionError:
        return float("inf")

class Population(Data):

    """
    Clase Población
    Alberga una lista de individuos y métodos especiales de la población.
    Herencia de la clase Data, para heredar el diccionario de grupos/items/índices de esta.

        * Atributos:
            @atr self.args       => Objeto de clase ArgParse, contine información sobre los comandos en línea.
            @atr self.items      => Diccionario procedente de la clase Data, heredado. Contiene información sobre los items y sus índices de aparición.
            @atr self.population => Lista de objetos de clase Individual.
            @atr self.elite      => Objeto de clase Elite.

        * Métodos
            @def self.__init__      => Inicializador, usado como rama ejecutante (solo es necesaria la instanciación para la ejecución del programa).
            @def self.crossover     => Operador de cruce. Cruza la población dos a dos y la cambia por completo.
            @def self.tournament    => Operador de torneo. Compara n individuos, y se queda con el mejor y cambia la población por completo.
            @def self.runGeneration => Englova la ejecución de todos los operadores evolutivos (torneo, cruce y mutación).
            @def self.runEvolutive  => Se encarga de lanzar todas las generaciones y el control entre las mismas.
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
        self.elite = Elite(self.args, list(self.items.keys()), self.population)
        self.registry = Registry(self.elite)
        self.runEvolutive()

    def crossover(self):

        """
        Operador de cruce.
        Recorre la población alternando entre individuos dos a dos [ind1, ind2, ind1, ind2, ind1, ind2, ...].
        Cruce siempre entre ind1 y ind2. Sujeto a probabilidad self.args.crossover_rate.
            @arg    (No directo) self.args.crossover_rate  => Probabilidad de aplicar el operador de cruce.
            @return (No directo) Cambio de estado de clase => Recambio de la población.
        """

        auxPopulation = [] #  Pobalción auxiliar para proteger self.popuplation de modificaciones.

        for ind1, ind2 in zip(self.population[::2], self.population[1::2]): #  Cambio de lista [a, b, c, d] ==> [(a, b), (c, d)].
            if self.args.crossover_rate >= random.random():
                crossoverPoint = random.randint(0, len(ind1) - 1) if len(ind1) <= len(ind2) else random.randint(0, len(ind2) - 1) #  Selección de punto de cruce.

                auxPopulation.append(Individual(self.items, self.args, pattern = set(list(ind1.individual)[:crossoverPoint] + list(ind2.individual)[crossoverPoint:])))
                auxPopulation.append(Individual(self.items, self.args, pattern = set(list(ind2.individual)[:crossoverPoint] + list(ind1.individual)[crossoverPoint:])))

        self.population = auxPopulation #  Recambio de la población.


    def tournament(self):

        #!WARNING este método no funciona como debe.
        #!REVISAR.
        """
        Operador de torneo
        Ejecuta el operador tantas veces como individuos hay en la población. Selecciona n individuos al azar, los compara y guarda el mejor de los tres.
        Al final recambia la población por completo. Pueden existir individuos repetidos.
            TODO @arg (No directo)
            @return (No directo) Cambio de estado de clase => Recambio de la población.
        """

        auxPopulation = [] # Para copiar sin apuntar al mismo sitio en memoria
        for _ in range(len(self.population)):
            best = random.choice(self.population)
            for _ in range(self.args.tournament_size - 1):
                ind = random.choice(self.population)
                if ind > best:
                    best = ind

            auxPopulation.append(best)
        self.population = auxPopulation

    def runGeneration(self):

        """
        Ejecución de una generación.
        Llamada al torneo -> cruce -> mutación.
        Actualización de la élite.
        """

        self.tournament()
        self.crossover()
        for individual in self.population:
            individual.mutation()
        self.elite.update(self.population)
        self.registry.updateRegistry(self.generation) # He tocado generation y la he puesto como self.generation para pasarla por aqui

    def runEvolutive(self):

        """
        Ejecución del algoritmo evolutivo.
        Llamada a la ejecución de generaciones n veces.
            TODO: Implementación de número de ejecuciones dinámicas.
            TODO: Implementación de controles de las generaciones.
            TODO: Implementación del reseteo de la población.
        """

        print(f"Running Emerging Pattern for {self.args.input_file}")
        print("\n".join([f"\tOption: {option}... {self.args.__dict__[option]}" for option in self.args.__dict__]))

        if self.args.generation_number == None:
            print("Running non finite state")

            self.generation = 0 # Antes empezaba en 1 pero lo he puesto en 0
            while True:
                print(f"Generation {self.generation}")
                self.runGeneration()
                if self.generation == 100:
                    break
                self.generation += 1
