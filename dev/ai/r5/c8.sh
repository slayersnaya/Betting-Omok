#!/bin/bash
cd /home/claude/eval/ai/r4
B='"base":"ultimate","pfF":1,"types":[-2,-3,-4],"S":40,"np":60'
./p.sh S40np60 "{$B}" 600 1200
./sp.sh S40np60 "{$B}" 200 7000
./rb.sh S40np60 "{$B}" 100 0
