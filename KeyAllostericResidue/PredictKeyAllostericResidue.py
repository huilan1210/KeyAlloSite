#Prediction of key allosteric residues by pairwise comparing the differences in evolutionary coupling values between residues in allosteric pocket.
import numpy as np
from numpy import transpose
import sys
from scipy import stats

pdbID = sys.argv[1]

for h in range(1,2):
    ec = np.loadtxt('./{0}oth_alopkt{1}.txt'.format(pdbID,h),dtype=str)
    print(type(ec),ec.shape,type(ec[:,6]))

    allo_resi_all = np.loadtxt('./allo_resi_{0}_{1}.txt'.format(pdbID,h),dtype=str)
    allo_resi = allo_resi_all[:,2]
    n = int(allo_resi_all.shape[0])

    ec_value=ec[:,6]
    print(type(ec_value),ec_value.shape)
    ec_matrix=np.array(ec_value).reshape(n,-1)
    print("type(ec_matrix):",type(ec_matrix),ec_matrix[0,:])
    np.savetxt("./ec_matrix_{0}_pkt{1}.txt".format(pdbID,h),ec_matrix.astype(float),fmt='%.6f')

#Pairwise comparison between residues in allosteri pocket
    A = np.zeros(shape=(n+1,n))
    B_var=np.zeros(shape=(n,n))
    for i in range(n):
        for j in range((i + 1),n):
            statistic,pvalue= stats.levene(ec_matrix[i,:].astype(float),ec_matrix[j,:].astype(float))
            B_var[i,j]= pvalue
            B_var[j,i]= pvalue
            statistic,pvalue= stats.ttest_ind(ec_matrix[i,:].astype(float),ec_matrix[j,:].astype(float))
            if pvalue < 0.05:
               A[i,j] = 1
               A[j,i] = 1

#Diff_num
    for i in range(n):
        A[n,i]=np.sum(A[0:n,i])
    print("Diff_num: ",A[n,:])

    mean =np.mean(A[n,:])
    std =np.std(A[n,:])
    print(mean,std)
    Zscore = [(i-mean)/std for i in A[n,:]]
    print(Zscore)

#Z-score of Diff_num of all allosteric residues
    allresi_Zscore = np.vstack((allo_resi,Zscore))
    allresi_Zscore_trans = transpose(allresi_Zscore)
    allresi_Zscore_trans = allresi_Zscore_trans.astype(float)
    allresi_Zscore_rank = allresi_Zscore_trans[np.lexsort(-allresi_Zscore_trans.T)]
    print("allresi_Zscore_rank: ",allresi_Zscore_rank)
    np.savetxt("./Allresi_Zscore_rank_{0}_pkt{1}.txt".format(pdbID,h),allresi_Zscore_rank,delimiter=' ',fmt='%d %.2f')

    key_resi=[]
    Zscore2=[]
    for i in range(allo_resi.shape[0]):
        if Zscore[i] > 0.8:
           key_resi.append(int(allo_resi[i]))
           Zscore2.append(Zscore[i].round(2))
    print("key_resi:",key_resi)
    resi_Zscore2 = np.vstack((key_resi,Zscore2))
    resi_Zscore2_trans = transpose(resi_Zscore2)
    resi_Zscore2_rank = resi_Zscore2_trans[np.lexsort(-resi_Zscore2_trans.T)]
    print("resi_Zscore2_rank:",type(resi_Zscore2_rank),resi_Zscore2_rank)

    key_resiname = []
    key_chain = []
    for i in range(resi_Zscore2_rank.shape[0]):
        for j in range(allo_resi_all.shape[0]):
            if int(resi_Zscore2_rank[i,0]) == int(allo_resi_all[j,2]):
               key_resiname.append(allo_resi_all[j,0])
               key_chain.append(allo_resi_all[j,1])
    key_name_chain = np.vstack((key_resiname,key_chain))
    key_name_chain_trans = transpose(key_name_chain)
    key_final = np.hstack((key_name_chain_trans,resi_Zscore2_rank))
    for i in range(key_final.shape[0]):
        key_final[i,2] = int(key_final[i,2].astype(float))

    print("Predicted allosteric key residues: ",type(key_final),key_final.shape,key_final)
    np.savetxt("./PredictKeyAlloResidues_{0}_pkt{1}.txt".format(pdbID,h),key_final,delimiter=' ',fmt='%s %s %s %s')
