#!/bin/bash
cd /home/claude/eval/ai/r4
./bias.sh T0 '{"base":"ultimate","pfF":1,"types":[-2,-3,-4]}'
./bias.sh T1 '{"base":"ultimate","pfF":1,"types":[-2,-3,-4,0.6,0.8]}'
./bias.sh T2 '{"base":"ultimate","pfF":1,"types":[-2,-3,-4,-2,-4]}'
./bias.sh T3 '{"base":"ultimate","pfF":1,"types":[-2,-3,-4,0.8,1.2,-2,-4]}'
