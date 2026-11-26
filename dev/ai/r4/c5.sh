#!/bin/bash
cd /home/claude/eval/ai/r4; export AIF=ai_r5.js
B='"base":"ultimate","pfF":1,"types":[-2,-3,-4]'
./p.sh lamU5 "{$B,\"lamU\":0.5}" 600 0
./p.sh lamU10 "{$B,\"lamU\":1}" 600 0
