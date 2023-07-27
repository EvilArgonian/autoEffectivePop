#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

specFolder="input/RhizobiumAgrobacterium_Group"
importFolder="../AgroRhizoGroup"
unzipFolder="../UnzipAgroRhizoGroup"

echo "Beginning moving of AgroRhizo Input."

for file in $(find ${importFolder} -mindepth 1 -maxdepth 1); do
	zipLabel="${file##*/}"
	label="${zipLabel%%.zip*}"

	mkdir ${specFolder}/${label}
	
	if [[ -f ${unzipFolder}/${label}/ncbi_dataset/data/GCA_*/cds_from_genomic.fna ]]; then
		codingSeqs=${unzipFolder}/${label}/ncbi_dataset/data/GCA_*/cds_from_genomic.fna
		cp ${codingSeqs} ${specFolder}/${label}/
		echo "${label} setup from GCA."
	elif [[ -f ${unzipFolder}/${label}/ncbi_dataset/data/GCF_*/cds_from_genomic.fna ]]; then
		codingSeqs=${unzipFolder}/${label}/ncbi_dataset/data/GCA_*/cds_from_genomic.fna
		cp ${codingSeqs} ${specFolder}/${label}/
		echo "${label} setup from GCF."
	fi
done
