#!/bin/bash
# 사다리(현 서비스 레벨): ladder/ld.txt
cd /home/claude/eval/ai/r4; O=../ladder/ld.txt
SEED=0 OUT=$O TAG="[cur]" LOG=../ladder/lg_pb.json node run.js 400 "ai:pro~ai:beginner" 2 >/dev/null
SEED=0 OUT=$O TAG="[cur]" node run.js 300 "ai:mid~ai:beginner,ai:pro~ai:mid" 2 >/dev/null
