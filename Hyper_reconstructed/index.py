import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import math 
import random
import numba
from numba import jit
import copy

import getprob

def index_step1(M,n,PSI,Pt,times=0,TM=200):
    rhoe=np.zeros((M-1,n))
    rho1=np.zeros((M-1,n,n))
    P1=np.array([[0.1]*n for j in range(n)])
    eps=np.array([0.1]*n)

    Li=getprob.sort1(PSI,rhoe, rho1,P1, eps, M, n,Pt)

    P1=Li[0]
    eps=Li[1]
    rhoe=Li[2]
    rho1=Li[3]

    Pin1=np.array([[0.1]*n for j in range(n)])

    while((np.linalg.norm(P1-Pin1)/n>0.01)&(times<=TM)):
        Pin1=copy.deepcopy(P1)
        epsin1=copy.deepcopy(eps)

        Li=getprob.sort1(PSI, rhoe, rho1, P1, eps, M, n,Pt)
        
        P1=Li[0]
        eps=Li[1]
        rhoe=Li[2]
        rho1=Li[3]

        times=times+1
    
    return P1,eps,rhoe,rho1

def index_step2(M,n,PSI,PSI2,rhoe,rho1,P1,eps,Pt,Pt1,twobody_hat,times=0,TM=200):
    rho2=np.zeros((M-1,n,len(twobody_hat)))
    P2=np.array([[0.1]*n for j in range(len(twobody_hat))])

    Li=getprob.sort2(PSI,PSI2, rhoe, rho1, rho2, P1, P2, eps, M, n, Pt, Pt1)

    P1=Li[0]
    P2=Li[1]
    eps=Li[2]
    rhoe=Li[3]
    rho1=Li[4]
    rho2=Li[5]

    Pin1=P1
    Pin2=np.array([[0.1]*n for j in range(len(twobody_hat))])

    while(((np.linalg.norm(P1-Pin1)+np.linalg.norm(P2-Pin2))/n>0.01)&(times<=TM)):
        Pin1=copy.deepcopy(P1)
        Pin2=copy.deepcopy(P2)
        epsin1=copy.deepcopy(eps)

        Li=getprob.sort2(PSI,PSI2, rhoe, rho1, rho2, P1, P2, eps, M, n, Pt, Pt1)
        
        P1=Li[0]
        P2=Li[1]
        eps=Li[2]
        rhoe=Li[3]
        rho1=Li[4]
        rho2=Li[5]

        times=times+1
    
    return P1, P2, eps, rhoe, rho1, rho2