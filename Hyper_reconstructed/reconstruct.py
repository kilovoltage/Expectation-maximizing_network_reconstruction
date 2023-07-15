import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

import generator
from generator import generateG

n=100
G=generateG(n)
nx.draw_networkx(G,pos=nx.kamada_kawai_layout(G),node_color='green',edge_color='grey',node_size=[10*G.degree[i] for i in range(n)])
plt.axis('off')
plt.savefig('origin_example.svg',format='svg')
plt.show()
plt.close()

M=20000
alpha=1.5
omega=1
rho0=0.3
mu=1
p3e=0.6

import analyzeG
anre=analyzeG.analyze(G,n,alpha,omega,p3e)
beta1=anre[0]
beta2=anre[1]
twobody=anre[2]
threebody=anre[3]

import getMatrix
PSI=getMatrix.getPSI(M,n,G,threebody,beta1,beta2,mu,rho0,t=0)
plt.imshow(PSI[30:60,:])
plt.savefig('Matrix_example.svg',format='svg')
plt.show()
plt.close()

Pt=getMatrix.getPt(PSI,n,M)

import index
S1=index.index_step1(M,n,PSI,Pt,times=0,TM=200)
P1=S1[0]
eps=S1[1]
rhoe=S1[2]
rho1=S1[3]

delta_hat=generator.threshold1(n,P1)
G_hat=generator.generateG_hat(n,P1,delta_hat)

import F1s
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
nx.draw_networkx(G_hat2,pos=nx.kamada_kawai_layout(G),edge_color='grey',node_size=[10*G.degree[i] for i in range(n)])
plt.axis('off')
plt.savefig('regenerate_example.svg',format='svg')
plt.show()
plt.close()

print(f'F11:{F11},F12:{F12}')