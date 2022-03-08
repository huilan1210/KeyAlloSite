# KeyAlloSite
Coevolution-based prediction of key allosteric residues for protein function regulation.
KeyAlloSite is a computational method for predicting key allosteric residues for protein function regulation.

## Dependencies
KeyAlloSite depends on [MAFFT](https://mafft.cbrc.jp/alignment/software/) to perform multiple sequence alignment, you need to install and compile it.

KeyAlloSite depends on [plmc](https://github.com/debbiemarkslab/plmc) to perform coevolutionary analysis, and it can output the inferred evolutionary coupling strengths between all pairs of residue positions. You need to install and compile it.

KeyAlloSite depends on [CAVITY](http://mdl.ipc.pku.edu.cn/mdlweb/register.php?id=14) to detect potential binding sites on the surface of a given protein structure, you can install and compile it alone or you can directly use our web server [CavityPlus](http://www.pkumdl.cn/cavityplus).

The following modules are required and will be installed upon installation:

-   [numpy](https://github.com/numpy/numpy)
-   [Matplotlib-PyPlot](https://github.com/zawster/Matplotlib-PyPlot)


## Usage

1. First, the user need to identify the potential binding pockets on the surface of a given protein structure and the orthosteric pocket.
2. Second, the user need to deal with the cavity files, such as renumbering residues and removing residues in the pockets that overlap with the orthosteric pocket.
```
usage: sh cavity_new.sh [PDB_ID] [Number_of_pockets] [The_number_of_the_orthosteric_pocket_found_by_CAVITY] 

```

3. Third, the user can calculate the motion correlations among the orthosteric pocket and other pockets in the top 3 slow modes and top 10 fast modes.
```
usage: python correlation_pockets.py [PDB_ID] [Number_of_pockets]

```

4. Finally, the predicted potential allosteric pockets and the corresponding Z-Score will be displayed on the screen and saved as a file.

**Example**:

Input:

```
sh cavity_new.sh 1a3w 14 1

python correlation_pockets.py 1a3w 14
```

Output files include:

```
Cavity_Zscore_Prediction_Allo_Site_1a3w.txt:   predicted potential allosteric sites,the first column is the number of the pockets, and the second column is the Z-Score corresponding to the pockets.
Cavity_Zscore_Rank_All_1a3w.txt:               the rankings of all pockets and the corresponding Z-Score.
Top3SlowMode_Zscore_Rank_1a3w.txt:             the rankings of all pockets in the top 3 slow modes and the corresponding Z-Score.
Top10FastMode_Zscore_Rank_1a3w.txt:            the rankings of all pockets in the top 10 fast modes and the corresponding Z-Score.
```


Please address all questions to juanxie@pku.edu.cn 

