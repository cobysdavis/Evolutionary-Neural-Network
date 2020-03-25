from random import random,randint
from time import sleep
import math
import numpy as np
import random
import pygame
inlayer=2
hidlayer=3
outlayer=3
# random.seed(1000)
gene_size=inlayer*hidlayer+hidlayer*outlayer

class Net():
    def __init__(self, w1=None, w2=None):
        self.insize = inlayer
        self.hidsize = hidlayer
        self.outsize = outlayer
        self.w1 = w1
        self.w2 = w2
        if not w1:
            self.random()
    def forward(self, X):
        hout = self.sigmoid(np.dot(X, self.w1))
        fout = self.sigmoid(np.dot(hout, self.w2))
        return fout
    def random(self):
        base=[]
        for i in range(gene_size):
            base.append(2*(random.random()-0.5))
        self.decode(base)
    def encode(self):
        gene = []
        for i in self.w1:
            gene.extend(i)
        for i in self.w2:
            gene.extend(i)
        return gene
    def decode(self, gene):
        w1 = []
        count = 0
        for i in range(self.insize):
            n = []
            for j in range(self.hidsize):
                n.append(gene[count])
                count += 1
            w1.append(n)
        self.w1 = w1
        w2 = []
        for i in range(self.hidsize):
            n = []
            for j in range(self.outsize):
                n.append(gene[count])
                count += 1
            w2.append(n)
        self.w2 = w2

    def sigmoid(self, n):
        return 1/(1 + np.exp(-n))

    def linear(self, n):
        return n

    def __repr__(self):
        return str(self.encode())

    def __str__(self):
        return str(self.encode())
