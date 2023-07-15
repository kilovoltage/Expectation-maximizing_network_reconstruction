import numpy as np
import networkx as nx

def analyze(G,n,alpha,omega,p3e):
    k1=sum([G.degree[i] for i in range(n)])/n

    clique=list(nx.enumerate_all_cliques(G))
    #n=G.number_of_nodes()
    N=len(clique)
    twobody=[]
    threebody=[]
    for i in range(N):
        if len(clique[i])==2:
            twobody.append(clique[i])
        elif len(clique[i])==3:
            threebody.append(clique[i])

    for [i,j,k] in threebody:
        index=np.random.uniform(0,1)
        if index<p3e:
            threebody.remove([i,j,k])
    
    d2=[0 for i in range(n)]
    for i in range(n):
        for j in range(len(threebody)):
            if i in threebody[j]:
                d2[i]=d2[i]+1
    k2=np.mean(d2)

    beta1=alpha/k1
    beta2=omega/k2
    
    return beta1,beta2,twobody,threebody,k1,k2

def analyzek(G,n):
    k1=sum([G.degree[i] for i in range(n)])/n

    clique=list(nx.enumerate_all_cliques(G))
    #n=G.number_of_nodes()
    N=len(clique)
    twobody=[]
    threebody=[]
    for i in range(N):
        if len(clique[i])==2:
            twobody.append(clique[i])
        elif len(clique[i])==3:
            threebody.append(clique[i])

    d2=[0 for i in range(n)]
    for i in range(n):
        for j in range(len(threebody)):
            if i in threebody[j]:
                d2[i]=d2[i]+1
    k2=np.mean(d2)
    
    return k1,k2