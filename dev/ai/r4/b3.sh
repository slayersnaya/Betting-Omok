#!/bin/bash
cd /home/claude/eval/ai/r4
while pgrep -f b2.sh >/dev/null; do sleep 5; done
B='"base":"ultimate","pfF":1'
./p.sh ty68 "{$B,\"types\":[-2,-3,-4,0.6,0.8]}"
./p.sh ty8 "{$B,\"types\":[-2,-3,-4,0.8]}"
