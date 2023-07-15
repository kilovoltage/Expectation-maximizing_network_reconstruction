import numpy as np
import random
from numba import jit

def getPSI(M,n,G,threebody,beta1,beta2,mu,pho0,t=0):
    psi=np.array([np.random.binomial(1,pho0) for i in range(0,n)])
    matrix=[]
    while t<M:
        matrix.append(psi)
        count1=[0 for i in range(n)]
        for i in range(n):
            ad1=set(G.adj[i])
            for j in ad1:
                if psi[j]==1:
                    count1[i]=count1[i]+1
        #计算被感染的节点数
        count2=[0 for i in range(n)]
        for [i1,j1,k1] in threebody:
            pact=random.uniform(0,1)
            for i in range(n):
                if (i in  [i1,j1,k1])&(pact<0.6):
                    c=set([i1,j1,k1])
                    c.remove(i)
                    c1=list(c)
                    if (psi[c1[0]]==1)&(psi[c1[1]]==1):
                        count2[i]=count2[i]+1

        p1=[]#因为相邻节点传播被感染的概率
        for i in range(n):
            if count1[i]==0:
                p1.append(0)#等价于，周围没有节点感染时，由于一阶社群传播被感染的概率为0
            else:
                p1.append(1-pow(1-beta1,count1[i]))
                #等价于，周围有节点感染时，由于一阶社群传播被感染的概率为1减去都不发生传播的概率

        p2=[]#因为相邻二阶社群都传播被感染的概率
        for i in range(n):
            if count2[i]==0:
                p2.append(0)
            else:
                p2.append(1-pow(1-beta2,count2[i]))

        p3=[1-(1-p1[i])*(1-p2[i]) for i in range(n)]
        #易感态变为感染态的概率，(1-p1[i])和(1-p2[i])分别表示不因一阶和二阶社群传播被感染的概率
        psi1=[0 for i in range(n)]
        for i in range(n):
            if psi[i]==1:
                psi1[i]=1-np.random.binomial(1,mu)
            else:
                psi1[i]=np.random.binomial(1,p3[i])

        psi=psi1
        t=t+1

    PSI=np.array(matrix)
    return PSI

def getfix0PSI(M,n,G,threebody,beta1,beta2,mu,array0,t=0):
    psi=array0
    matrix=[]
    while t<M:
        matrix.append(psi)
        count1=[0 for i in range(n)]
        for i in range(n):
            ad1=set(G.adj[i])
            for j in ad1:
                if psi[j]==1:
                    count1[i]=count1[i]+1
        #计算被感染的节点数
        count2=[0 for i in range(n)]
        for [i1,j1,k1] in threebody:
            pact=random.uniform(0,1)
            for i in range(n):
                if (i in  [i1,j1,k1])&(pact<0.6):
                    c=set([i1,j1,k1])
                    c.remove(i)
                    c1=list(c)
                    if (psi[c1[0]]==1)&(psi[c1[1]]==1):
                        count2[i]=count2[i]+1

        p1=[]#因为相邻节点传播被感染的概率
        for i in range(n):
            if count1[i]==0:
                p1.append(0)#等价于，周围没有节点感染时，由于一阶社群传播被感染的概率为0
            else:
                p1.append(1-pow(1-beta1,count1[i]))
                #等价于，周围有节点感染时，由于一阶社群传播被感染的概率为1减去都不发生传播的概率

        p2=[]#因为相邻二阶社群都传播被感染的概率
        for i in range(n):
            if count2[i]==0:
                p2.append(0)
            else:
                p2.append(1-pow(1-beta2,count2[i]))

        p3=[1-(1-p1[i])*(1-p2[i]) for i in range(n)]
        #易感态变为感染态的概率，(1-p1[i])和(1-p2[i])分别表示不因一阶和二阶社群传播被感染的概率
        psi1=[0 for i in range(n)]
        for i in range(n):
            if psi[i]==1:
                psi1[i]=1-np.random.binomial(1,mu)
            else:
                psi1[i]=np.random.binomial(1,p3[i])

        psi=psi1
        t=t+1

    PSI=np.array(matrix)
    return PSI

