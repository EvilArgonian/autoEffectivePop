#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

#Don't run both this script and the normal with-filtering script on the same species at the same time; they will interfere with each other.

echo "Launching!"

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

echo "Species Processing: ${processSpecies[@]}"

processCount=0
for specFolder in ${processSpecies[@]}; do
	{ # Try	

		specLabel="${specFolder##*/}"
		
		processCount=$(( ${processCount}+1 ))
		echo "Species ${processCount}: ${specLabel}"
		
		{ time sh inputProcessing.sh ${specFolder} ; } 2> time_autoEffLaunch.txt
		
		specFolderTemp=temp/${specLabel}
		
		# This line should determine number of strains
		strains=$(find ${specFolderTemp}/BLAST/ -mindepth 1 -maxdepth 1 -type f -name '*.ffn' -printf x | wc -c)
		#if (( strains > 400 )); then
		#	echo "High strain count recognized; optimizing for time using blastFilteringLite."
		#	{ time sh blastFilteringLite.sh ${specFolderTemp} ; } 2>> time_autoEffLaunch.txt
		#elif (( strains < 3 )); then
		#	echo "Low strain count recognized; no calculations to perform."
		#	continue
		#else
		#	echo "Normal blast filtering beginning."
		#	{ time sh blastFiltering.sh ${specFolderTemp} ; } 2>> time_autoEffLaunch.txt
		#fi
		
		echo "Skipping filtering by simply using all strain ffn files."
		cp -r ${specFolderTemp}/BLAST/*.ffn ${specFolderTemp}/Nucleotide/
		
		{ time sh orthoFinding.sh ${specFolderTemp} ; } 2>> time_autoEffLaunch.txt
		
		{ time sh findingOrthogroups.sh ${specFolderTemp} ; } 2>> time_autoEffLaunch.txt
		
		{ time sh muscleAligning.sh ${specFolderTemp} ; } 2>> time_autoEffLaunch.txt
		
		
		
		mkdir -p final_output/${specLabel}
		{ time readarray -d ',' -t calculations <<< $(echo $(python manualCalculations.py ${specLabel} )) ; } 2>> time_autoEffLaunch.txt
		watsThetaS=${calculations[0]}
		watsThetaN=${calculations[1]}
		watsTheta=${calculations[2]}
		piS=${calculations[3]}
		piN=${calculations[4]}
		pi=${calculations[5]}
		dendropyTheta=${calculations[6]}
		dendropyPi=${calculations[7]}
		{ time mutRate=$(echo $(python getMutationRate.py ${specLabel})) ; } 2>> time_autoEffLaunch.txt
		
		echo watsThetaS: ${watsThetaS} watsThetaN: ${watsThetaN} watsTheta: ${watsTheta} piS: ${piS} piN: ${piN} pi: ${pi} dendropyTheta: ${dendropyTheta} dendropyPi: ${dendropyPi} mutRate: ${mutRate} specLabel: ${specLabel} strains: ${strains}
		
		currentDate=$(date +%d-%b-%Y)
		effPopSizeFile="final_output/Effective_Population_Sizes_No_Filtering_${currentDate}.txt"
		if [[ -f ${effPopSizeFile} ]]; then
			{ time python calcEffPopSize.py ${watsThetaS} ${watsThetaN} ${watsTheta} ${piS} ${piN} ${pi} ${dendropyTheta} ${dendropyPi} ${mutRate} ${specLabel} ${effPopSizeFile} ; } 2>> time_autoEffLaunch.txt
		else
			touch ${effPopSizeFile}
			echo "Species	NE (ThS)	NE (ThN) NE (Th) 	NE (PiS) 	NE (PiN)  NE (Pi) 	ThetaS 	Theta	PiS 	Pi" > ${effPopSizeFile}
			{ time python calcEffPopSize.py ${watsThetaS} ${watsThetaN} ${watsTheta} ${piS} ${piN} ${pi} ${dendropyTheta} ${dendropyPi} ${mutRate} ${specLabel} ${effPopSizeFile} ; } 2>> time_autoEffLaunch.txt
		fi
		
		python determineProcessTime.py final_output/${specLabel}/Process_Time.txt ${strains} "No Filter"
	
	} || { # Catch
		echo "Some kind of interrupting error occurred while processing ${specFolder##*/}"
	}
done
	
