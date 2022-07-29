#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

divideInto=10 # Number of unique runs to divide into

rm -rf dividedInput/*
for i in {1..$divideInto}; do
	touch dividedInput/division_${i}.txt
done

# Lazy fix for apparent extra file created
rm dividedInput/division_\{1..${divideInto}\}.txt

totalCounter=0
counter=1
for file in $(find input/ -mindepth 1 -maxdepth 1 -type d); do
	echo "${file}" >> dividedInput/division_${counter}
	counter=$(( counter+1 ))
	totalCounter=$(( totalCounter+1 ))
	if ((counter > divideInto)); then
		counter=1
		echo "${totalCounter} inputs assorted"
	fi
done
