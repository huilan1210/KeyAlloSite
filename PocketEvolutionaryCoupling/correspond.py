#!/usr/bin/python
from sys import *
import numpy
import os

def readFasta(infile):
    """
    This function read sequences from fasta file
    """
    try:
        data = open(infile,'r').readlines()
    except IOError,io:
        exit('IOError: %s' % str(io))

    seqs=[]
    length = len(data)
    tmpseq=''
    for i in range(length):
        if data[i].startswith('>'):
            if i == 0:
                continue
            else:
                seqs.append(tmpseq)
                tmpseq = ''
        else:
            if i == length-1 :
                tmpseq = tmpseq + data[i].strip()
                seqs.append(tmpseq)
            else:
                tmpseq = tmpseq + data[i].strip()
    return seqs

def readMafftFasta(infile):
    """
    This function read sequences from fasta file generated by mafft
    """
    try:
        data = open(infile,'r').readlines()
    except IOError,io:
        exit('IOError: %s' % str(io))

    seqs=[]
    length = len(data)
    tmpseq=''
    seq_init_num = []
    for i in range(length):
        if data[i].startswith('>'):
            x = data[i].split('/')
            y = (x[1]).split('-')
            seq_init_num.append(int(y[0]))
            if i == 0:
                continue
            else:
                seqs.append(tmpseq)
                tmpseq = ''
        else:
            if i == length-1 :
                tmpseq = tmpseq + data[i].strip()
                seqs.append(tmpseq)
            else:
                tmpseq = tmpseq + data[i].strip()
    return seqs, seq_init_num
def res_t2s(resname_t):
    """
    res_t2s(resname_t) -> 'ALA->A', 'CYS->C', 'ARG->R', or 'like this'
    resname_t (str) Amino acid (3-letter)
    """
    return {'ALA':'A', 'GLY':'G', 'SER':'S', 'CYS':'C', 'ASP':'D', 'ASN':'N',
                'PRO':'P', 'THR':'T', 'VAL':'V', 'GLU':'E', 'PHE':'F', 'HIS':'H',
                'ILE':'I', 'LYS':'K', 'LEU':'L', 'MET':'M', 'ARG':'R', 'GLN':'Q',
                'TRP':'W', 'TYR':'Y'}[resname_t]
   
def readPDB(infile,chainid):
    """
    This function read sequence from PDB file, all the residues with 3D coordinates were record
    this function is for the chain that is not segmented.
    """
    AAs = ['ALA', 'GLY', 'SER', 'CYS', 'ASP', 'ASN', 'PRO', 'THR', 'VAL', 'GLU', 'PHE', 'HIS', 'ILE', 'LYS', 'LEU', 'MET', 'ARG', 'GLN', 'TRP', 'TYR']
    try:
        data = open(infile,'r').readlines()
    except IOError,io:
        exit('IOError: %s' % str(io))
    NMRlabel = 0
    for line in data:
        if line.startswith('EXPDTA'):
            xx = line.split()
            if len(xx) == 3 and xx[1] == 'SOLUTION' and xx[2] == 'NMR':
                NMRlabel = 1
                break
    if NMRlabel == 1:
        for line in data:
            if line.startswith('MODEL'):
                yy = line.split()
                if len(yy) == 2 and yy[1] == '1':
                    nstartl = data.index(line)+1
                elif len(yy) == 2 and yy[1] == '2':
                    nfinal = data.index(line)
                    break
        data1 = data[nstartl:nfinal]
    else:
        data1 = data
    resnum = []
    seq = ''
    cur_num = -100
    cur_res = ''
    for line in data1:
        if line.startswith('ATOM'):
            if len(line) >26 and line[21] == chainid:
                resname = line[17:20]
                res_num = int((line[22:26]).strip())
                if resname in AAs:
                    if resname == cur_res and res_num == cur_num:
                        continue
                    else:
                        resnum.append(res_num)
                        seq = seq + res_t2s(resname)
                        cur_num = res_num
                        cur_res = resname
                else:
                    continue
            else:
                continue
        else:
            if line.startswith('HETATM'):
                if len(line) >26 and line[21] == chainid:
                    resname = line[17:20]
                    res_num = int((line[22:26]).strip())
                    if resname == 'MSE':
                        if resname == cur_res and res_num == cur_num:
                            continue
                        else:
                            resnum.append(res_num)
                            seq = seq + 'M'
                            cur_num = res_num
                            cur_res = resname
                    else:
                        continue
                else:
                    continue
            else:
                continue
    misresl = -100
    for line in data:
        if line.startswith('REMARK 465   M RES C SSSEQI'):
            misresl = data.index(line) + 1
            break
    if misresl != -100:
        misresnums = []
        misress = ''
        for line in data[misresl:]:
            if line.startswith('REMARK 465'):
                x = (line[:26]).split()
                tmpresnum = int(x[4])
                if x[3] == chainid and tmpresnum >= resnum[0] and tmpresnum <= resnum[-1]:
                    if len(misresnums) == 0:
                        misresnums.append(tmpresnum)
                        misress = misress + res_t2s(x[2])
                    else:
                        if (tmpresnum - misresnums[-1]) <= 1:
                            misresnums.append(tmpresnum)
                            misress = misress + res_t2s(x[2])
                        else:
                            insertpos = resnum.index(misresnums[0] -1) + 1
                            tmpresnums = resnum[:insertpos] + misresnums + resnum[insertpos:]
                            tmpseq_tot = seq[:insertpos] + misress + seq[insertpos:]
                            resnum = tmpresnums
                            seq = tmpseq_tot
                            misresnums = []
                            misress = ''
                            misresnums.append(tmpresnum)
                            misress = misress + res_t2s(x[2])
                else:
                    continue
            else:
                if len(misresnums) > 0:
                    insertpos = resnum.index(misresnums[0] -1) + 1
                    tmpresnums = resnum[:insertpos] + misresnums + resnum[insertpos:]
                    tmpseq_tot = seq[:insertpos] + misress + seq[insertpos:]
                    resnum = tmpresnums
                    seq = tmpseq_tot
                break
            
    return resnum,seq

