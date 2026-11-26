#!/bin/bash
cd /home/claude/eval/ai/r4
B='"base":"ultimate","pfF":1,"types":[-2,-3,-4]'
./q.sh pfR2 "{$B,\"pfR\":0.2}" 100
./p.sh pfR2 "{$B,\"pfR\":0.2}" 600 1200
./p.sh pfR3 "{$B,\"pfR\":0.3}" 600 0
