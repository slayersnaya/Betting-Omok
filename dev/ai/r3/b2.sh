#!/bin/bash
cd /home/claude/eval/ai/r3
B='"base":"ultimate","types":[-2,-3,-4],"pfF":1'
./p.sh tempo7 "{$B,\"tempo\":0.7}"
./p.sh dthr5 "{$B,\"dThreat\":0.5}"
./p.sh force2 "{$B,\"force\":2}"
./p.sh dtReal "{$B,\"dtReal\":1}"
