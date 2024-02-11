import numpy as np
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import scipy
import math
import numpy.random as rd

def TwoClaim(N):
    p=0.3
    G= np.random.binomial(1,p,N)
    X=[]
    for i in range (0,len(G)):
        if G[i]==0:
            X.append(1)
        else:
            X.append(5)
    return X

def claim(a,N):
    # N is the number of claims
    # a = 0 : Log normal
    # a = 1 : Bernouilli
    # a = 2 : Weibull
    # a = 3 : Pareto
    # a = 4 : 1 (so that we just study the Poisson process)
    # a = 5 : Gaussian (in order to test the case of a continuous cdf)
    if a==0:
        return np.random.lognormal(0,1,N)
    elif a==1:
        return TwoClaim(N)
    elif a==2:
        return np.random.weibull(0.3,N)
    elif a==3: 
        return np.random.pareto(10,N) + 1.0
    elif a==5:
        return np.random.normal(0,1,N)
    else:
        return np.ones(N)

def Jump_Times_Poisson(lam,Te):
    tau=[]
    tau.append(0.0)
    e=rd.exponential(1/lam,1)
    i=1
    while e<=Te:
        tau.append(float(e))
        i+=1
        e=e+rd.exponential(1/lam,1)
    return tau

def N(t,Te,J):
    K=[]
    n=len(J)
    for j in range(0,n):
        K.append(J[j])
    if t==Te:
        return n-1
    K.append(Te)
    for i in range(0,n):
        if t >=K[i] and t <K[i+1]:
            return i
    
def C(t,Te,J,Cl):
    from func import N
    K=[]
    D=[]
    n=len(J)
    
    for j in range(0,n):
        K.append(J[j])
        D.append(Cl[j])
    
    n=N(t,Te,K)
    r=0
    for i in range(0,n+1):
        r=r+D[i]
    return r

def Rprocess(u,p,a,Te,lam):

    #Discretization grid without the jump times
    Np=100 # Number of time discretization
    tk=[]
    for i in range(0,Np+1):
        tk.append(i*Te/Np)
    
    J=Jump_Times_Poisson(lam,Te) # We generate the jump times of the Poisson process
    
    temp=claim(a,len(J))
    Cl=[0]
    for k in range(0,len(J)):
        Cl.append(temp[k])
    
    for t in J:
        if t!=0:
            tk.append(t)
    
    tk.sort()
    
    pk=[]
    
    K=[]
    for t in J:
        K.append(t)
        
    L=[]
    for f in Cl:
        L.append(f)
    
    for t in tk:
        pk.append([t,u+p*t-C(t,Te,K,L)])
        
    return pk


def Ruin(u,p,a,Te,lam):
    pk=Rprocess(u,p,a,Te,lam)
    tk=[i[0] for i in pk] # We recover the times
    
    t=0 # Ruin time (if 0 then no ruin, else is the ruin time)
    
    for temp in pk:
        if temp[1]<0:
            t=temp[0]
            return t
    return t