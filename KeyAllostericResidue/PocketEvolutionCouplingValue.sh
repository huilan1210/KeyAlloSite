#Evolutionary coupling values between residues in orthosteric and allosteric pockets.
for ((i=1;i<=2;i++));
do
    python2 ./ec_of_pkt1_pkt2.py $1.fasta 1 $1.pdb A ./$1.mafft 1 ./$1.EC ./alo$1pkt${i}.pdb ./oth$1pkt${i}_nooverlap.pdb $1oth_alopkt${i}.txt
    cat alo$1pkt${i}.pdb |grep '^ATOM  ' |cut -c18-26 |sed 's/...../& /g' |sort -u |sort -k 3n > allo_resi_$1_${i}.txt
done

