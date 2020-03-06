from population import Population
from individual import Individual
import random
import argparse
import statistics as st

def division(a, b):
    try:
        return float(a / b)
    except ZeroDivisionError:
        return float("inf")

class Elite():
    """
    Elite Class

    This class contains the best individuals generated by the algorithm after g number of generations
    """
    def __init__(self, args, items):
        self.args = args
        self.elite = dict()

        for group in items:
            self.elite[group] = []

    def isBetter(self): # Para comprobar si un individuo es mejor que otro
        for group in self.elite:
            if self.elite[group]