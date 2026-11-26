#!/bin/bash
# ./bat.sh SEED 'TAG|json' 'TAG|json' ...  -> pp.txt (각 600판, 새 고수)
cd /home/claude/eval/ai/r5; S=$1; shift
B='"base":"ultimate"'
for x in "$@"; do t=${x%%|*}; j=${x#*|}; ./pp.sh "$t" "{$B${j:+,$j}}" 600 $S; done
