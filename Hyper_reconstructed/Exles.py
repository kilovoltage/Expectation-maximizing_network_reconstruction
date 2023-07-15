import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import math 
import random
import numba
from numba import jit
import copy

G=nx.les_miserables_graph()
colors = ["blue","gold","cyan","seagreen","darkviolet","green","orange","dodgerblue","turquoise"]
n=len(G.nodes)
cc=random.choices(colors,k=n)
plt.figure(figsize=(16,9))
nx.draw_networkx(G,pos=nx.kamada_kawai_layout(G),node_color=cc,edge_color='grey',node_size=[10*G.degree[i] for i in G.nodes],with_labels=True)
plt.axis('off')
plt.savefig('graph_les.svg',format='svg')
plt.show()
plt.close()
print(n)

test=[G.degree[i] for i in range(len(G.nodes))]
print(np.sqrt(np.var(test)))

#for i in set(G.nodes):
#    if G.degree[i]<2:
#        G.remove_nodes_from([i])
#nx.draw_networkx(G,pos=nx.kamada_kawai_layout(G),node_color=random.choices(colors,k=n),edge_color='grey',node_size=[10*G.degree[i] for i in G.nodes],with_labels=True)
#plt.show()
#n=len(G.nodes)
#print(n)

name=list(G.nodes)
bind=list(G.edges)
G1=nx.Graph()
for i in range(n):
    for j in range(n):
            if ((name[i],name[j]) in bind)|((name[j],name[i]) in bind):
                G1.add_edges_from([[i,j]])
G=G1

M=50000
alpha=1.8
omega=0.8
rho0=0.3
mu=1
p3e=0.6

miancharacter=['Valjean','Myriel','Thenardier', 'Cosette', 'Javert','Fantine','Marius','Gavroche','Grantaire','Enjolras','Eponine']
array0=[0 for i in range(n)]
for i in range(n):
    if name[i] in miancharacter:
        array0[i]=1
    else:
        array0[i]=np.random.binomial(1,rho0)

import analyzeG
anre=analyzeG.analyze(G,n,alpha,omega,p3e)
beta1=anre[0]
beta2=anre[1]
twobody=anre[2]
threebody=anre[3]
k1=anre[4]
k2=anre[5]
print(k1,k2)

import getMatrix
PSI=getMatrix.getfix0PSI(M,n,G,threebody,beta1,beta2,mu,array0,t=0)
plt.imshow(PSI[0:60,:])
plt.show()

import reconstruct_index
import analyzeG
anre=analyzeG.analyze(G,n,alpha,omega,p3e)
beta1=anre[0]
beta2=anre[1]
twobody=anre[2]
threebody=anre[3]

Pt=getMatrix.getPt(PSI,n,M)

import index
S1=index.index_step1(M,n,PSI,Pt,times=0,TM=200)
P1=S1[0]
eps=S1[1]
rhoe=S1[2]
rho1=S1[3]

import generator
from generator import generateG
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

bind2=list(G_hat2.edges)
G12=nx.Graph()
G12.add_nodes_from(name)
for i in range(n):
    for j in range(n):
            if ((i,j) in bind2)|((j,i) in bind2):
                G12.add_edges_from([[name[i],name[j]]])

plt.figure(figsize=(16,9))
nx.draw_networkx(G12,pos=nx.kamada_kawai_layout(nx.les_miserables_graph()),node_color=cc,edge_color='grey',node_size=[10*G.degree[i] for i in range(n)])
plt.axis('off')
plt.savefig('regenerate_les.svg',format='svg')
plt.show()
plt.close()

M=10000

F=reconstruct_index.construct(PSI,M,n,alpha,omega,threebody,p3e,G)
F11=F[0]
F12=F[1]

print(F11,F12)