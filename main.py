# -*- coding: utf-8 -*-
import random
import numpy as np

from deap import base
from deap import creator
from deap import tools
from deap import algorithms

vet = [1, 7, 0, 5, 4, 9, 3, 2, 8, 6]


random.seed(0)
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

def random_no_repeat1(numbers, count):
    number_list = list(numbers)
    random.shuffle(number_list)
    return number_list[:count]


toolbox = base.Toolbox()
toolbox.register("attr_int", random_no_repeat1, range(10), 10)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_int)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
print(toolbox.individual())
toolbox.population(100)


notas_recursos = [
        [8,	8,	6,	3,	9,	8],
        [10,1,	5,	10,	2,	9],
        [7,	3,	4,	1,	1,	6],
        [5,	4,	2,	3,	1,	7],
        [4,	5,	8,	1,	1,	7],
        [3,	7,	1,	1,	2,	5],
        [1,	1,	4,	1,	8,	1],
        [1,	9,	8,	8,	6,	2],
        [1,	1,	8,	6,	1,	9],
        [3,	1,	1,	1,	1,	2]]

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
        [0,	10, 1],
        [3,	9, 2],
        [4,	8, 1],
        [1,	7, 3],
        [2,	6, 3],
        [5,	1, 3],
        [1,	2, 2],
        [3,	3, 2],
        [2,	4, 3],
        [4,	5, 1]]


# Função de Avaliação
def evalOneMin(individual):
    s = 0
    for i in range(len(individual)-1):
        ind = individual[i]
        tec_proj = projetos[i][0]
        s += (notas_recursos[ind][tec_proj]/projetos[i][1])*projetos[i][2]
        
    return s,


toolbox.register("evaluate", evalOneMin)
toolbox.register("mate", tools.cxPartialyMatched)
toolbox.register("mutate", tools.mutUniformInt, low=0, up=9, indpb=0.01)
toolbox.register("select", tools.selTournament, tournsize=3)

def print_ind(individual):
    print('Individuo:' + str(individual))

#Plotar Gráfico
def plot_log(logbook):
    gen = logbook.select("gen")
    min = logbook.select("min")
    avg = logbook.select("avg")
    max = logbook.select("max")

    import matplotlib.pyplot as plt

    fig, ax1 = plt.subplots()
    line1 = ax1.plot(gen, min, "b-", label="Minimum Fitness")
    ax1.set_xlabel("Generation")
    ax1.set_ylabel("Fitness", color="b")
    for tl in ax1.get_yticklabels():
        tl.set_color("b")

    ax2 = ax1.twinx()
    line2 = ax2.plot(gen, avg, "g-", label="Average Fitness")
    for tl in ax2.get_yticklabels():
        tl.set_color("g")

    ax3 = ax1.twinx()
    line3 = ax3.plot(gen, max, "y-", label="Maximum Fitness")
    ax3.set_ylabel("Size")
    for tl in ax3.get_yticklabels():
        tl.set_color("y")

    lns = line1 + line2 + line3
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc="center right")

    plt.show()



def main():
    random.seed(64)

    pop = toolbox.population(n=100)
    CXPB, MUTPB, NGEN = 0.5, 0.2, 300

    #stats a serem guardados
    stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("avg", np.mean)
    stats.register("max", np.max)
    

    pop, logbook = algorithms.eaSimple(pop, toolbox, CXPB, MUTPB, NGEN, stats=stats)
    
    #Seleciona o melhor individuo da populacao resultante
    best_ind = tools.selSPEA2(pop, 1)

    #Imprime as infromações do melhor individuo
    print_ind(best_ind[0])

    #Plota o Gráfico
    plot_log(logbook)
if __name__ == "__main__":
    main()