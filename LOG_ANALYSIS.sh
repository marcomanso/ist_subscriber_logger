#!/bin/bash
DIR=$1

for filename in $DIR/*.*; do
   echo "--process $filename"
   python log_analyser.py --input $filename
done
