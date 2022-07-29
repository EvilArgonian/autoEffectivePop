#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

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
		echo "Processing input for Species ${processCount}: ${specLabel}"
		start_time=`date +%s`
		
		sh inputProcessing.sh ${specFolder}
		
		specFolderTemp=temp/${specLabel}
		
		# This line should determine number of strains
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
		sh findingOrthogroups.sh ${specFolderTemp}
		sh muscleAligning.sh ${specFolderTemp}
		
		mkdir -p final_output/${specLabel}
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
		
		currentDate=$(date +%d-%b-%Y)
		effPopSizeFile="final_output/Effective_Population_Sizes_${currentDate}.txt"
		if [[ -f "${effPopSizeFile}" ]]; then
			{ time python calcEffPopSize.py ${watsThetaS} ${watsThetaN} ${watsTheta} ${piS} ${piN} ${pi} ${dendropyTheta} ${dendropyPi} ${mutRate} ${specLabel} ${effPopSizeFile} ; } 2>> time_autoEffLaunch.txt
		else
			touch ${effPopSizeFile}
			echo -e "Species\tNE (ThS)\tNE (ThN)\tNE (Th)\tNE (PiS)\tNE (PiN)\tNE (Pi)\tNE (DenTh)\tNE (DenPi)\tThetaS\tThetaN\tTheta\tPiS\tPiN\tPi\tDenTh\tDenPi" > ${effPopSizeFile}
			{ time python calcEffPopSize.py ${watsThetaS} ${watsThetaN} ${watsTheta} ${piS} ${piN} ${pi} ${dendropyTheta} ${dendropyPi} ${mutRate} ${specLabel} ${effPopSizeFile} ; } 2>> time_autoEffLaunch.txt
		fi
		
		end_time=`date +%s`
		runtime=$((end_time-start_time))
		python determineProcessTime.py final_output/${specLabel}/Process_Time.txt ${strains} ${runtime} "Standard" 
		
	
	} || { # Catch
		echo "Some kind of interrupting error occurred while processing ${specFolder##*/}"
	}
done
	
