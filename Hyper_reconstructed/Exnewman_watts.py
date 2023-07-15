import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import math 
import random
import numba
from numba import jit
import copy

G=nx.newman_watts_strogatz_graph(100, 12, 0.1, seed=None)

colors = ["blue","gold","cyan","seagreen","darkviolet","green","orange","dodgerblue","turquoise"]
n=len(G.nodes)
nx.draw_networkx(G,node_color=random.choices(colors,k=n),edge_color='grey',node_size=[10*G.degree[i] for i in G.nodes],with_labels = True)
plt.axis('off')
plt.savefig('newman_watts_graph.svg',format='svg')
plt.show()
plt.close()

M=20000
alpha=1.5
omega=1
rho0=0.1
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
plt.imshow(PSI[0:60,:])
plt.show()

import reconstruct_index

listM=[1000,2000,3000,4000,5000,6000,7000,8000,9000,10000,11000]
#listM=[1000,3000,5000,7000,9000,11000,13000,15000,17000,19000,20000]
listF1=[]
listF12=[]

for M in listM:
    F=reconstruct_index.construct(PSI,M,n,alpha,omega,threebody,p3e,G)
    F11=F[0]
    F12=F[1]
    listF1.append(F11)
    listF12.append(F12)
    
plt.ylim((0,1.1))
plt.plot(listM, listF1, marker='*', mec='r', mfc='w',label=u'two-body')
plt.plot(listM, listF12, marker='o', ms=10,label=u'three-body')
plt.legend()  # 让图例生效
plt.xlabel(u"times") #X轴标签
plt.ylabel("F1") #Y轴标签
plt.savefig('newman_watts_times.svg',format='svg')
plt.show()
plt.close()

M=10000
alpha=1.5
omega=1
rho0=0.3
mu=1
p3e=0.6
rholist=[0.01,0.03,0.05,0.07,0.09,0.11,0.13,0.15,0.17,0.19]

listF1=[]
listF12=[]

import getMatrix
import reconstruct_rho
for rho in rholist:
    F=reconstruct_rho.constructrho(M,n,alpha,omega,rho0,mu,p3e,G,rho)
    F11=F[0]
    F12=F[1]
    listF1.append(F11)
    listF12.append(F12)

plt.ylim((0,1.1))
plt.plot(rholist, listF1, marker='*', mec='r', mfc='w',label=u'two-body')
plt.plot(rholist, listF12, marker='o', ms=10,label=u'three-body')
plt.legend()  # 让图例生效
plt.xlabel(f"{chr(961)}") #X轴标签
plt.ylabel("F1") #Y轴标签
plt.savefig('newman_watts_rho.svg',format='svg')
plt.show()
plt.close()