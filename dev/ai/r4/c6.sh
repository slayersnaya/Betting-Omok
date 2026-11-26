#!/bin/bash
cd /home/claude/eval/ai/r4
B='"base":"ultimate","pfF":1,"types":[-2,-3,-4]'
./sp.sh dPre45 "{$B,\"dPre\":45}" 200 5000
./p.sh dPre45 "{$B,\"dPre\":45}" 600 1200
./p.sh dPre60 "{$B,\"dPre\":60}" 600 0
