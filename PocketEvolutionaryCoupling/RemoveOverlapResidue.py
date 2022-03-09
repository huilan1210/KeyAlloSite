#Remove residues in cavities that overlap with the orthosteric pocket.
import numpy as np
import re
import os
import sys

pdbID = sys.argv[1]
pocketNum = sys.argv[2]

file_orth = open('./oth{0}pkt1.pdb'.format(pdbID),'r+')
fileorth = file_orth.readlines()
file_orth.close()
orthres = []
orthnum = []
for line2 in fileorth:
    if line2.startswith('ATOM'):
        orthres.append(line2[17:20])
        orthnum.append((line2[22:26]).strip())
print("type(orthres):",type(orthres),len(orthres),type(orthnum),len(orthnum))

for i in range(int(pocketNum)):
    pocnum = i + 1
    print("cavity: ",pocnum)
    file_cav =open('thischains_cavity_{0}.pdb'.format(pocnum),'r+')
    new_file = 'new_test.pdb'
    if not os.path.exists(new_file):
        os.system(r"touch {}".format(new_file))
    file_cav2 =open('new_test.pdb','r+')

    for line1 in file_cav.readlines():
        if line1.startswith('ATOM'):
            resname1 = line1[17:20]
            #print(resname1)
            res_num1 = (line1[22:26]).strip()
            #print(res_num1)
            if res_num1 in orthnum and resname1 in orthres:
                line1 =[]
                print("overlap residues",res_num1,resname1)
            else:
                file_cav2.write(line1)
                #file_orth2.write(line1 + '\n')

    file_cav.close()
    file_cav2.close()

    #rename file
    os.rename("new_test.pdb","thischains_cavity_{0}_nooverlap.pdb".format(pocnum))
