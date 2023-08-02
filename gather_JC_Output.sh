#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

echo "Moving JC Modified-Processing Input!"

#Establish what species are being processed; $1 and further arguments should be species names matching those used as directory names in the input folder
processInput=()
if [ -z "${1+set}" ]; then 
    for file in $(find ../../jcaraway/collapsed_fastas/ -mindepth 1 -maxdepth 1 -type d); do
		processInput+=($file)
	done
else 
	for arg in "$@"; do
		processInput+=("../../jcaraway/collapsed_fastas/"$arg)
	done
fi

echo "Input Processing: ${processInput[@]}"

outTable="JC_Out_Table.txt"
stageFolder="modifiedAlignmentInput"

echo -e "Source\tGene\tTheta S\tTheta N\tTheta\tPot. Syn\tPot. NonSyn\tPot. All\tAct. Syn\t Act.NonSyn\tAct. All" > ${outTable}

processCount=0
for inputFolder in ${processInput[@]}; do
	{ # Try	
		inputLabel="${inputFolder##*/}"
		
		processCount=$(( ${processCount}+1 ))
		
		python gather_JC_Output.py ${inputLabel} ${outTable}
		
		if [[ -f "${stageFolder}/${inputLabel}_1a/ORF1a_collapsed_mutation_fastas.fa" ]]; then #Check if it contains gene ORF1a, which is contained within ORF1ab, and must be processed separately to avoid counting the sites doubly
			echo "Found ORF1a for: ${inputLabel}"
			python gather_JC_Output.py ${inputLabel}_1a ${outTable}
		fi
	} || { # Catch
		echo "Some kind of interrupting error occurred while processing ${inputFolder##*/}"
	}
done
