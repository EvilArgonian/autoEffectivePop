#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

specFolder="input/RhizobiumAgrobacterium_Group"
importFolder="../AgroRhizoGroup/"

echo "Beginning moving of AgroRhizo Input."

for file in $(find ${importFolder} -mindepth 1 -maxdepth 1); do
	label="${file##*/}"

	unzip ${file} -d ${label}
	codingSeqs=${label}/ncbi_dataset/data/GCA_*/cds_from_genomic.fna
	mkdir ${specFolder}/${label}
	cp ${codingSeqs} ${specFolder}/${label}/
	
	echo "${label} had been set up."
done

