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

	unzip ${file} -d ${unzipFolder}/${label}
done
