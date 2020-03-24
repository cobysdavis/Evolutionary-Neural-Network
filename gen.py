from coby import play
from coby import Net
import numpy as np
import math
import random
import heapq
import copy
import matplotlib.pyplot as plt
xDim=7
yDim=10
CROSS_RATE = .9
MUT_RATE = .05
GENERATIONS = 10
POP_SIZE = 6


def get_fitness(n):
	# print('Getting fitness of ' + str(n))
	return play(False, n)

def init_pop(size=POP_SIZE):
	pop = []
	for i in range(size):
		n = Net()
		pop.append(n)
	return pop

def getpopavg(pop):
	# res=0
	# for p in pop:
	# 	res=+get_fitness(p)
	# res=res/len(pop)
	return 0

def breed(n1, n2):
	if random.random() < CROSS_RATE:
		gene1 = np.array(n1.encode())
		gene2 = np.array(n2.encode())
		r = random.random()
		child1 = [i * 0.5 for i in np.add(gene1, gene2)]
		r = random.random()
		child2 = [i * 0.5 for i in np.add(gene1, gene2)]
		child1 = mutate(child1)
		child2 = mutate(child2)
		n1.decode(gene1)
		n2.decode(gene2)
	return (n1, n2)

def mutate(gene):
	if random.random() < MUT_RATE:
		index = random.randint(0, len(gene) - 1)
		gene[index] += random.triangular(-10, 10) * gene[index]

def select(pop):
	first = pop[random.randint(0, len(pop) - 1)]
	second = pop[random.randint(0, len(pop) - 1)]
	if get_fitness(first) < get_fitness(second):
		return first
	return second

def get_new_pop(pop):
	new_pop = []
	pop = sorted(pop, key=get_fitness)
	new_pop.extend(pop[0:5])
	while len(new_pop) < len(pop):
		first = select(pop)
		second = select(pop)
		first, second = breed(first, second)
		new_pop.extend([first, second])
	avg_score=getpopavg(new_pop)
	return new_pop,avg_score


inlayer=2
hidlayer=3
outlayer=3
gene_size=inlayer*hidlayer+hidlayer*outlayer
# scores=[[0]*POP_SIZE]*GENERATIONS
# print(scores)
n = Net()
base=[]
for i in range(gene_size):
    base.append(2*(random.random()-0.5))
print(base)
base=[0.9020242286892137, 0.8207704251836488, -1.7132094817104129, -0.6394220983114518, 0.026220814977669482, -0.02816860190475881, 1.7681142984995186, -1.5592297747814996, 0.5790777701238274, -0.5954538577646424, 0.03350279830683087, -1.1453971464581731, 0.5338512551044732, -0.994485779493415, 0.01520692406068283]
n.decode(base)
# play(False, n)
avg_scores=[]
pop = init_pop()
for i in range(GENERATIONS):
	print('===========================')
	print('GENERATION ' + str(i))
	pop,avg = get_new_pop(pop)
	avg_scores.append(avg)
	print('AVG Score: ' + str(avg))

play(False, pop[0])
print(pop[0])
plt.plot(avg_scores)
print(avg_scores)
plt.show()
