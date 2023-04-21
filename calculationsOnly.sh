#!/bin/bash
set -uo pipefail
IFS=$'\n\t'

echo "Running calculations only..."

#Establish what species are being processed; $1 and further arguments should be species names matching those used as directory names in the input folder
processSpecies=()
if [ -z "${1+set}" ]; then 
    for file in $(find temp/ -mindepth 1 -maxdepth 1 -type d); do
		processSpecies+=($file)
	done
else 
	for arg in "$@"; do
		processSpecies+=("temp/"$arg)
	done
fi

for specFolder in ${processSpecies[@]}; do
	{ # Try
		specLabel="${specFolder##*/}"
		if [[ ! " ${processSpecies[@]} " =~ " temp/${specLabel} " ]]; then
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
		dendropyTheta=${calculations[6]}
		dendropyPi=${calculations[7]}
		mutRate=$(echo $(python getMutationRate.py ${specLabel}))
		
		echo watsThetaS: ${watsThetaS} watsThetaN: ${watsThetaN} watsTheta: ${watsTheta} piS: ${piS} piN: ${piN} pi: ${pi} dendropyTheta: ${dendropyTheta} dendropyPi: ${dendropyPi} mutRate: ${mutRate} specLabel: ${specLabel} strains: "N/A"
		python calcEffPopSize.py ${watsThetaS} ${watsThetaN} ${watsTheta} ${piS} ${piN} ${pi} ${dendropyTheta} ${dendropyPi} ${mutRate} ${specLabel}
	} || { # Catch
		echo "Some kind of interrupting error occurred while processing ${specFolder##*/}"
	}
done
