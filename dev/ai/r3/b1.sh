#!/bin/bash
cd /home/claude/eval/ai/r3
B='"base":"ultimate","types":[-2,-3,-4],"pfF":1'
./p.sh iwo3 "{$B,\"insWo\":0.3}"
./p.sh ins1 "{$B,\"ins\":1.0}"
./p.sh lam55 "{$B,\"lamK\":0.55}"
./p.sh resv3 "{$B,\"resv\":0.3}"
