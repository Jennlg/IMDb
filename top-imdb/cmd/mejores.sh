#!/bin/bash
cd ~/Escritorio/PCD/aclImdb/train/pos
for file in *.txt; do  
    id=$(echo "$file" | cut -d'_' -f1)   
    score=$(echo "$file" | cut -d'_' -f2 | cut -d'.' -f1)   
    echo "$id $score"; 
done > ../id_scores.txt 

sort -V ../id_scores.txt > ../sort_id.txt

awk '{getline url < "urls_pos.txt"; print url, $2}' ../sort_id.txt > ../urls_scores.txt

awk '{scores[$1] += $2; count[$1]++}
    END {for (url in scores) print url, scores[url]/count[url]}' 
    ../urls_scores.txt > ../avg_urls_scores.txt

sed 's/\/usercomments//g' ../avg_urls_scores.txt | sort -k2,2nr | head -n 10 > ../10mejores.txt
