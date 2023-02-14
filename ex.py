import wgraph as wgf
import time
from random import random, randint
from itertools import product, combinations
import matplotlib.pyplot as plt
import numpy as np

def random_graph(n, p, directed=False):
    nodes = range(n)
    adj_mat = [[] for i in nodes]
    possible_edges = product(nodes, repeat=2) if directed else combinations(nodes, 2)
    for u, v in possible_edges:
        if len(adj_mat[u]) * len(adj_mat[v]) < 1 or random() < p:
            adj_mat[u].append( (v, randint(1,10)) )
            if not directed:
                adj_mat[v].append( (u, randint(1,10)) )
    return {vertex: adj_list for vertex, adj_list in enumerate(adj_mat)}

grafo = random_graph(4, 0.5)
print(grafo)

# grafo = {'A': [('B', 1), ('C', 2), ('D', 3)],
#          'B': [('A', 1), ('C', 4)],
#          'C': [('A', 2), ('B', 4), ('D', 5)],
#          'D': [('A', 3), ('C', 5)]}

# g = wgf.WeightedGraph(grafo)
# print(g)
# g.djikstra(0)
# g.drawGraph()

class Experiment:
    currentStep = 1
    timesPerStep = []
    avgTimesPerStep = []

    def __init__(self, prob, trials):
        self.prob = prob
        self.trials = trials
    
    def runStep(self):
        print("\n# STEP " + str(self.currentStep))
        times = []
        for x in range(self.trials):
            graphMat = random_graph(self.currentStep, 0.5)
            graph = wgf.WeightedGraph(graphMat)
            start = time.time()
            graph.djikstra(0)
            end = time.time()
            currentTime = (end - start) * 1000
            times.append(currentTime)
            print("\n# TRIAL " + str(x) + " took " + str(currentTime) + " ms")
        avgTime = sum(times) / len(times)
        self.timesPerStep.append(times)
        self.avgTimesPerStep.append(avgTime)

        print("\n\n# STEP TIMES:", times, "AVG: " + str(avgTime) + " ms")

    def runSteps(self, steps):
        while (self.currentStep <= steps):
            self.runStep()
            self.currentStep += 1

    def plot(self):
        fig, ax = plt.subplots(1, self.trials, sharey=True, sharex=True)

        times = list(zip(*self.timesPerStep))

        for step in range(self.trials):
            ax[step].bar([str(trial) for trial in range(self.trials)], times[step])

        fig.text(0.5, 0.04, 'Numero de Nodos', ha='center', va='center')
        fig.text(0.06, 0.5, 'Tiempo de Ejecucion (ms)', ha='center', va='center', rotation='vertical')

        fig.suptitle('Tiempos de Ejecucion de algoritmo de Djikstra')
        plt.show()

        plt.plot([str(trial + 1) for trial in range(0, self.trials, self.increment)], self.avgTimesPerStep, label="Ponderado Sin Dirigir")
        if (self.directed): plt.plot([str(trial + 1) for trial in range(0, self.trials, self.increment)], self.avgTimesPerStepDirected, label="Ponderado Dirigido")

        plt.xlabel("Numero de Nodos")
        plt.ylabel("Tiempo de Ejecucion Promedio (ms)")
        plt.legend()

ex = Experiment(0.5, 5)
ex.runSteps(5)
ex.plot()
