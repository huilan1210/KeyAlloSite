#Normalized evolutionary coupling strength between orthosteric and other pockets.
import numpy as np
import re
import sys
import os
from numpy import transpose
import pandas as pd

pdbID = sys.argv[1]
pocketNum = sys.argv[2]

#Load the evolutionary couping strength between the orthosteric and other pockets.
SumcorrList = []
cavity = []

for h in range(1,int(pocketNum)+1):
    if os.path.exists("{0}_ortho_cavity_{1}.txt".format(pdbID,h)):
        cav_h_site_ori = np.loadtxt('{0}_ortho_cavity_{1}.txt'.format(pdbID,h),dtype=str)
        cav_h_site = cav_h_site_ori[:,6]
        cav_h_site = cav_h_site.astype(float)
        total_corr = np.sum(cav_h_site)
        SumcorrList.append(total_corr)
        cavity.append(h)
    else:
        print("ortho_cavity_%d.txt does not exist"%h)
print("SumcorrList: ",SumcorrList)

SumcorrList = np.array(SumcorrList)
mean =np.mean(SumcorrList)
std =np.std(SumcorrList)
print(mean,std)
Zscore = [((i-mean)/std).round(2) for i in SumcorrList]
print(Zscore)

cavity =np.array(cavity)
print("Cavities: ",type(cavity),cavity)
Zscore_rank = np.vstack((cavity,Zscore))
Zscore_rank = transpose(Zscore_rank)
Zscore_rank =Zscore_rank[np.lexsort(-Zscore_rank.T)]
print("SumFNList_Zscore_rank: ",Zscore_rank)
Zscore_rank_pd = pd.DataFrame(Zscore_rank)
for i in range(Zscore_rank.shape[0]):
    Zscore_rank_pd.iloc[i,0] = "cavity_"+str(int(Zscore_rank[i,0]))

Zscore_rank_pd.to_csv('NormalizedPocketEvolutionCouplingStrength_Rank_{0}.txt'.format(pdbID),header=None,sep=' ',index=False)

