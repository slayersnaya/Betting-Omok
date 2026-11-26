#!/bin/bash
cd /home/claude/eval/ai/r4
B='"base":"ultimate","pfF":1,"types":[-2,-3,-4]'
./p.sh lam55 "{$B,\"lamK\":0.55}" 600 600
./p.sh dPre45 "{$B,\"dPre\":45}" 600 600
./p.sh L55D45 "{$B,\"lamK\":0.55,\"dPre\":45}" 600 0
./p.sh pfF4 "{$B}" 600 600
