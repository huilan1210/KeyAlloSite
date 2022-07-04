#Remove residues in the orthosteric pocket that overlap with the allosteric pocket.
import numpy as np
import os
import sys

pdbID = sys.argv[1]

for i in range(1,2):
    file_allo = open('./alo{0}pkt{1}.pdb'.format(pdbID,i),'r+')
    new_file = 'new_test_{0}.pdb'.format(i)
    if not os.path.exists(new_file):
        os.system(r"touch {}".format(new_file))

    file_orth =open('./oth{0}pkt{1}.pdb'.format(pdbID,i),'r+')
    file_allo2 =open('new_test_{0}.pdb'.format(i),'r+')

    fileorth = file_orth.readlines()
    file_orth.close()
    orthres = []
    orthnum = []
    for line2 in fileorth:
        if line2.startswith('ATOM'):
            orthres.append(line2[17:20])
            orthnum.append((line2[22:26]).strip())
    print("type(allores):",type(orthres),len(orthres),type(orthnum),len(orthnum))

    for line1 in file_allo.readlines():
        if line1.startswith('ATOM'):
            resname1 = line1[17:20]
            #print(resname1)
            res_num1 = (line1[22:26]).strip()
            #print(res_num1)
            if res_num1 in orthnum and resname1 in orthres:
                line1 =[]
                print("overlap residues",res_num1,resname1)
            else:
                file_allo2.write(line1)
                #file_orth2.write(line1 + '\n')

    file_allo.close()
    file_allo2.close()

    #rename file
    os.rename("new_test_{0}.pdb".format(i),"alo{0}pkt{1}_nooverlap.pdb".format(pdbID,i))