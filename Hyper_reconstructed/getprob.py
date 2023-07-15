import numpy as np
from numba import jit

@jit(nopython=True)
def sort1(PSI, rhoe, rho1, P1, eps, M, n,Pt):

    for time in range(M-1):
        S=np.sum(np.transpose(P1)*Pt*PSI[time,:],axis=1)
        rhoe[time,:]=eps/(eps+S)
        rho1[time,:,:]=np.transpose(P1)*Pt*PSI[time,:]/(eps+S).reshape(n,1)

    for i in range(n):
        PSItm=PSI[0:M-1,:]
        PSItmp1=PSI[1:M,:]
        S11=np.sum(rho1[0:M-1,i,:]*(PSItmp1[:,i]*(PSItm[:,i]==0)).reshape(M-1,1),axis=0)
        S12=np.sum(PSItm*Pt[i,:]*(PSItm[:,i]==0).reshape(M-1,1),axis=0)
        P1[:,i]=S11*(S12!=0)/(S12+0.01*(S12==0))
        
        S31=np.sum(rhoe[0:M-1,i]*(PSItmp1[:,i]*(PSItm[:,i]==0)))
        S32=np.sum((PSItm[:,i]==0))
        eps[i]=S31*(S32!=0)/(S32+0.01*(S32==0))  
    
    return P1, eps, rhoe, rho1

@jit(nopython=True)
def sort2(PSI, PSI2, rhoe, rho1, rho2, P1, P2, eps, M, n, Pt, Pt1):

    for time in range(M-1):
        S=np.sum(np.transpose(P1)*Pt*PSI[time,:],axis=1)+np.sum(np.transpose(P2)*Pt1*PSI2[time,:],axis=1)
        rhoe[time,:]=eps/(eps+S)
        rho1[time,:,:]=np.transpose(P1)*Pt*PSI[time,:]/(eps+S).reshape(n,1)
        rho2[time,:,:]=np.transpose(P2)*Pt1*PSI2[time,:]/(eps+S).reshape(n,1)

    for i in range(n):
        PSItm=PSI[0:M-1,:]
        PSItmp1=PSI[1:M,:]
        S11=np.sum(rho1[0:M-1,i,:]*(PSItmp1[:,i]*(PSItm[:,i]==0)).reshape(M-1,1),axis=0)
        S12=np.sum(PSItm*Pt[i,:]*(PSItm[:,i]==0).reshape(M-1,1),axis=0)
        P1[:,i]=S11*(S12!=0)/(S12+0.01*(S12==0))

        PSI2tm=PSI2[0:M-1,:]
        PSI2tmp1=PSI2[1:M,:]
        S21=np.sum(rho2[0:M-1,i,:]*(PSItmp1[:,i]*(PSItm[:,i]==0)).reshape(M-1,1),axis=0)
        S22=np.sum(PSI2tm*Pt1[i,:]*(PSItm[:,i]==0).reshape(M-1,1),axis=0)
        P2[:,i]=S21*(S22!=0)/(S22+0.01*(S22==0))
        
        S31=np.sum(rhoe[0:M-1,i]*(PSItmp1[:,i]*(PSItm[:,i]==0)))
        S32=np.sum((PSItm[:,i]==0))
        eps[i]=S31*(S32!=0)/(S32+0.01*(S32==0))  
    
    return P1, P2, eps, rhoe, rho1, rho2