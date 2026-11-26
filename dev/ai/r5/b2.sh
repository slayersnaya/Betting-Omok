#!/bin/bash
cd /home/claude/eval/ai/r4
B='"base":"ultimate","types":[-2,-3,-4],"pfF":1'
./p.sh pfR1 "{$B,\"pfR\":0.1}"
./p.sh pfR2 "{$B,\"pfR\":0.2}"
./p.sh pfR2f3 "{$B,\"pfR\":0.2,\"pfRf\":0.3}"
