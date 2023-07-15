import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import generator
from generator import generateG

n=100
G=generateG(n)
nx.draw_networkx(G,node_color='green',edge_color='grey',node_size=[10*G.degree[i] for i in range(n)])
plt.show()

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

plt.ylim((0,1))
plt.plot(rholist, listF1, marker='*', mec='r', mfc='w',label=u'two-body')
plt.plot(rholist, listF12, marker='o', ms=10,label=u'three-body')
plt.legend()  # 让图例生效
plt.xlabel(f"{chr(961)}") #X轴标签
plt.ylabel("F1") #Y轴标签
plt.show()
