#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

source Config.shlib

true=1
false=0

skipFiltering=$(config_get Skip_Filtering)
keepPreOrthofinding=$(config_get Keep_Pre_Orthogroup_Files)
keepMuscleInput=$(config_get Keep_Unaligned_Files)
liteFilterThreshold=$(config_get Lite_Filter_Threshold)

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
		
		# This line should determine number of strains (pre-filtering)
		echo "Finding number of unfiltered strains..."
		unfiltered_strains=$(find ${specFolderTemp}/BLAST/ -mindepth 1 -maxdepth 1 -type f -name '*.ffn' -printf x | wc -c)
		
		if (( skipFiltering )); then
			for skipFilterFile in $(find ${specFolderTemp}/BLAST/ -mindepth 1 -maxdepth 1 -type f); do
				cp ${skipFilterFile} ${specFolderTemp}/Nucleotide/
			done
		else
			if (( unfiltered_strains > liteFilterThreshold )); then
				echo "High strain count recognized; optimizing for time using blastFilteringLite."
				sh blastFilteringLite.sh ${specFolderTemp}
			elif (( unfiltered_strains < 3 )); then
				echo "Low strain count recognized; no calculations to perform."
				continue
			else
				echo "Normal blast filtering beginning."
				sh blastFiltering.sh ${specFolderTemp}
			fi
		fi
		
		surviving_strains=$(find ${specFolderTemp}/Nucleotide/ -mindepth 1 -maxdepth 1 -type f -name '*.ffn' -printf x | wc -c)
		
		
		sh orthoFinding.sh ${specFolderTemp} ${keepPreOrthofinding}
		sh muscleAligning.sh ${specFolderTemp} ${keepMuscleInput}
		
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
		
		echo watsThetaS: ${watsThetaS} watsThetaN: ${watsThetaN} watsTheta: ${watsTheta} piS: ${piS} piN: ${piN} pi: ${pi} dendropyTheta: ${dendropyTheta} dendropyPi: ${dendropyPi} mutRate: ${mutRate} specLabel: ${specLabel} unfilteredStrains: ${unfiltered_strains} survivingStrains: ${surviving_strains}
		python calcEffPopSize.py ${watsThetaS} ${watsThetaN} ${watsTheta} ${piS} ${piN} ${pi} ${dendropyTheta} ${dendropyPi} ${mutRate} ${specLabel} ${unfiltered_strains} ${surviving_strains}
		
		end_time=`date +%s`
		runtime=$((end_time-start_time))
		finished=`date +"%Y-%m-%d %T"`
		echo -e "${specLabel} Process Time (Standard run): " > final_output/${specLabel}/Process_Time.txt
		echo -e "Unfiltered Strains: ${unfiltered_strains}\tSurviving Strains: ${surviving_strains}\tRuntime: ${runtime} seconds\tFinished: ${finished}" >> final_output/${specLabel}/Process_Time.txt		
	
	} || { # Catch
		echo "Some kind of interrupting error occurred while processing ${specFolder##*/}"
	}
done
	
