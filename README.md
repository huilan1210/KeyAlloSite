# KeyAlloSite
Companion software for "Coevolution-based prediction of key allosteric residues for protein function regulation".
KeyAlloSite is a computational method for predicting key allosteric residues for protein function regulation.

## Dependencies
KeyAlloSite depends on [MAFFT](https://mafft.cbrc.jp/alignment/software/) to perform multiple sequence alignment, you need to install and compile it.

KeyAlloSite depends on [plmc](https://github.com/debbiemarkslab/plmc) to perform coevolutionary analysis, and it can output the inferred evolutionary coupling strengths between all pairs of residue positions. You need to install and compile it.

KeyAlloSite depends on [CAVITY](http://mdl.ipc.pku.edu.cn/mdlweb/register.php?id=14) to detect potential binding sites on the surface of a given protein structure, you can install and compile it alone or you can directly use our web server [CavityPlus](http://www.pkumdl.cn/cavityplus).

## Usage

1. First, multiple sequence alignments are performed using MAFFT.
```
    Example command: ./mafft 3lcb.fa > 3lcb.mafft

```
2. Based on multiple sequence alignments, plmc was used to generate coevolutionary parameters and pairwise evolutionary coupling values between all residues.
```
    Example command: ./plmc -c ./3lcb.EC -o ./3lcb.eij -le 16.0 -lh 0.01 -m 100 -g -f ACEK_ECO5E ./3lcb.mafft >3lcb.log

```

3. According to the coevolutionary parameters obtained in the previous step, the matlab script in plmc was used to calculate the evolutionary coupling strength FN between residues.
```
    Example command: matlab -r read_EC_matrix

```

   **Evolutionary coupling strength between orthosteric and other pockets**:

4. Define orthosteric pockets and use CAVITY to detect all possible ligand binding pockets on the protein surface.

5. Residues in the pockets found by CAVITY that overlap with the orthosteric pocket are removed, and the evolutionary coupling strength between each pocket and the orthosteric pocket is calculated and normalized to Z-scores.
```
    Example command: python RemoveOverlapResidue.py 3lcb 19
                 sh RemoveOverlapPocket.sh 19 10
                 sh PocketsEvolutionaryCouplingStrength.sh 3lcb 19
                 python NormalizedPocketsEvolutionaryCouplingStrength.py 3lcb 19

```

   **Identification of key allosteric residues**:

6. Calculate the evolutionary coupling value between the orthosteric and allosteric pockets.
```
    Example command: sh PocketsEvolutionaryCouplingValue.sh 3lcb

```

7. Key allosteric residues are predicted by pairwise comparison of the differences in evolutionary coupling values corresponding to allosteric pocket residues.
```
    Example command: python PredictKeyAllostericResidue.py 3lcb

```

Please address all questions to lhlai@pku.edu.cn. 
