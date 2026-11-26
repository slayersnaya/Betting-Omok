#!/bin/bash
cd /home/claude/eval/ai/r5
export AIF=ai_u3.js
./bat.sh 1800 'u3rv8|"resv":0.8' 'u3lam55|"lamK":0.55' > bN1.log 2>&1 &
./bat.sh 1800 'u3rvU3|"resvU":0.3' 'u3rvD|"resvD":1,"resvU":0' > bN2.log 2>&1 &
wait
