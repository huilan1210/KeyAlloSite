#Remove residues in the orthosteric pocket that overlap with the allosteric pocket.
import numpy as np
import os
import sys

pdbID = sys.argv[1]

for i in range(1,3):
    file_orth = open('./oth{0}pkt{1}.pdb'.format(pdbID,i),'r+')
    new_file = 'new_test_{0}.pdb'.format(i)
    if not os.path.exists(new_file):
        os.system(r"touch {}".format(new_file))

    file_allo =open('./alo{0}pkt{1}.pdb'.format(pdbID,i),'r+')
    file_orth2 =open('new_test_{0}.pdb'.format(i),'r+')

    fileallo = file_allo.readlines()
    file_allo.close()
    allores = []
    allonum = []
    for line2 in fileallo:
        if line2.startswith('ATOM'):
            allores.append(line2[17:20])
            allonum.append((line2[22:26]).strip())
    print("type(allores):",type(allores),len(allores),type(allonum),len(allonum))

    for line1 in file_orth.readlines():
        if line1.startswith('ATOM'):
            resname1 = line1[17:20]
            #print(resname1)
            res_num1 = (line1[22:26]).strip()
            #print(res_num1)
            if res_num1 in allonum and resname1 in allores:
                line1 =[]
                print("overlap residues",res_num1,resname1)
            else:
                file_orth2.write(line1)
                #file_orth2.write(line1 + '\n')

    file_orth.close()
    file_orth2.close()

    #rename file
    os.rename("new_test_{0}.pdb".format(i),"oth{0}pkt{1}_nooverlap.pdb".format(pdbID,i))