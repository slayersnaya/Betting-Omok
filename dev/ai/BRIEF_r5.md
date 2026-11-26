# Ultimate 학습 완료 + 고수 보완 함께 — 작업 지시서 (AI 엔지니어)
진행 기록 /home/claude/eval/ai/PROGRESS.md 이어서 갱신(끊길 수 있음). 먼저 PROGRESS.md 끝까지 읽기.

## 사용자 지시
"Ultimate는 학습 완료하고 업데이트." → 고수 보완안(pro_fix.diff: brCrit + brP 0.7, 고수>초보 77→86.8%, 고수>중수 88%)을 넣은 '새 고수'를 기준으로, Ultimate가 그 새 고수에게도 95% 이상 이기도록 Ultimate를 더 강화해서 둘을 함께 낼 것. (현재: pro_fix 적용 시 Ultimate>새 고수 94.1%(1200판))
- 리그(league/) 틀과 지금까지의 도구(r4/p.sh, q.sh, sp.sh, ladder/ld.sh 등)를 활용.

## 통과 기준(모두)
1. 새 Ultimate > 새 고수(pro_fix 적용) ≥95% (1200판 이상, seed 여러 개, 자리 바꿔)
2. 실제 기록 replay 16/16
3. 새 Ultimate vs 현재 서비스 Ultimate(S40np60) 자기대국 ≥50% (600판)
4. 사람형 봇 4종 현재 서비스 Ultimate보다 나빠지지 않기(각 200판, 같은 seed)
5. 사다리: 중수>초보 ≈87~89%, 새 고수>중수 ≈84~90%, 새 고수>초보 ≥85%
6. p99 계산 시간 현 수준(지정+입찰 p99 대략 120ms 이내, 이 서버 기준)
- 원칙: AI는 대국 중 사람 베팅·점수 안 봄(공개 정보+자기 정보만), 카운팅은 공개 정보로 범위 추정만, 게임 규칙 불변.
- 못 맞추면 가장 나은 조합과 숫자를 정직하게. 숫자 지어내지 말 것.

## 규칙
- 서비스 파일 수정 금지(/home/claude/betting-omok, /home/claude/web, /home/claude/gh-betting-omok), 배포·git 금지. CPU 2개를 다른 팀(상점 팀)과 나눠 씀 — 명령 하나 10분 이내.
- 기준 파일: 현재 /home/claude/betting-omok/index.html(이미 ulti_r2 적용, 랭크 점검 플래그 등 다른 변경 있음). AI 구간만 바꾸는 diff로.

## 결과물
1. /home/claude/eval/ai/ulti_r3.diff (현재 원본 기준, AI 구간만, pro_fix 포함) + 적용 확인
2. /home/claude/eval/ai/ulti_r3.md (기준별 숫자·판 수·한계)
3. 마지막 응답 10줄 이내
