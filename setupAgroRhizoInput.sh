#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

specFolder="input/RhizobiumAgrobacterium_Group"
importFolder="../AgroRhizoGroup/"

echo "Beginning moving of AgroRhizo Input."

for file in $(find ${importFolder} -mindepth 1 -maxdepth 1); do
	zipLabel="${file##*/}"
	label="${zipLabel%%.zip*}"

	unzip ${file} -d ${importFolder}/${label}
	
	if [[ -f ${label}/ncbi_dataset/data/GCA_*/cds_from_genomic.fna ]]; then
		codingSeqs=${label}/ncbi_dataset/data/GCA_*/cds_from_genomic.fna
		echo "${label} is being used from GCA."
	else if [[ -f ${label}/ncbi_dataset/data/GCF_*/cds_from_genomic.fna ]]; then
		codingSeqs=${label}/ncbi_dataset/data/GCA_*/cds_from_genomic.fna
		echo "${label} is being used from GCF."
	fi
	
	mkdir ${specFolder}/${label}
	cp ${codingSeqs} ${specFolder}/${label}/
	
	
done

