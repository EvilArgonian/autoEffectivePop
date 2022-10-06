#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

echo "Launching!"

#Establish what species are being processed; $1 and further arguments should be species names matching those used as directory names in the input folder
#If no arguments are present, uses entire input directory
input="../../../input"
processSpecies=()
if [ -z "${1+set}" ]; then 
    for file in $(find ${input}/ -mindepth 1 -maxdepth 1 -type d); do
		processSpecies+=($file)
	done
else 
	for arg in "$@"; do
		processSpecies+=("${input}/"$arg)
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
		
		# Processes input strains into acceptable formats
		sh inputProcessing.sh ${specFolder}
		
		specFolderTemp=../../../temp/${specLabel}
		
		echo "Finding number of strains..."
		strains=$(find ${specFolderTemp}/BLAST/ -mindepth 1 -maxdepth 1 -type f -name '*.ffn' -printf x | wc -c)
		if (( strains > 400 )); then
			echo "High strain count recognized; optimizing for time using blastFilteringLite."
			sh blastFilteringLite.sh ${specFolderTemp}
		elif (( strains < 3 )); then
			echo "Low strain count recognized; no calculations to perform."
			continue
		else
			echo "Normal blast filtering beginning."
			sh blastFiltering.sh ${specFolderTemp}
		fi
		
		sh orthoFinding.sh ${specFolderTemp}
		sh muscleAligning.sh ${specFolderTemp}
		
		specOutputFolder=../../../final_output/${specLabel}
		
		mkdir -p ${specOutputFolder}
		readarray -d ',' -t calculations <<< $(echo $(python manualCalculations.py ${specLabel} ))
		watsThetaS=${calculations[0]}
		watsThetaN=${calculations[1]}
		watsTheta=${calculations[2]}
		piS=${calculations[3]}
		piN=${calculations[4]}
		pi=${calculations[5]}
		dendropyTheta=${calculations[6]}
		dendropyPi=${calculations[7]}
		mutRate=$(echo $(python getMutationRate.py ${specLabel}))
		
		echo watsThetaS: ${watsThetaS} watsThetaN: ${watsThetaN} watsTheta: ${watsTheta} piS: ${piS} piN: ${piN} pi: ${pi} dendropyTheta: ${dendropyTheta} dendropyPi: ${dendropyPi} mutRate: ${mutRate} specLabel: ${specLabel} strains: ${strains}
		python calcEffPopSize.py ${watsThetaS} ${watsThetaN} ${watsTheta} ${piS} ${piN} ${pi} ${dendropyTheta} ${dendropyPi} ${mutRate} ${specLabel} ${strains}
		
		end_time=`date +%s`
		runtime=$((end_time-start_time))
		finished=`date +"%Y-%m-%d %T"`
		echo -e "${specLabel} Process Time (Standard run): " > ${specOutputFolder}/Process_Time.txt
		echo -e "Strains: ${strains}\tRuntime: ${runtime} seconds\tFinished: ${finished}" >> ${specOutputFolder}/Process_Time.txt		
	
	} || { # Catch
		echo "Some kind of interrupting error occurred while processing ${specFolder##*/}"
	}
done
	
