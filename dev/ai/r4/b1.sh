#!/bin/bash
cd /home/claude/eval/ai/r4
B='"base":"ultimate","types":[-2,-3,-4],"pfF":1'
./p.sh i10a0 "{$B,\"ins\":1.0,\"insAdd\":0}"
./p.sh ia0 "{$B,\"insAdd\":0}"
./p.sh i115a2 "{$B,\"ins\":1.15,\"insAdd\":2}"
