import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import math 
import random
import numba
from numba import jit
import copy

def F1(G,G_hat,n,TP1=0,TN1=0,FP1=0,FN1=0):
    for i in range(n):
        for j in range (i,n):
            if (i,j) in set(G_hat.edges)&set(G.edges):
                TP1=TP1+1
            elif (i,j) in set(G_hat.edges):
                FP1=FP1+1
            elif (i,j) in set(G.edges):
                FN1=FN1+1
            else:
                TN1=TN1+1

    PS1=TP1/(TP1+FP1)
    RS1=TP1/(TP1+FN1)
    F11=2*PS1*RS1/(PS1+RS1)
    return F11

def F2(threebody,threebody_hat2,TP2=0,TN2=0,FP2=0,FN2=0):
    testthree=[tuple(threebody[i]) for i in range(len(threebody))]
    for (i,j,k) in set(threebody_hat2)|set(testthree):
        if (i,j,k) in set(threebody_hat2)&set(testthree):
            TP2=TP2+1
        elif (i,j,k) in set(threebody_hat2):
            FP2=FP2+1
        elif (i,j,k) in set(testthree):
            FN2=FN2+1
        else:
            TN2=TN2+1

    PS2=TP2/(TP2+FP2)
    RS2=TP2/(TP2+FN2)
    F12=2*PS2*RS2/(PS2+RS2)
    return F12