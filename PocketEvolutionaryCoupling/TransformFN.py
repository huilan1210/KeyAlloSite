#Generate evolutionary coupling strength FN between residues.
import numpy as np
import sys

pdbID = sys.argv[1]

FN = np.loadtxt('Result_FN_{0}.txt'.format(pdbID),dtype=str,delimiter=',')
FN = FN.astype(float)
print("FN: ",type(FN),FN.shape)
#half_FN = np.triu(FN).tolist()
#print("half_FN: ",type(half_FN),len(half_FN),half_FN)
FN_list = []
for i in range(0,FN.shape[0]):
    for j in range((i+1),FN.shape[0]):
        FN_list.append(FN[i,j])

print("FN_list: ",len(FN_list),FN_list[0:20])

EC_list = np.loadtxt('{0}.EC'.format(pdbID),dtype=str)
print("EC_list: ",type(EC_list),EC_list.shape)

for i in range(EC_list.shape[0]):
    EC_list[i,5] = FN_list[i]
np.savetxt("./{0}_FN.EC".format(pdbID),EC_list,fmt='%s %s %s %s %s %s')