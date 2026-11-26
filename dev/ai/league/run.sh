#!/bin/bash
# 리그 학습 실행: ./league/run.sh [세대 수=1]
#  - 한 세대 = node 한 번(약 3~5분, 10분 제한 안). 상태(league/state.json)가 남아 있으면 이어서 진행.
#  - 처음부터 다시: rm league/state.json league/gens.jsonl
#  - 시작 매개변수: SEED0='{"lamK":0.5}' (없으면 r3/ai_r3.js 의 ultimate + types[-2,-3,-4] + pfF)
#  - 판 수 조절: POP(후보 수,6) RR(쌍당,16) GA(현 Ultimate 상대,40) GP(고수 상대,60) GB(봇 상대, 0=끔)
cd /home/claude/eval/ai
N=${1:-1}
for ((i=0;i<N;i++)); do
  timeout 590 node league/league.js gen | tee -a league/run.log || { echo "세대 실패/시간 초과"; exit 1; }
done
node league/league.js show
