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