def getPSIwithrho(M,n,G,threebody,beta1,beta2,mu,pho0,rho,t=0):
    psi=np.array([np.random.binomial(1,pho0) for i in range(0,n)])
    matrix=[]
    while t<M:
        matrix.append(psi)
        count1=[0 for i in range(n)]
        for i in range(n):
            ad1=set(G.adj[i])
            for j in ad1:
                if psi[j]==1:
                    count1[i]=count1[i]+1
        #计算被感染的节点数
        count2=[0 for i in range(n)]
        for [i1,j1,k1] in threebody:
            pact=random.uniform(0,1)
            for i in range(n):
                if (i in  [i1,j1,k1])&(pact<0.6):
                    c=set([i1,j1,k1])
                    c.remove(i)
                    c1=list(c)
                    if (psi[c1[0]]==1)&(psi[c1[1]]==1):
                        count2[i]=count2[i]+1

        p1=[]#因为相邻节点传播被感染的概率
        for i in range(n):
            if count1[i]==0:
                p1.append(0)#等价于，周围没有节点感染时，由于一阶社群传播被感染的概率为0
            else:
                p1.append(1-pow(1-beta1,count1[i]))
                #等价于，周围有节点感染时，由于一阶社群传播被感染的概率为1减去都不发生传播的概率

        p2=[]#因为相邻二阶社群都传播被感染的概率
        for i in range(n):
            if count2[i]==0:
                p2.append(0)
            else:
                p2.append(1-pow(1-beta2,count2[i]))

        p3=[1-(1-p1[i])*(1-p2[i]) for i in range(n)]
        #易感态变为感染态的概率，(1-p1[i])和(1-p2[i])分别表示不因一阶和二阶社群传播被感染的概率
        psi1=[0 for i in range(n)]
        for i in range(n):
            if psi[i]==1:
                psi1[i]=1-np.random.binomial(1,mu)
            else:
                psi1[i]=np.random.binomial(1,p3[i])

        for i in range(n):
            rhoi=random.uniform(0,1)
            if rhoi<rho:
                psi1[i]=abs(psi1[i]-1)
        
        psi=psi1
        t=t+1
    
    PSI=np.array(matrix)
    return PSI

def getPSI2(PSI,twobody_hat,M):
    PSI2=[]
    for time in range(M):
        PSI2t=[]
        for j1s in range(len(twobody_hat)):
            PSI2t.append(PSI[time][twobody_hat[j1s][0]]*PSI[time][twobody_hat[j1s][1]])
        PSI2.append(PSI2t)
    PSI2=np.array(PSI2)
    return PSI2

@jit(nopython=True)
def getPt(PSI,n,M):
    Pt=np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            if j==i:
                Pt[i][j]=0
            else:
                m1=0
                m2=0
                for time in range(M-1):
                    if (PSI[time][j]==1)&(PSI[time][i]==0):
                        m1=m1+1
                        if (PSI[time+1][i]==1):
                            m2=m2+1
                if m1!=0:
                    Pt[i][j]=m2/m1  
                else:
                    Pt[i][j]=0
                #print([i,j],[m2,m1],Pt[i][j])
    return Pt

@jit(nopython=True)
def getPt1(PSI,twobody,n,M):
    Pt1=np.zeros((n,len(twobody)))
    for i in range(n):
        for j in range(len(twobody)):
            if i in set(twobody[j]):
                Pt1[i][j]=0
            else:
                m1=0
                m2=0
                for time in range(M-1):
                    if (PSI[time][twobody[j][0]]==1)&(PSI[time][twobody[j][1]]==1)&(PSI[time][i]==0):
                        m1=m1+1
                        if (PSI[time+1][i]==1):
                            m2=m2+1
                if m1!=0:
                    Pt1[i][j]=m2/m1  
                else:
                    Pt1[i][j]=0
                #print([i,j],[m2,m1],Pt1[i][j])
    return Pt1
