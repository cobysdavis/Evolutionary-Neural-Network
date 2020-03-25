from random import random,randint
from time import sleep
import math
import numpy as np
import random
import pygame

class Bug():
    def __init__(self,xDim,yDim):
        self.x = int((xDim-1)/2)
        self.y=yDim-1
        self.xDim=xDim
        self.yDim=yDim
        self.alive=True
        self.score=0
        self.colour=(randint(0,255),randint(0,255),randint(0,255))

    def left(self,g):
        if self.x>0:
            if g[self.y][self.x-1]==1:
                self.x=self.x-1
    def right(self,g):
        if self.x<self.xDim-1:
            if g[self.y][self.x+1]==1:
                self.x=self.x+1
    def up(self,g):
        if self.y>0:
            if g[self.y-1][self.x]==1:
                self.y=self.y-1
    def down(self,g):
        if self.y<self.yDim-1:
            if g[self.y+1][self.x]==1:
                self.y=self.y+1

    def checkCollide(self,g):
        if g[self.y][self.x]==0 or self.x<0 or self.x>=self.xDim:
            return False
        return True

    def __repr__(self):
        return str(self.encode())

    def __str__(self):
        return str(self.encode())