def write_fasta(seqs, headstr, filename):
    """
    this function write a seqs as a fasta file with head headstr
    """
    output = open(filename, 'w')
    output.write('>%s\n' % headstr)
    length = len(seqs)
    linen = length/80
    startn = 0 
    finaln = 0
    for i in range(linen):
        startn = i*80
        finaln = (i+1)*80
        output.write('%s\n' % seqs[startn:finaln])
    output.write('%s\n' % seqs[finaln:])
    output.close()

def get_blst_result(blstofile):
    """
     this function get the first match position of the blast results of two sequences
    """
    data = open(blstofile, 'r').readlines()
    for line in data:
        if line.startswith('Query:'):
            linen = data.index(line)
            break
    x = data[linen].split()
    qinit = int(x[1])
    y = data[linen + 2].split()
    sinit = int(y[1])
    return qinit,sinit

def correspond(align_fastafile, seqn, origin_fastafile, seqm, pdbfile, chainid):
    """
    this function will identify the correspondence between sequenc from PDB file and the sequence from aligned_fastafile
    """
    res_crspd = {}
    alned_seqs,seq_init_num = readMafftFasta(align_fastafile)
    pdbresn, pdbseq = readPDB(pdbfile,chainid)
    orgn_seqs = readFasta(origin_fastafile)
    alnseq = alned_seqs[seqn - 1]
    alnseq_init_num = seq_init_num[seqn - 1]
    orgnseq = orgn_seqs[seqm - 1]
    #first identify the seq number of pdb file in origin fasta file
    try:
        startp = orgnseq.index(pdbseq)
    except:
        stdout.write('the original sequence is: \n')
        stdout.write('%s\n' % orgnseq)
        stdout.write('the sequence from PDB is: \n')
        stdout.write('%s\n' % pdbseq)
        exit('above two sequences not matched, please do a blast to identify where is the mismatch\n')
    #second, get the non-gap residues in alnseq with seq num and residue name
    alnseq_without_gap = ''
    alnres_num = []
    for i in range(len(alnseq)):
        if alnseq[i] == '-' :
            continue
        else:
            j = i + alnseq_init_num
            alnres_num.append(j)
            alnseq_without_gap = alnseq_without_gap + alnseq[i]
    # third, identify the seq number of alnseq in the origin fasta file
    try:
        startp1 = orgnseq.index(alnseq_without_gap)
    except:
        stdout.write('the original sequence is: \n')
        stdout.write('%s\n' % orgnseq)
        stdout.write('the sequence from aligned fasta is: \n')
        stdout.write('%s\n' % alnseq_without_gap)
        stdout.write('The above two sequences not matched! next do a blast to identify where is the start position in original sequence\n')
        write_fasta(orgnseq, 'original seq', './tmp1.fa')
        write_fasta(alnseq_without_gap, 'alned seq', './tmp2.fa')
        cmd = '/lustre1/dengmh_pkuhpc/jxie/src/soft/mpiblast-1.6.0/ncbi/bin/bl2seq ' + '-i ' + './tmp1.fa ' + '-j ' + './tmp2.fa ' + '-p blastp ' + '-e 0.01 ' + '-o blst_out.txt'
        os.system(cmd)
        o_init, a_init = get_blst_result('./blst_out.txt')
        startp1 = o_init - a_init
        os.system('rm ./tmp1.fa')
        os.system('rm ./tmp2.fa')
        os.system('rm ./blst_out.txt')
    # fourth, identify the correspondence between residues in pdb file and residues in alned seq
    for i in range(len(pdbseq)):
        if (i+startp) < startp1:
            continue
        elif (i+startp) >= (startp1 + len(alnseq_without_gap)):
            continue
        else:
            tmpkey = (pdbresn[i],pdbseq[i])
            j = i + startp - startp1
            res_crspd[tmpkey] = (alnres_num[j], alnseq_without_gap[j])
    return res_crspd
            
