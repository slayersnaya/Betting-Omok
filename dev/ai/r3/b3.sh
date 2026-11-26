#!/bin/bash
cd /home/claude/eval/ai/r3
B='"base":"ultimate","types":[-2,-3,-4],"pfF":1'
./p.sh dk5 "{$B,\"dk\":5,\"dS\":12}"
./p.sh iwo5 "{$B,\"insWo\":0.5}"
./p.sh dk5s "{$B,\"dk\":5,\"dS\":12,\"smooth\":0}"
