#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

echo "Running calculations only..."

#Establish what species are being processed; $1 and further arguments should be species names matching those used as directory names in the input folder
processSpecies=()
if [ -z "${1+set}" ]; then 
    for file in $(find input/ -mindepth 1 -maxdepth 1 -type d); do
		processSpecies+=($file)
	done
else 
	for arg in "$@"; do
		processSpecies+=("input/"$arg)
	done
fi

effPopSizeCurrentDate=$(date +%d-%b-%Y)
effPopSizeFile="final_output/Calculations_Only_Effective_Population_Sizes_${effPopSizeCurrentDate}.txt"
rm -f ${effPopSizeFile}
touch ${effPopSizeFile}
echo "Species	NE (ThS)	NE (ThN) NE (Th) 	NE (PiS) 	NE (PiN)  NE (Pi) 	ThetaS 	Theta	PiS 	Pi" > final_output/Effective_Population_Sizes_${effPopSizeCurrentDate}.txt

for specFolder in $(find muscle_output/ -mindepth 1 -maxdepth 1 -type d); do
	specLabel="${specFolder##*/}"
	if [[ ! " ${processSpecies[@]} " =~ " input/${specLabel} " ]]; then
		continue
	fi
	rm -rf final_output/${specLabel}
	mkdir -p final_output/${specLabel}
	readarray -d ',' -t calculations <<< $(echo $(python manualCalculations.py ${specLabel}))
	watsThetaS=${calculations[0]}
	watsThetaN=${calculations[1]}
	watsTheta=${calculations[2]}
	piS=${calculations[3]}
	piN=${calculations[4]}
	pi=${calculations[5]}
	mutRate=$(echo $(python getMutationRate.py ${specLabel}))
	
	echo watsThetaS: ${watsThetaS} watsThetaN: ${watsThetaN} watsTheta: ${watsTheta} piS: ${piS} piN: ${piN} pi: ${pi} mutRate: ${mutRate} specLabel: ${specLabel}
	
	python calcEffPopSize.py ${watsThetaS} ${watsThetaN} ${watsTheta} ${piS} ${piN} ${pi} ${mutRate} ${specLabel} ${effPopSizeFile}
	
done


