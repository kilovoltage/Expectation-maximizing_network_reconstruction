import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import generator
from generator import generateG
import analyzeG
import getMatrix
import reconstruct_index
import gc

c=[10,12,14]
color=['blue','gold','green']
listM=[1000,2000,3000,4000,5000,6000,7000,8000,9000,10000]
listF11=np.zeros([3,len(listM)])
listF12=np.zeros([3,len(listM)])


for ii in range(3):
    n=100
    k1=c[ii]
    z = [k1 for i in range(n)]
    G = nx.expected_degree_graph(z)
    
    anak=analyzeG.analyzek(G,n)
    k1=anak[0]
    k2=anak[1]
    print(k1,k2)
    
    M=20000
    alpha=1.5
    omega=1
    rho0=0.3
    mu=1
    p3e=4/k2

    anre=analyzeG.analyze(G,n,alpha,omega,p3e)
    beta1=anre[0]
    beta2=anre[1]
    twobody=anre[2]
    threebody=anre[3]

    PSI=getMatrix.getPSI(M,n,G,threebody,beta1,beta2,mu,rho0,t=0)

    for jj in range(len(listM)):
        M=listM[jj]
        F=reconstruct_index.construct(PSI,M,n,alpha,omega,threebody,p3e,G)
        F11=F[0]
        F12=F[1]
        listF11[ii,jj]=F11
        listF12[ii,jj]=F12
    print(listF11,listF12)
    
plt.ylim((0,1))
for ii in range(3):
    plt.plot(listM, listF11[ii], marker='*',c=color[ii], ms=10,mec='r', mfc='w',label=f'k1={c[ii]},two-body')
    plt.plot(listM, listF12[ii], marker='o',c=color[ii],ms=10,label=u'k2=4,three-body')
plt.legend()  # 让图例生效
plt.xlabel(u"times") #X轴标签
plt.ylabel("F1") #Y轴标签
plt.savefig('main_k1.svg',format='svg')
plt.show()
plt.close()
            
