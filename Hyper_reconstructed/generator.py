import networkx as nx 
import random

def rand_edge(G,vi,vj,p=0.1):
    prob=random.uniform(0,1)
    if (prob<p):
        G.add_edge(vi,vj)

def generateG(n):
    G=nx.Graph()
    H=nx.path_graph(n)
    G.add_nodes_from(H)

    i=0
    while(i<n):
        j=0
        while(j<i):
            rand_edge(G,i,j)
            j +=1
        i +=1
    
    return G

def threshold1(n,P1):
    delta_hat=[0 for i in range(n)]
    for i in range(n):
        Pl=[]
        for j in range(n):
            Pl.append(P1[j][i])
        Pl.sort(reverse=True)

        delta=[]
        for l in range(len(Pl)-1):
            if Pl[l+1]!=0:
                delta.append((Pl[l]-Pl[l+1])*Pl[l]/Pl[l+1])
        
        for l in range(len(delta)):
            if delta[l]==max(delta):
                delta_hat[i]=Pl[l+1]
    return delta_hat

def threshold2(n,P2,twobody_hat):
    delta_hat2=[0 for i in range(n)]
    for i in range(n):
        Pl=[]
        for j in range(len(twobody_hat)):
            Pl.append(P2[j][i])
        Pl.sort(reverse=True)

        delta2=[]
        for l in range(len(Pl)-1):
            if Pl[l+1]!=0:
                delta2.append((Pl[l]-Pl[l+1])*Pl[l]/Pl[l+1])
        
        for l in range(len(delta2)):
            if delta2[l]==max(delta2):
                delta_hat2[i]=Pl[l+1]
    return delta_hat2

def generateG_hat(n,P1,delta_hat):
    G_hat=nx.Graph()
    H=nx.path_graph(n)
    G_hat.add_nodes_from(H)

    for i in range(n):
        for j in range(i,n):
            if (P1[j][i]>delta_hat[i])&(P1[i][j]>delta_hat[j]):
                G_hat.add_edges_from([[i,j]])
    
    return G_hat

def generateG_hat2(n,P1,P2,twobody_hat,threebody_hat,delta_hat,delta_hat2):
    G_hat2=nx.Graph()
    H=nx.path_graph(n)
    G_hat2.add_nodes_from(H)

    for i in range(n):
        for j in range(i,n):
            if (P1[j][i]>delta_hat[i])&(P1[i][j]>delta_hat[j]):
                G_hat2.add_edges_from([[i,j]])
    threebody_hat2=[]
    for (i,j,k) in threebody_hat:
        for m in range(len(twobody_hat)):
            if set(twobody_hat[m])==set([i,j]):
                j1=m
            if set(twobody_hat[m])==set([k,j]):
                j2=m
            if set(twobody_hat[m])==set([i,k]):
                j3=m
        if (P2[j1][k]>delta_hat2[k])&(P2[j2][i]>delta_hat2[i])&(P2[j3][j]>delta_hat2[j]):
            G_hat2.add_edges_from([(i,j),(i,k),(j,k)])
            threebody_hat2.append((i,j,k))
    return G_hat2,threebody_hat2