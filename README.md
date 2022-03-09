# KeyAlloSite
Companion software for "Coevolution-based prediction of key allosteric residues for protein function regulation".

KeyAlloSite is a computational method for predicting key allosteric residues for protein function regulation and calculating the evolutionary coupling strength between orthosteric and other pockets.

## Dependencies
KeyAlloSite depends on [MAFFT](https://mafft.cbrc.jp/alignment/software/) to perform multiple sequence alignment, you need to install and compile it.

KeyAlloSite depends on [plmc](https://github.com/debbiemarkslab/plmc) to perform coevolutionary analysis, and it can output the inferred evolutionary coupling strengths between all pairs of residue positions. You need to install and compile it.

KeyAlloSite depends on [CAVITY](http://mdl.ipc.pku.edu.cn/mdlweb/register.php?id=14) to detect potential binding sites on the surface of a given protein structure, you can install and compile it alone or you can directly use our web server [CavityPlus](http://www.pkumdl.cn/cavityplus).

## Usage

1. First, multiple sequence alignments are performed using MAFFT.
```
    Example command: ./mafft 5mo4.fa > 5mo4.mafft

```
2. Based on multiple sequence alignments, plmc was used to generate coevolutionary parameters and pairwise evolutionary coupling values between all residues.
```
    Example command: ./plmc -c ./5mo4.EC -o ./5mo4.eij -le 16.0 -lh 0.01 -m 100 -g -f 5mo4_A ./5mo4.mafft >5mo4.log

```

3. According to the coevolutionary parameters obtained in the previous step, the matlab script in plmc was used to calculate the evolutionary coupling strength FN between residues.
```
    Example command: matlab -r read_EC_matrix

```

   **Evolutionary coupling strength between orthosteric and other pockets**:

4. Define orthosteric pockets and use CAVITY to detect all possible ligand binding pockets on the protein surface.

5. Residues in the pockets found by CAVITY that overlap with the orthosteric pocket are removed, and the evolutionary coupling strength between each pocket and the orthosteric pocket is calculated and normalized to Z-scores.
```
    Example command: python RemoveOverlapResidue.py 5mo4 16
                     sh RemoveOverlapPocket.sh 16 4
                     python TransformFN.py 5mo4
                     sh PocketEvolutionCouplingStrength.sh 5mo4 16
                     python NormalizedPocketEvolutionCouplingStrength.py 5mo4 16

    Output: NormalizedPocketEvolutionCouplingStrength_Rank_5mo4.txt: normalized evolutionary coupling strength of each pocket, which have been ranked according to the Z-scores.
```

   **Identification of key allosteric residues**:

6. Calculate the evolutionary coupling values between residues in the orthosteric and allosteric pockets.
```
    Example command: python RemoveOverlapOrthoResidue.py 5mo4
                     sh PocketEvolutionCouplingValue.sh 5mo4

```

7. Key allosteric residues are predicted by pairwise comparison of the differences in evolutionary coupling values corresponding to allosteric pocket residues.
```
    Example command: python PredictKeyAllostericResidue.py 5mo4

    Output: PredictKeyAlloResidues_5mo4_pkt1.txt: predicted key allosteric residues.

```

Please address all questions to lhlai@pku.edu.cn. 
