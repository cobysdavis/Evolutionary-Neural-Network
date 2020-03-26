from random import random,randint
from time import sleep
import math
import numpy as np
import random
import pygame
from bug import Bug
from AI import Net
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
gene_size=inlayer*hidlayer+hidlayer*outlayer

def calcInputs(grid,bug):
    x=bug.x
    y=bug.y
    min = np.min(grid[yDim-2])
    loc=np.where(grid[yDim-2]==min)[0][0]
    return [x,loc]

def updateGrid(grid):
    grid.pop()
    if np.sum(grid[0])==xDim:
        grid.insert(0,genRow(xDim))
    else:
        grid.insert(0,[1]*xDim)
    return grid

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

def getBugsDead(bugs):
    for b in bugs:
        if b.alive==True:
            return False
    return True

def getBugsScores(bugs):
    scores=[]
    for b in bugs:
        scores.append(b.score)
    return scores

def play(headless=False,nets=None,verbose=False):
    N=len(nets)
    H=xDim*(WIDTH+MARGIN)
    W=yDim*(HEIGHT+MARGIN)
    WINDOW_SIZE = [H,W]
    framerate=30
    invSpeed=20
    done = False
    frame=0
    counter=1
    time=0
    start=True
    pygame.init()
    bugs=[]
    if not headless:
        screen = pygame.display.set_mode(WINDOW_SIZE)
        clock = pygame.time.Clock()
    grid=genBoard(xDim,yDim)
    for i in range(N):
        bugs.append(Bug(xDim,yDim))
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        inputs=[]
        for b in bugs:
            inputs.append(calcInputs(grid,b))
        actions=[]
        if nets:
            for b,n in zip(bugs,nets):
                if b.alive:
                    nnAction=n.forward(inputs[i])
                    maximum = np.max(nnAction)
                    action = np.where(nnAction == maximum)[0][0]
                    # print(action)
                    if action==0:
                        b.left(grid)
                        actions.append("left")
                    elif action==2:
                        b.right(grid)
                        actions.append("right")
                    else:
                        actions.append("nothing")
        if verbose:
            print(actions)

        if not headless:
            screen.fill(BLACK)
        for row in range(yDim):
            for column in range(xDim):
                color = BLACK
                if grid[row][column] == 1:
                    color = GREEN
                if not headless:
                    pygame.draw.rect(screen,color,[(MARGIN + WIDTH) * column + MARGIN,(MARGIN + HEIGHT) * row + MARGIN,WIDTH,HEIGHT])

        if not headless:
            for b in bugs:
                if b.alive:
                    color=b.colour
                    pygame.draw.rect(screen,color,[(MARGIN + WIDTH) * b.x + MARGIN,(MARGIN + HEIGHT) * b.y + MARGIN,WIDTH,HEIGHT])
            pygame.display.flip()

        if frame%invSpeed==0:
            grid=updateGrid(grid)
            for b in bugs:
                if b.alive:
                    b.score += 1

        for b in bugs:
            if b.score>=300:
                scores=getBugsScores(bugs)
                pygame.quit()
                return scores
            if b.alive:
                b.alive=b.checkCollide(grid)

        frame+=1

        allDead=getBugsDead(bugs)
        if allDead:
            scores=getBugsScores(bugs)
            pygame.quit()
            return scores
