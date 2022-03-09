#!/usr/bin/python
# this script is used to get conservative score for residues of similar chains
from sys import *
from correspond import *
from read_ec import *

def read_pkt_res(infile):
    """
    this function get residue from pkt file
    """
    ress = []
    AAs = ['ALA', 'GLY', 'SER', 'CYS', 'ASP', 'ASN', 'PRO', 'THR', 'VAL', 'GLU', 'PHE', 'HIS', 'ILE', 'LYS', 'LEU', 'MET', 'ARG', 'GLN', 'TRP', 'TYR']
    try:
        data = open(infile,'r').readlines()
    except IOError, io:
        exit('IOError: %s' % str(io))
    cur_num = -100
    cur_res = ''
    cur_chid =''
    for line in data:
        if line.startswith('ATOM'):
            if len(line) >26 :
                chainid = line[21]
                resname = line[17:20]
                res_num = int((line[22:26]).strip())
                if resname in AAs:
                    if resname == cur_res and res_num == cur_num and chainid == cur_chid:
                        continue
                    else:
                        ress.append((res_t2s(resname), res_num, chainid))
                        cur_num = res_num
                        cur_res = resname
                        cur_chid = chainid
                else:
                    continue
            else:
                continue
        else:
            if line.startswith('HETATM'):
                if len(line) >26 :
                    chainid = line[21]
                    resname = line[17:20]
                    res_num = int((line[22:26]).strip())
                    if resname == 'MSE':
                        if resname == cur_res and res_num == cur_num and chainid == cur_chid:
                            continue
                        else:
                            ress.append(('M', res_num, chainid))
                            cur_num = res_num
                            cur_res = resname
                            cur_chid = chainid
                    else:
                        continue
                else:
                    continue
            else:
                continue
    return ress  

if len(argv) != 11:
    exit('Usage: python %s orig_fastafile seqm pdbfile chainid alnd_fastafile seqn ecfile pkt1 pkt2 outfile' % argv[0])

res_crspd = correspond(argv[5],int(argv[6]),argv[1],int(argv[2]),argv[3],argv[4])
ecs = read_ec(argv[7])
ress_pkt1 = read_pkt_res(argv[8])
ress_pkt2 = read_pkt_res(argv[9])
output = open(argv[10],'w')
for res in ress_pkt1:
    if (res[1], res[0]) in res_crspd.keys():
        for nres in ress_pkt2:
            if (nres[1], nres[0]) in res_crspd.keys():
                if res[1] == nres[1] and res[0] == nres[0]:
                    continue
                else:
                    res1_cpd = res_crspd[(res[1],res[0])]
                    res2_cpd = res_crspd[(nres[1],nres[0])]
                    if res1_cpd[0] > res2_cpd[0]:
                        tmpkey = (str(res2_cpd[0]), res2_cpd[1], str(res1_cpd[0]), res1_cpd[1])
                        tmpec = ecs[tmpkey]
                        output.write('%-2s %4d %2s %-2s %4d %2s %s\n' % (nres[0],nres[1], nres[2], res[0], res[1], res[2],tmpec))
                    else:
                        tmpkey = (str(res1_cpd[0]), res1_cpd[1], str(res2_cpd[0]), res2_cpd[1]) 
                        tmpec = ecs[tmpkey]
                        output.write('%-2s %4d %2s %-2s %4d %2s %s\n' % (res[0],res[1], res[2], nres[0], nres[1], nres[2],tmpec))
            else:
                continue
    else:
        continue
output.close()
