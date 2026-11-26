#!/bin/bash
cd /home/claude/eval/ai/r5
J='{"base":"ultimate","dThreat":0.6,"opK":1.3}'
./sp.sh dT6o13 "$J" 200 7000
./sp.sh dT6o13 "$J" 200 9000
./pp.sh dT6o13 "$J" 600 1800
