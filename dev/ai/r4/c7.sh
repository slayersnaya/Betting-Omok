#!/bin/bash
cd /home/claude/eval/ai/r4
B='"base":"ultimate","pfF":1,"types":[-2,-3,-4]'
./sp.sh S40np60 "{$B,\"S\":40,\"np\":60}" 200 5000
./p.sh pfF4 "{$B}" 600 1200
./p.sh S40np60 "{$B,\"S\":40,\"np\":60}" 600 600
