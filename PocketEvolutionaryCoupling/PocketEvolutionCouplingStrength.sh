#Evolutionary coupling strength between residues in orthosteric and other pockets.
for ((i=1;i<=$2;i++));
do
    if [ -f "thischains_cavity_${i}_nooverlap.pdb" ]; then
        python2 ./ec_of_pkt1_pkt2.py $1.fasta 1 $1.pdb A ./$1.mafft 1 ./$1_FN.EC ./thischains_cavity_${i}_nooverlap.pdb ./oth$1pkt1.pdb $1_ortho_cavity_${i}.txt
    else
        echo cavity_${i} overlaps with orthosteric pocket
    fi
done
