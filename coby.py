from random import random,randint
from time import sleep
import math
import numpy as np
import random
import pygame
xDim=7
yDim=10
base=[]
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WIDTH = 20
HEIGHT = 20
MARGIN = 5
inlayer=2
hidlayer=3
outlayer=3
# random.seed(1000)

gene_size=inlayer*hidlayer+hidlayer*outlayer

base=[]
for i in range(gene_size):
    base.append(2*(random.random()-0.5))
print(base)

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
    def calcInputs(self,grid,bug):
        x=bug.x
        y=bug.y
        min = np.min(grid[yDim-2])
        loc=np.where(grid[yDim-2]==min)[0][0]
        return [x,loc]

    def sigmoid(self, n):
        return 1/(1 + np.exp(-n))

    def linear(self, n):
        return n

    def __repr__(self):
        return str(self.encode())

    def __str__(self):
        return str(self.encode())

def updateGrid(grid):
    grid.pop()
    if np.sum(grid[0])==xDim:
        grid.insert(0,genRow(xDim))
    else:
        grid.insert(0,[1]*xDim)
    return grid

class Bug():
    x = int((xDim-1)/2)
    y = yDim-1

    def __init__(self,xDim,yDim):
        self.x = int((xDim-1)/2)
        self.y=yDim-1

    def left(self,g):
        if self.x>0:
            if g[self.y][self.x-1]==1:
                self.x=self.x-1
    def right(self,g):
        if self.x<xDim-1:
            if g[self.y][self.x+1]==1:
                self.x=self.x+1
    def up(self,g):
        if self.y>0:
            if g[self.y-1][self.x]==1:
                self.y=self.y-1
    def down(self,g):
        if self.y<yDim-1:
            if g[self.y+1][self.x]==1:
                self.y=self.y+1

    def checkCollide(self,g):
        if g[self.y][self.x]==0:
            # print("Dead")
            return False
        return True

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

def printBoard(board):
    for row in board:
        print(row)


def reset(bug):
    alive=0
    start=0
    bug.x=int((xDim-1)/2)
    bug.y=yDim-1

def play(headless=False, ai=None):
    H=xDim*(WIDTH+MARGIN)
    W=yDim*(HEIGHT+MARGIN)
    WINDOW_SIZE = [H,W]
    framerate=30
    invSpeed=18
    done = False
    frame=0
    counter=1
    score=0
    time=0
    alive=True
    start=True
    pygame.init()
    if not headless:
        screen = pygame.display.set_mode(WINDOW_SIZE)
        clock = pygame.time.Clock()
    grid=genBoard(xDim,yDim)
    b=Bug(xDim,yDim)
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                grid[row][column] = 0
                print("Click ", pos, "Grid coordinates: ", row, column)
            elif event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE:
                    start=1
                if event.key == pygame.K_ESCAPE :
                    done = True
                elif event.key == pygame.K_LEFT :
                    b.left(grid)
                elif event.key == pygame.K_RIGHT :
                    b.right(grid)
                elif event.key == pygame.K_UP :
                    b.up(grid)
                elif event.key == pygame.K_DOWN :
                    b.down(grid)
        inputs=ai.calcInputs(grid,b)
        nnAction=ai.forward(inputs)
        # print(nnAction)
        maximum = np.max(nnAction)
        action = np.where(nnAction == maximum)[0][0]
        # print(action)
        if action==0:
            b.left(grid)
            # print("left")
        elif action==2:
            b.right(grid)
            # print("right")

        if not headless:
            screen.fill(BLACK)
        for row in range(yDim):
            for column in range(xDim):
                color = BLACK
                if grid[row][column] == 1:
                    color = GREEN
                if not headless:
                    pygame.draw.rect(screen,color,[(MARGIN + WIDTH) * column + MARGIN,(MARGIN + HEIGHT) * row + MARGIN,WIDTH,HEIGHT])
        color=RED
        if not headless:
            pygame.draw.rect(screen,color,[(MARGIN + WIDTH) * b.x + MARGIN,(MARGIN + HEIGHT) * b.y + MARGIN,WIDTH,HEIGHT])
            pygame.display.flip()

        if frame%invSpeed==0:
            grid=updateGrid(grid)
            score += 1
        alive=b.checkCollide(grid)
        frame+=1
        if not alive:
            pygame.quit()
            return score


nn=Net()
play(False,nn)
print(nn)
