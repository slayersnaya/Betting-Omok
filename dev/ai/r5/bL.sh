#!/bin/bash
cd /home/claude/eval/ai/r5
export AIF=ai_u3.js
./bat.sh 1800 'u3S60np90|"S":60,"np":90' > bL1.log 2>&1 &
./bat.sh 1800 'u3force15|"force":1.5' > bL2.log 2>&1 &
wait
