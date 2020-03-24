import random
import argparse
import statistics as st

class Data:

    """
    Clase Data
    Recoge información del dataset para generar los individuos y calcular su soporte.
    Genera un diccionario de diccionarios de sets.
        * Atributos.
            @atr self.file  => Nombre del fichero que contiene el dataset.
            @atr self.items => Diccionario de diccionarios de sets.
            *    self.items[grupo][item] : set{índices de aparición}.

        * Métodos.
            @def self.__init__    => Inicializador. Hilo de ejecución principal.
            @def self.extractData => Extrae información línea a línea y la almacena en self.items

    """

    def __init__(self, file):
        self.file = file
        self.items = dict()

        with open(self.file, "r") as inFile:

            for index, line in enumerate(inFile):
                line = line.strip("\r").strip("\n").split(",")
                self.extractData(index, line)

    def extractData(self, index, instance):

        """
        Extracción de información línea a línea.
        Lee la línea y almacena la información en self.items
        @arg    (Directo)    index                     => Número de línea.
        @arg    (Directo)    instance                  => Línea completa, contiene información del grupo al que pertenece y del registro.
        @return (No directo) Cambio de estado de clase => Modificación de self.items.
        """
        group, instance = instance[-1], set(instance[:-1])

        if group not in self.items.keys():
            self.items[group] = dict()

        for item in instance:
            try:
                self.items[group][item].add(index)
            except KeyError:
                self.items[group][item] = {index}