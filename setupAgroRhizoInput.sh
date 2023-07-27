#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

true=1
false=0

specFolder="input/RhizobiumAgrobacterium_Group"
importFolder="../AgroRhizoGroup"
unzipFolder="../UnzipAgroRhizoGroup"

echo "Beginning moving of AgroRhizo Input."

for file in $(find ${importFolder} -mindepth 1 -maxdepth 1); do
	zipLabel="${file##*/}"
	label="${zipLabel%%.zip*}"

	mkdir ${specFolder}/${label}
	
	weGotIt=${false}
	for cdsFile in $(find ${unzipFolder}/${label}/ncbi_dataset/data/GCA_*/ -mindepth 1 -maxdepth 1); do
		if [[ "${cdsFile}" == *cds_from_genomic.fna ]]; then
			cp ${cdsFile} ${specFolder}/${label}/
			echo "${label} setup from GCA."
			weGotIt=${true}
			break
		fi
	done
	if ! ((weGotIt)); then
		for file in $(find ${unzipFolder}/${label}/ncbi_dataset/data/GCF_*/ -mindepth 1 -maxdepth 1); do
			if [[ "${cdsFile}" == *cds_from_genomic.fna ]]; then
				cp ${cdsFile} ${specFolder}/${label}/
				echo "${label} setup from GCF."
				weGotIt=${true}
				break
			fi
		done
	fi
	
	if ! ((weGotIt)); then
		echo "${label} did not locate a cds_from_genomic"
	fi
done
