from game import play
from AI import Net
from bug import Bug
import numpy as np
import math
import random
import heapq
import copy
import pygame
import matplotlib.pyplot as plt
xDim=7
yDim=10
CROSS_RATE = .9
MUT_RATE = .05
GENERATIONS = 20
POP_SIZE = 10

def init_pop(size=POP_SIZE):
	pop = []
	for i in range(size):
		n = Net()
		pop.append(n)
	return pop

def breed(n1, n2):
	if random.random() < CROSS_RATE:
		gene1 = np.array(n1.encode())
		gene2 = np.array(n2.encode())
		child1 = [i * 0.5 for i in np.add(gene1, gene2)]
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

def select(pop,scores):
	rand1=random.randint(0, len(pop) - 1)
	rand2=random.randint(0, len(pop) - 1)
	score1=scores[rand1]
	score2=scores[rand2]
	first = pop[rand1]
	second = pop[rand2]
	if score1 > score2:
		return first
	return second

def get_new_pop(pop):
	new_pop = []
	scores=play(headless=False,nets=pop,verbose=False)
	#sort the population and scores
	pop = [x for _, x in sorted(zip(scores,pop), key=lambda pair: pair[0])]
	scores=[x for _, x in sorted(zip(scores,scores), key=lambda pair: pair[0])]
	new_pop.extend(pop[0:5])
	while len(new_pop) < len(pop):
		first = select(pop,scores)
		second = select(pop,scores)
		first, second = breed(first, second)
		new_pop.extend([first, second])
	return new_pop,np.mean(scores)


inlayer=2
hidlayer=3
outlayer=3
gene_size=inlayer*hidlayer+hidlayer*outlayer
# scores=[[0]*POP_SIZE]*GENERATIONS
# print(scores)

nets=[Net(),Net(),Net()]
# scores=play(headless=False,nets=nets,verbose=False)
avg_scores=[]
pop = init_pop()
print(pop)
for i in range(GENERATIONS):
	print('===========================')
	print('GENERATION ' + str(i))
	pop,avg = get_new_pop(pop)
	print('AVG Score: ' + str(avg))
	avg_scores.append(avg)

for p in pop:
	print(p)
# play(False, pop[0])
# print(pop[0])
with open("file.txt", 'w') as output:
    for p in pop:
        output.write(str(p) + '\n')
plt.plot(avg_scores)
print(avg_scores)
plt.show()
print(pop[0])
