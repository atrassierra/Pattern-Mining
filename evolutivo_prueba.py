from deap import base, creator, tools, algorithms
import sys
import random
import pandas as pd
import numpy as np
import array
import csv


def abrir_fichero(fichero): # Devuelve un conjunto de frozensets 
    with open(fichero, 'r') as inp: # transacciones del dataset
        tracts = [frozenset(line.split(",")) for line in inp]

    return tracts

def crear_diccionario(tracts): # Crea dict a partir de transacciones
    dic = {}
    contador = 1
    for i in range(0, len(tracts)):
        for j in tracts[i]:
            if j not in dic:
                dic.update({j: contador})
                contador += 1
    return dic

def transformar_dataset_set(tracts, dic):
    lista = []
    for i in range(0, len(tracts)):
        listita = []
        for j in tracts[i]:
            listita.append(dic[j])
        lista.append(listita)
    sets = [frozenset(tract) for tract in lista]
    return sets

def transformar_dataset_array(tracts, dic):
    lista = []
    for i in range(0, len(tracts)):
        for j in tracts[i]:
            lista.append(dic[j])
    return lista


def seleccion():
    global dataset
    global IND_SIZE
    bucle = True
    cojo = random.randint(1, IND_SIZE)
    while bucle:
        individuo = set(random.choices(dataset, k = cojo))
        if len(individuo) == cojo:
            bucle = False
    return individuo

def evaluacion(individuo):
    first_support = 0
    second_support = 0
    global frozen_dataset
    set_individuo = set(individuo)
    for i in range(0, len(frozen_dataset)):
        if set_individuo.issubset(frozen_dataset[i]) and i <= 660:
            first_support += 1
        elif set_individuo.issubset(frozen_dataset[i]) and i > 660:
            second_support += 1
    if first_support != 0 and second_support == 0:
        growth_rate = float("inf")
    elif first_support == 0 and second_support == 0:
        growth_rate = 0
    else:
        growth_rate = first_support/second_support
    return growth_rate, first_support


def mutacion(individuo): 
    bucle = True 
    global dataset # que coja cualquier valor posible
    while bucle:
        sup_genes = soporte_genes(individuo)
        for i in range(0, len(individuo)):
            try:
                if (1/sup_genes[i])*100 >= random.randint(0, 100):
                    nuevo_alelo = random.choice(dataset)
                    individuo[i] = nuevo_alelo
            except ZeroDivisionError:
                    nuevo_alelo = random.choice(dataset)
                    individuo[i] = nuevo_alelo
        if len(set(individuo)) == len(individuo):
            bucle = False
    return individuo

def soporte_genes(individuo):
    global frozen_dataset
    sup_genes = []
    for gen in individuo:
        gen_set = set([gen])
        soporte_gen = 0
        for i in range(0, len(frozen_dataset)):
            if gen_set.issubset(frozen_dataset[i]) and i <= 660:
                soporte_gen += 1
        sup_genes.append(soporte_gen)
    return sup_genes

def cruce(ind1, ind2): # Con mala suerte puede ser un bucle infinito
    bucle = True
    child1, child2 = [toolbox.clone(ind) for ind in (ind1, ind2)]
    while bucle:
        if len(ind1) < len(ind2):
            crossover_point = random.randint(0, len(child1) - 1)
        else:
            crossover_point = random.randint(0, len(child2) - 1)
        child1, child2 = child1[:crossover_point] + child2[crossover_point:], \
            child2[:crossover_point] + child1[crossover_point:]
        if len(set(child1)) == len(child1) and \
            len(set(child2)) == len(child2):
            bucle = False
    return child1, child2

def evolutivo(ngen, pop):
    hof = []
    p_cruce = 10
    p_mutacion = 10
    for g in range(ngen):
        offspring = toolbox.select(pop, k = len(pop)) # Siguiente generación
        offspring = map(toolbox.clone, offspring) # Clonamos
        offspring = list(offspring)

        # Aplicamos los cruces
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.randint(0, 10) <= p_cruce:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        # Apply mutation on the offspring
        for mutant in offspring:
            if random.randint(0, 10) <= p_mutacion:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)

        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # The population is entirely replaced by the offspring
        padres_hijos = pop + offspring
        padres_hijos_sort = sorted(padres_hijos, key = lambda x: x.fitness.values, reverse = True)
        rep_set = list()
        for individual_position in range(len(padres_hijos_sort)):
            if set(padres_hijos_sort[individual_position]) in rep_set:
                padres_hijos_sort[individual_position] = 0
            else:
                rep_set.append(set(padres_hijos_sort[individual_position]))

        new_pop = []
        for individual in padres_hijos_sort:
            if individual != 0:
                new_pop.append(individual)
        
        if len(hof) == 0:
            hof = new_pop[1:100]
        else:
            for i in new_pop:
                if i.fitness.values > hof[-1].fitness.values and i not in hof:
                    hof[-1] = i
                    hof = sorted(hof, key = lambda x: x.fitness.values, reverse = True)

        pop[:] = offspring
    return pop, hof

def salida(pop_sinduplicados, dictionary):        
    lista = []
    for i in pop_sinduplicados:
        lista.append((i, i.fitness.values))

    correspondencia = []  

    for i in pop_sinduplicados:
        pattern = []
        for j in i:
            for name_function, entero in dictionary.items():
                if entero == j:
                    pattern.append(name_function)
        correspondencia.append(pattern)
    
    for i in range(0, len(correspondencia)):
        correspondencia[i] = (correspondencia[i], lista[i][1])
    return correspondencia



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please, insert dataset")
    else:
        random.seed(1234)
        print("Ejecutando...")
        generaciones = 500
        poblacion_inicial = 100
        IND_SIZE = 10 # max longitud del patron

        tracts =  abrir_fichero("afr_amr_adipo.csv")
        dic = crear_diccionario(tracts)
        dataset = transformar_dataset_array(tracts, dic) # Global para funciones
        frozen_dataset = transformar_dataset_set(tracts, dic) # Global para funciones
        

        creator.create("FitnessMax", base.Fitness, weights = (1.0, 1.0))
        creator.create("Individual", array.array, typecode = "i", fitness=creator.FitnessMax)

        toolbox = base.Toolbox()
        toolbox.register("patron", seleccion)
        toolbox.register("individual", tools.initIterate, creator.Individual, \
            toolbox.patron)
        toolbox.register("poblacion", tools.initRepeat, list, toolbox.individual)

        # Tengo que hacer la funcion de evaluacion, cruce y mutacion
        toolbox.register("evaluate", evaluacion)
        toolbox.register("mutate", mutacion)
        toolbox.register("mate", cruce)
        toolbox.register("select", tools.selTournament, tournsize = 2)

        # Set the population size
        pop = toolbox.poblacion(n = poblacion_inicial)
        evo, hof = evolutivo(generaciones, pop)
        final = salida(evo, dic)
        with open("results.txt", 'w') as f:
            for p in final:
                f.write(str(p[0]))
                f.write(",")
                f.write(str(p[1]))
                f.write("\n")
            f.write("\n Hall of Fame \n")
            for i in hof:
                f.write(str(i))
                f.write("\n")
            f.close()
        print("Done!")