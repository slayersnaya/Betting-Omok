#!/bin/bash
cd /home/claude/eval/ai/r5
./bat.sh 1200 'dT6|"dThreat":0.6' 'BASE|'
./sp.sh dT6 '{"base":"ultimate","dThreat":0.6}' 200 5000
