import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import generator
from generator import generateG

n=100
G=generateG(n)
nx.draw_networkx(G,node_color='green',edge_color='grey',node_size=[10*G.degree[i] for i in range(n)])
plt.show()

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
plt.imshow(PSI[0:60,:])
plt.show()

import reconstruct_index

listM=[1000,2000,3000,4000,5000,6000,7000,8000,9000,10000,11000]
#listM=[1000,3000,5000,7000,9000,11000]
listF1=[]
listF12=[]

for M in listM:
    F=reconstruct_index.construct(PSI,M,n,alpha,omega,threebody,p3e,G)
    F11=F[0]
    F12=F[1]
    listF1.append(F11)
    listF12.append(F12)
    
plt.ylim((0,1))
plt.plot(listM, listF1, marker='*', mec='r', mfc='w',label=u'two-body')
plt.plot(listM, listF12, marker='o', ms=10,label=u'three-body')
plt.legend()  # 让图例生效
plt.xlabel(u"times") #X轴标签
plt.ylabel("F1") #Y轴标签
plt.show()
        