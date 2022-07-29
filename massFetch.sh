#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

python massFetch.py > massFetch.txt
readarray -d " " -t fetchAll < "massFetch.txt"
echo "Mass Fetch Beginnning..."
echo "Inputs: ${#fetchAll[@]}"
totalInputs="${#fetchAll[@]}"
countInputs="0"

for((i=$countInputs;i<=$totalInputs;++i)) do
   sh fetchInput.sh "${fetchAll[$i]}"
   sleep 30
done


