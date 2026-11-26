#!/bin/bash
cd /home/claude/eval/ai/r4
B='"base":"ultimate","pfF":1'
./p.sh tyR2 "{$B,\"types\":[-2,-3,-4,0.6,0.8],\"pfR\":0.2}"
./p.sh pfR2 "{$B,\"types\":[-2,-3,-4],\"pfR\":0.2}" 600 600
./p.sh ty68 "{$B,\"types\":[-2,-3,-4,0.6,0.8]}" 600 600
./p.sh tyR2 "{$B,\"types\":[-2,-3,-4,0.6,0.8],\"pfR\":0.2}" 600 600
