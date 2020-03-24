from random import random,randint
from time import sleep
import math
import numpy as np
import random
import pygame
base = []

print(base)
xDim=7
yDim=10
def genRow(x):
    empty=randint(0,x-1)
    row=[1]*x
    row[empty]=0
    return row

def genBoard(x,y):
    board=[]
    for i in range(int(y/2)):
        board.append(genRow(x))
        board.append([1]*x)
    board.append([1]*x)
    return board
class Net():
    def __init__(self, w1=None, w2=None):
        self.insize = 3
        self.hidsize = 3
        self.outsize = 1
        self.w1 = w1
        self.w2 = w2
        if not w1:
            self.random()

    def forward(self, X):
        hout = self.sigmoid(np.dot(X, self.w1))
        print("w1",self.w1)
        print("middle")
        print(hout.shape)
        print(hout)
        print("w2")
        print(self.w2)
        fout = self.sigmoid(np.dot(hout, self.w2))
        print("final")
        print(fout)
        return fout

    def random(self):
        gene = []
        for weight in base:
            gene.append(weight + random.triangular(weight - .3, weight + .3))
        self.decode(gene)

    def encode(self):
        gene = []
        for i in self.w1:
            gene.extend(i)
        for i in self.w2:
            gene.extend(i)

        return gene

    # set weights given gene
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


class Bug():
    x = xDim-1
    y = yDim-1
    def left(grid):
        if Bug.x>0:
            if grid[Bug.y][Bug.x-1]==1:
                Bug.x=Bug.x-1
    def right(grid):
        if Bug.x<xDim-1:
            if grid[Bug.y][Bug.x+1]==1:
                Bug.x=Bug.x+1
    def up(grid):
        if Bug.y>0:
            if grid[Bug.y-1][Bug.x]==1:
                Bug.y=Bug.y-1
    def down(grid):
        if Bug.y<yDim-1:
            if grid[Bug.y+1][Bug.x]==1:
                Bug.y=Bug.y+1

    def checkCollide(grid):
        if grid[Bug.y][Bug.x]==0:
            print("Dead")
            return False
        return True
b=Bug()
nn=Net()

grid=genBoard(xDim,yDim)
x=b.x
y=b.y
left,right,up=0,0,0
if x==0:
    left=1
elif grid[y][x-1]==0:
    left=1
if x==xDim-1:
    right=1
elif grid[y][x+1]==0:
    right=1
if grid[y-1][x]==0:
    up=1

nnAction=nn.forward([up,left,right])
if nnAction>1:
   Bug.left(grid)
   print("left")
elif nnAction< -1:
   Bug.right(grid)
   print("right")
