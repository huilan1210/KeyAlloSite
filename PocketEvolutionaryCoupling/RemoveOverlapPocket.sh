#Remove cavities that overlap more than 50% of the orthosteric pocket.
for ((i=1;i<=$1;i++));
do
    cat thischains_cavity_${i}_nooverlap.pdb |grep '^ATOM  ' |cut -c18-26 |sort -u |sort -k 3n > thischains_cavity_${i}_nooverlap.txt 
    cat thischains_cavity_${i}_nooverlap.txt |wc -l >>number_resi_1.txt
    cat thischains_cavity_${i}.pdb |grep '^ATOM  ' |cut -c18-26 |sort -u |sort -k 3n > thischains_cavity_${i}.txt 
    cat thischains_cavity_${i}.txt |wc -l >>number_resi_2.txt
done
cp number_resi_1.txt number_resi_nooverlap.txt
rm number_resi_1.txt
cp number_resi_2.txt number_resi.txt
rm number_resi_2.txt

exclude_list="${@:2}"
echo $exclude_list
if [ ${#exclude_list} == 0 ]; then
    echo No known orthosteric pocket is entered
else
    for g in $exclude_list;do
        mv thischains_cavity_${g}_nooverlap.txt thischains_cavity_${g}_nooverlap_ortho.txt
        mv thischains_cavity_${g}_nooverlap.pdb thischains_cavity_${g}_nooverlap_ortho.pdb
    done
fi

exec 3<"number_resi.txt"
exec 4<"number_resi_nooverlap.txt"
while read line1<&3 && read line2<&4
do
    #echo $line2/$line1
    ratio=$(printf "%.1f" `echo "scale=2;$line2/$line1"|bc`)
    echo $ratio >> cavity_nooverlap_ratio.txt
done

cp cavity_nooverlap_ratio.txt cavity_nooverlap_ratio_final.txt
rm cavity_nooverlap_ratio.txt
cat cavity_nooverlap_ratio_final.txt | awk '{if($1 < 0.5 ) printf("%d\n", NR)}'> overlap.txt

cat overlap.txt | while read line;
do
    echo The cavity$line is overlap with the orthosteric site
    if [ -e "thischains_cavity_${line}_nooverlap_ortho.txt" ]; then
        echo This cavity has been marked
    else
        mv thischains_cavity_${line}_nooverlap.txt thischains_cavity_${line}_nooverlap_ortho.txt
        mv thischains_cavity_${line}_nooverlap.pdb thischains_cavity_${line}_nooverlap_ortho.pdb
    fi
done
