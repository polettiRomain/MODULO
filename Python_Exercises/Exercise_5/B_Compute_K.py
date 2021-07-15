# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 01:08:07 2019

@author: mendez
"""
# For a Cartesian Domain, we use no Weight Matrix. 
# Therefore the correlation is computed simply via matrix multiplication.
# However in this case we work with partitions. We we proceed by blocks


#%% First load from the first partition the info about the case

import numpy as np
data = np.load('D1.npz')
D=data['D']; N_B=data['N_B']
t=data['t']; n_t=len(t); 


# Prepare the Indices for the repartitions
import math
n_t_B=math.floor(n_t/(N_B-1))
n_T_R= n_t-n_t_B*(N_B-1)# Reminder in the last partition
# This creates a new index (for the partitions):

if n_T_R==0:
# You will have N_B partitions with n_t_B entries each
 n_PAR=N_B
 Indices=np.zeros(n_PAR) 
 Indices[0:N_B]=np.arange(N_B)*n_t_B; 
else:
#You will have N_B partitions with n_t_B entries each + 1 partition with   
 n_PAR=N_B+1 
 Indices=np.zeros(n_PAR)
 Indices[0:N_B]=np.arange(N_B)*n_t_B; Indices[n_PAR-1]=n_t 
 
#%% Loop to Mount K
K=np.zeros((n_t,n_t))

for j in range(1,len(Indices)):
  R1j=int(Indices[j-1]); R2j=int(Indices[j]) # Range of indices with j
  String1='D'+str(j)+'.npz'; data = np.load(String1); D=data['D']
  for k in range(j,N_B):
   R1k=int(Indices[k-1]); R2k=int(Indices[k]) # Range of indices with k   
   String2='D'+str(k)+'.npz' ;data = np.load(String2); D2=data['D']
   D1D2=np.dot(D.transpose(), D2)  
   print('D'+str(j)+' dot '+'D'+str(k))
   K[R1j:R2j,R1k:R2k]=D1D2  # Assign the block
   #K[R1k:R2k,R1j:R2j]=D1D2  # Mirror the Block
   print('Block '+str(j)+'/'+str(len(Indices)-1),'Line '+str(k)+'/'+str(N_B))   


# Now clear everything in the lower triangular part and then mirror it
K_T = np.triu(K, k=1)
K_E = K_T+K_T.T+np.diag(np.diag(K))
    
# Save as numpy array all the data
np.savez('Correlation_K',K=K_E)
 