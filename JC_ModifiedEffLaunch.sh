#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

echo "Launching!"

#Establish what species are being processed; $1 and further arguments should be species names matching those used as directory names in the input folder
processSpecies=()
if [ -z "${1+set}" ]; then 
    for file in $(find modifiedAlignmentInput/ -mindepth 1 -maxdepth 1 -type d); do
		processSpecies+=($file)
	done
else 
	for arg in "$@"; do
		processSpecies+=("modifiedAlignmentInput/"$arg)
	done
fi

echo "Species Processing: ${processSpecies[@]}"

processCount=0
for specFolder in ${processSpecies[@]}; do
	{ # Try	

		specLabel="${specFolder##*/}"
		
		processCount=$(( ${processCount}+1 ))
		echo "Processing input for Species ${processCount}: ${specLabel}"
		start_time=`date +%s`
		
		mkdir -p final_output/${specLabel}
		readarray -d ',' -t calculations <<< $(echo $(python JC_ModifiedManualCalculations.py ${specLabel} ))
		watsThetaS=${calculations[0]}
		watsThetaN=${calculations[1]}
		watsTheta=${calculations[2]}
		piS=${calculations[3]}
		piN=${calculations[4]}
		pi=${calculations[5]}
		dendropyTheta=${calculations[6]}
		dendropyPi=${calculations[7]}
		mutRate=$(echo $(python getMutationRate.py ${specLabel}))
		
		echo watsThetaS: ${watsThetaS} watsThetaN: ${watsThetaN} watsTheta: ${watsTheta} piS: ${piS} piN: ${piN} pi: ${pi} dendropyTheta: ${dendropyTheta} dendropyPi: ${dendropyPi} mutRate: ${mutRate} specLabel: ${specLabel} unfilteredStrains: ${unfiltered_strains} survivingStrains: ${surviving_strains}
		python calcEffPopSize.py ${watsThetaS} ${watsThetaN} ${watsTheta} ${piS} ${piN} ${pi} ${dendropyTheta} ${dendropyPi} ${mutRate} ${specLabel}
		
		end_time=`date +%s`
		runtime=$((end_time-start_time))
		finished=`date +"%Y-%m-%d %T"`
		echo -e "${specLabel} Process Time (Standard run): " > final_output/${specLabel}/Process_Time.txt
		echo -e "Runtime: ${runtime} seconds\tFinished: ${finished}" >> final_output/${specLabel}/Process_Time.txt		
	
	} || { # Catch
		echo "Some kind of interrupting error occurred while processing ${specFolder##*/}"
	}
done
	
