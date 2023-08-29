#!/bin/bash
DIR=$1
for filename in $DIR/*.log; do
  echo "--process $filename"
  python log_fixer.py --input $filename  --output $filename"_fixed"
done

