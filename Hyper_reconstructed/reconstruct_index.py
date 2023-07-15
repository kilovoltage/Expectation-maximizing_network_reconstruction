import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import generator
from generator import generateG
import analyzeG
import getMatrix
import index
import F1s

def construct(PSI,M,n,alpha,omega,threebody,p3e,G):

    PSI=PSI[0:M,:]
    Pt=getMatrix.getPt(PSI,n,M)

    S1=index.index_step1(M,n,PSI,Pt,times=0,TM=200)
    P1=S1[0]
    eps=S1[1]
    rhoe=S1[2]
    rho1=S1[3]

    delta_hat=generator.threshold1(n,P1)
    G_hat=generator.generateG_hat(n,P1,delta_hat)

    F11=F1s.F1(G,G_hat,n,TP1=0,TN1=0,FP1=0,FN1=0)

    anre1=analyzeG.analyze(G_hat,n,alpha,omega,p3e)
    twobody_hat=np.array(anre1[2])
    threebody_hat=np.array(anre1[3])
    Pt1=getMatrix.getPt1(PSI,twobody_hat,n,M)

    PSI2=getMatrix.getPSI2(PSI,twobody_hat,M)
    S2=index.index_step2(M,n,PSI,PSI2,rhoe,rho1,P1,eps,Pt,Pt1,twobody_hat,times=0,TM=200)
    P1=S2[0]
    P2=S2[1]
    eps=S2[2]
    rhoe=S2[3]
    rho1=S2[4]
    rho2=S2[5]

    delta_hat1=generator.threshold1(n,P1)
    delta_hat2=generator.threshold2(n,P2,twobody_hat)

    G_hat2i=generator.generateG_hat2(n,P1,P2,twobody_hat,threebody_hat,delta_hat1,delta_hat2)
    G_hat2=G_hat2i[0]
    threebody_hat2=G_hat2i[1]
    F12=F1s.F1(G,G_hat2,n,TP1=0,TN1=0,FP1=0,FN1=0)

    print(f'M:{M},F11:{F11},F12:{F12}')
    return F11,F12