# -*- coding: utf-8 -*-
import random
import numpy as np

from deap import base
from deap import creator
from deap import tools
from deap import algorithms

vet = [2, 8, 1, 6, 5, 10, 4, 3, 9, 7]

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)


toolbox = base.Toolbox()
toolbox.register("attr_int", random.sample, range(10), 10)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_int, n=10)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.population(10)


notas_recursos = [
        [8,	8,	6,	3,	9,	8],
        [10,1,	5,	10,	2,	9],
        [7,	3,	4,	1,	1,	6],
        [5,	4,	2,	3,	1,	7],
        [4,	5,	8,	1,	1,	7],
        [3,	7,	0,	1,	2,	5],
        [0,	1,	4,	1,	8,	1],
        [0,	9,	8,	8,	6,	2],
        [1,	1,	8,	6,	0,	9],
        [3,	1,	1,	1,	0,	2]]

#notas coluna:
'''
0 - Python
1 - C
2 - Java
3 - AA
4 - UiPath
5 - Banco de Dados
'''

projetos = [
        [1, 0,	10],
        [2,	3,	9],
        [1,	4,	8],
        [3,	1,	7],
        [3,	2,	6],
        [3,	5,	1],
        [2,	1,	2],
        [2,	3,	3],
        [3,	2,	4],
        [1,	4,	5]]


recurso_projeto = np.zeros((10,10))
for i in range(len(notas_recursos)):
    for j in range(len(projetos)):
        aux = projetos[j][1]
        recurso_projeto[i][j] = ((notas_recursos[i][aux]/projetos[j][2])*projetos[j][0])



# Função de Avaliação
def evalOneMin(individual):
    s = 0
    menor = 1000
    pos_res = 0
    for i in range(len(vet)):
        for j in range(len(projetos)):
            if( menor > recurso_projeto[j][i]):
                menor = recurso_projeto[j][i]
                pos_res = i
        
        if (individual[i] == pos_res):
            s = s+1
    
    return s,

ind1 = toolbox.individual()
ind1.fitness.values = evalOneMin(ind1)
print(ind1.fitness.valid)
print(ind1.fitness.valid)
print(ind1.fitness)
print(ind1)
toolbox.register("evaluate", evalOneMin)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, low=0, up=10, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    random.seed(64)

    pop = toolbox.population(n=300)
    CXPB, MUTPB = 0.5, 0.2
    
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    
    fits = [ind.fitness.values[0] for ind in pop]
    g = 0
    while g < 1000:
        g = g + 1
        # Select and clone the next generation individuals
        offspring = map(toolbox.clone, toolbox.select(pop, len(pop)))
        # Apply crossover and mutation on the offspring
        offspring = algorithms.varAnd(offspring, toolbox, CXPB, MUTPB)

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # The population is entirely replaced by the offspring
        pop[:] = offspring


        fits = [ind.fitness.values[0] for ind in pop]
            
        print(" - Melhor: %d" % min(fits))
        print(" - Pior  : %d" % max(fits))
        print(" - Média : %d" % (sum(fits) / 300))
        
        frase_ag = []
        best_ind = tools.selBest(pop, 1)[0]
        for i in range(len(vet)):
            frase_ag.append(best_ind[i])
                
        print("")
        print(" - Target: ", vet)
        print(" - AG    : ", frase_ag)
        print("")
"""
    while g < 1000 and min(fits) > 0:

        g = g + 1
        print("================")
        print("* GERAÇÃO: %i" % g)
        print("================")
        
        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))
         
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)

                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values
    
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        pop[:] = offspring
        
        fits = [ind.fitness.values[0] for ind in pop]
        
        print(" - Melhor: %d" % min(fits))
        print(" - Pior  : %d" % max(fits))
        print(" - Média : %d" % (sum(fits) / 300))
        
        frase_ag = []
        best_ind = tools.selBest(pop, 1)[0]
        for i in range(len(vet)):
            frase_ag += chr(best_ind[i])
            
        print("")
        print(" - Target: %d" % vet)
        print(" - AG    : %d" % frase_ag)
        print("")
"""

if __name__ == "__main__":
    main()