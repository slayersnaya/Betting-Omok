# 베팅 오목 음향팀 회의록 (2차)

- 일시: 2026-11-26 (1차 회의 같은 날 오후)
- 안건: 사용자 피드백 "4개면 돼? 모든 버튼·동전 소리까지 전부" → 실제 코드 전수 조사, 소리 설계 원칙, 최종 파일 목록과 프롬프트 전부, 만드는 순서
- 참석(역할): 사운드 디자이너(효과음) · 게임 오디오 기획(목록·우선순위·라이선스·개발 연결) · 작곡가(배경음·징글) · UX 담당(볼륨·피로도·심리전 보호)
- 기준: 담당자 4명 모두 95점 이상일 때 확정
- 조사 대상: `/home/claude/betting-omok/index.html` (읽기만 함, 수정 안 함). **회의 중에 개발팀이 같은 파일에 합성음 효과음(`SND`, `snd()`)을 넣고 있어서** 그 결과(2026-11-26 11:18 기준)까지 반영함. 줄 번호는 계속 바뀌므로 함수·액션 이름으로만 적음.
- 함께 낸 파일: `/home/claude/eval/sound/sound_list.csv` (파일명·쓰는곳·액션·길이·음량·우선순위·도구·프롬프트·설정, 엑셀에서 바로 열림)

---

## 0. 한눈에 보기

| 항목 | 숫자 |
|---|---|
| 소리가 날 수 있는 순간(전수 조사) | **250개** (게임·시스템 순간 100 + 버튼 data-act 130 + 설정 스위치 9 + 배경음 장면 11) |
| 실제로 만들 파일 | **43개** (배경음 6 · 징글 7 · 효과음 30) |
| 우선순위 | 1순위 20개 · 2순위 16개 · 3순위 7개 |
| 줄인 방법 | 같은 계열은 한 파일을 여러 곳에 쓰고, 피치(음 높이)·음량·반복 횟수만 바꿔서 구분 |
| 파일이 없을 때 | 개발팀이 넣은 합성음(`SND`)이 그대로 나옴 → 파일은 하나씩 들어오는 대로 바꿔 끼우면 됨 |

효과음 분류별 파일 수: UI 6 · 돌 5 · 칩 4 · 동전 2 · 타이머 2 · 연출 4 · 보상 2 · 상점 2 · 알림 1 · 랭크 2

---

## 1. 1차 대비 바뀐 점

| 1차 | 2차 |
|---|---|
| 우선순위 1을 Suno 4곡(배경음 2·징글 2) 중심으로 정리 | 코드 전수 조사로 **250개 순간**을 뽑고 **43개 파일**로 전부 덮음 |
| 효과음은 "어떤 도구로" 한 줄씩 | **모든 파일에 Suno Sounds 프롬프트 1개씩** + 대안 도구 프롬프트 1개씩 (Suno로 전부 시도 가능) |
| 함수·액션 연결 없음 | 순간마다 실제 함수·data-act 이름 + 개발팀 합성음 키(`SND.xxx`)와 1:1 연결 |
| 배경음 4장면 | 6곡이 11장면(로비·대국·긴장·결과·매칭·친구 대기·묘수·복기·튜토리얼·결산·가림)을 덮음 |
| 심리전 보호 3줄 | 10개 규칙. 동점 전용 소리 금지, +5·+10 칩 소리 통일 등 **코드에서 찾은 문제 2건** 포함 |
| 볼륨: 배경음 35%·효과음 70% | 파일마다 상대 dB 값, 5단계 볼륨 표, 덕킹(징글 때 배경음 줄이기) |
| 만드는 순서 8단계 | 하루 단위 6일 계획 + 분류별 고르는 기준 + 이름 규칙 |

---

## 2. 회의 전에 확인한 사실

### 2-1. 코드 조사 결과 (index.html)

- 소리 장치: `sndCtx()`(Web Audio), `snd(키)`로 재생. 설정 **효과음** 스위치 `setSnd` → 저장값 `bo-snd`(기본 켬), 진동 `setVib` → `bo-vib`. 첫 터치(`pointerdown`·`keydown`) 때 소리 장치를 깨움. 화면이 숨겨지면 소리 안 남(`document.hidden`).
- 버튼 기본음: 모든 `[data-act]` 클릭에 `SND_ACT[액션]` 또는 `tap`. 체크박스는 `toggleOn/Off`.
- 현재 합성음 키 44개: tap, soft, tab, open, close, toggleOn, toggleOff, pick, stone, chipUp, chipDown, chipStack, chipReset, over, seal, oppSeal, crack, coinFlip, coinLand, five, voidLine, win, lose, draw, tick, tickLate, timeout, turn, reward, coin1, stamp, buy, equip, error, notify, msg, match, pop, correct, wrong, tierUp, tierPiece, tierDown, page
- **아직 호출되지 않는 키(11:18 기준)**: pick(칸 탭), over(합계 초과), draw(무승부), timeout(시간 초과), notify(친구 알림), tierPiece(문양 조각), tierDown(강등) → 소리 목록에서는 연결 위치를 적어 둠
- **소리가 빠지는 경우**: 승패 소리는 `startReveal()` 안에서만 남 → 개봉 없이 끝나는 **기권·나감·부재승**, 그리고 **무승부(winner 없음)·관전자**는 지금 무음. 연결이 필요함
- **심리전 관련 발견**: `SND_ACT`에서 +1(`bp`)은 chipUp, **+5·+10(`b5`·`bq`)은 chipStack(3번 짤깍)**으로 소리가 다름 → 같은 방에서 하면 "크게 거는 중"이 소리로 들림. 같은 소리로 통일 권고
- 개봉 시간표: `RS=0.38`(칸 간격), `RL=0.57`(도장→돌), 개봉 화면 1.85초, 승패 화면 `WIN_T.sheet`=3.7초. 동전: 회전 1.75초 뒤 착지
- 이모트 12종(`EMO`): 안녕·최고·깜짝·메롱·덤벼·아쉽다·힘내·음…·하하·분해·고마워·박수

### 2-2. Suno·도구·라이선스 (웹 검색, 1차에서 확인)

| 항목 | 확인 내용 | 출처 |
|---|---|---|
| 연주곡 | Custom(Advanced) 모드에서 **Instrumental** 켜면 목소리 없는 곡 | [blakecrosley Suno 가이드](https://blakecrosley.com/guides/suno) |
| 스타일·제외 | Style 칸에 4~7개 묘사 권장, 빼고 싶은 건 고급 옵션 **Exclude** 칸. **글자 수 제한은 확인 못 함** | 같은 가이드 |
| 길이·편집 | v5는 최대 약 8분. Song Editor에 Extend·**Crop(자르기)**·Replace Section | [Suno 공식 v5](https://help.suno.com/en/articles/8105153), 같은 가이드 |
| 효과음 | **Suno Sounds(베타)**: Create → 위쪽 **Sounds**. One Shot / Loop 선택, BPM·Key 지정, 한 번에 2개 생성. **필요 요금제·최대 길이·크레딧 소모는 확인 못 함** | [Suno 공식 Suno Sounds](https://help.suno.com/en/articles/10625537) |
| 상업적 이용 | **Pro·Premier(·Platinum)로 만든 것만** 상업적 이용 가능(게임 포함). 무료로 만든 건 나중에 업그레이드해도 상업용 안 됨 | [Suno 공식 상업적 이용](https://help.suno.com/en/articles/2425345), [소유권](https://help.suno.com/en/articles/2416769), [유료 플랜](https://help.suno.com/en/articles/14617153) |
| Sounds 결과물 조건 | 일반 곡과 같은 조건일 것으로 보이나 **명시 문장은 못 찾음** | — |
| 다운로드 한도 | 2026년부터 월 다운로드 한도가 생긴다는 보도. 정확한 숫자는 출처마다 달라 **확인 못 함** → [가격 페이지](https://suno.com/pricing) 확인 | [dynamoi 정리](https://dynamoi.com/learn/ai-music-distribution/suno-commercial-rights-explained) |
| ElevenLabs | 무료 플랜 결과물은 상업 불가, 유료 플랜이면 게임에 사용 가능. 효과음만 따로 판매 금지 | [ElevenLabs 도움말](https://help.elevenlabs.io/hc/en-us/articles/13313564601361), [효과음 약관](https://elevenlabs.io/sound-effects-terms) |
| 무료 효과음 | Kenney는 CC0(표기 불필요). Freesound는 CC0·CC BY만(BY는 표기), CC BY-NC 금지 | [Cinevva 정리](https://app.cinevva.com/guides/free-sound-effects-music), [Kenney Interface Sounds](https://kenney.nl/assets/interface-sounds), [Kenney Casino Audio](https://kenney.nl/assets/casino-audio) |

**모르는 것**: 사용자의 Suno 요금제(무료면 게임에 못 씀), Suno Sounds 한 번에 드는 크레딧, Suno가 "4초"처럼 적은 길이를 지키는지, 루프 이음새가 매끄럽게 나오는지(그래서 자르는 방법을 9장에 적음).

---

## 3. 안 비교 → 결정

| 안 | 내용 | 장점 | 단점 |
|---|---|---|---|
| A. 순간마다 파일 | 250개 순간에 각각 파일 | 세밀함 | 수백 개 생성·관리, 소리 통일감 깨짐, 용량 큼 |
| B. 계열별 파일 + 변형 | **43개 파일**을 계열로 묶고 피치·음량·반복으로 구분, 파일 없으면 합성음 | 만들 양이 현실적, 같은 계열은 같은 질감, 하나씩 바꿔 끼우기 가능 | 변형 규칙을 개발팀이 지켜야 함(표로 해결) |
| C. 합성음만 | 지금 개발팀 합성음 유지 | 추가 작업 없음 | 바둑돌·도장·옥돌 같은 "진짜 물건 소리"는 합성음으로 한계, 배경음 없음 |

**결정: B안.** 근거: ① 250개 순간 중 대부분은 "버튼 열기/닫기/확인" 같은 반복 동작이라 6개 UI 파일로 충분 ② 게임의 얼굴인 돌·칩·도장·동전은 실제 물건 소리 파일로 품질을 올림 ③ 합성음이 이미 있어서 파일이 늦어져도 게임이 무음이 되지 않음.

**도구 결정**: 사용자가 Suno를 갖고 있으니 **모든 파일을 Suno(곡 또는 Sounds)로 먼저 시도** → 효과음이 마음에 안 들면 대안(직접 녹음 / Kenney 무료 / ElevenLabs 유료)으로. 특히 바둑돌·칩·동전·도장·옥돌은 녹음본과 꼭 비교.

**사운드 콘셉트(1차 유지)**: "조용한 옥(玉) 대국실" — 피아노 + 은은한 가야금·대금 + 부드러운 패드. 대국·긴장·매칭 배경음은 A minor, 로비·결과는 C major, 징글·알림 같은 음이 있는 효과음은 C major로 맞춰 겹쳐도 어울리게.

---

## 4. 소리 설계 원칙

### 4-1. 계열 묶기

| 계열 | 질감 | 파일 | 쓰는 곳 |
|---|---|---|---|
| UI 클릭 | 작고 부드러운 나무·종이 | ui_tap, ui_open, ui_close, ui_toggle, ui_confirm, ui_error | 버튼 130개 대부분, 토스트 오류 |
| 돌 | 단단한 돌+나무판 | stone_place_1~3, stone_tick, stone_void | 개봉, 세 칸 고르기, 6목, 복기, 묘수 |
| 칩·봉인 | 플라스틱 칩, 나무 상자, 밀랍 도장 | chip_click, chip_sweep, seal_lock, seal_break | 베팅, 봉인, 개봉 |
| 동전·타이머 | 금속, 나무 목탁 | coin_flip, coin_land, timer_tick, timer_out | 선 정하기, 남은 시간 |
| 연출·보상 | 맑은 종, 옥돌 | fx_chime, fx_sparkle, fx_myturn, reward_stamp, reward_gem, shop_buy, shop_equip, tier_snap, mm_found, notify, emote_pop | 오목, 정답, 보상, 상점, 승급, 알림 |
| 음악 | 피아노·가야금·패드 | bgm 6, jg 7 | 장면 배경음, 결과·티어 징글 |

### 4-2. 재사용과 변형 (파일 수 줄이기)

- **피치**: 같은 파일을 0.75~1.5배 속도로 재생(높낮이 변화). 예) 탭 이동 0.9, 끔 스위치 0.85, 장착 해제 0.85, 마지막 1초 1.25
- **음량**: 같은 파일을 작게. 예) 상대 봉인 완료 = seal_lock −16dB, 대화상자 취소 = ui_close −16dB
- **반복**: 한 파일을 여러 번 짧은 간격으로. 예) 지정 확정 = stone_tick 3번(0·60·120ms), 모두 받기 = reward_gem 3번(90ms), 오목 완성 = fx_chime 3번(도·미·솔 = 피치 1.0·1.26·1.5)
- **뒤집기**: ui_close는 ui_open을 Audacity에서 거꾸로 돌려 만듦(생성 1번 절약)
- **겹치기**: 오목 완성 = 돌 + 종, 출석 = 도장 + 옥돌
- **무작위 흔들기**: UI·돌·칩은 재생마다 피치 ±3% 무작위(같은 소리 반복 느낌 감소). 종·징글처럼 음이 있는 소리는 흔들지 않음

### 4-3. 심리전 보호 규칙 (필수)

1. 상대의 칩 조작(올림·내림·입력)은 **어떤 소리도 내지 않음**(코드 원칙과 같음)
2. 칩 소리는 **금액·버튼과 무관하게 같은 파일**. +1·+5·+10 모두 chip_click 1번 → 현재 `b5`·`bq`=chipStack은 chipUp과 같게 바꾸길 권고(대면 플레이 때 큰 베팅이 들림)
3. **동점 전용 소리 금지**: 동점이면 후 플레이어 돌이 놓이는데, 따로 소리를 내면 "상대가 나와 똑같이 걸었다"가 드러남
4. 칸마다 "이김·짐"이나 "큰 차이" 소리 금지. 돌 소리는 흑/백 피치 차이만(돌 색은 화면에도 보이는 정보)
5. 상대 봉인 완료는 허용(화면에도 "봉인" 표시). 단 턴당 1번, 작게, 금액과 무관
6. AI 상대 매칭도 사람과 **같은 mm_found**. AI "생각 중" 소리 없음(소리로 AI 티 안 나게)
7. 긴장 배경음은 **판 위 공개 정보(막히지 않은 4 등)만** 보고 켬. 칩 잔액·베팅은 절대 안 씀
8. 타이머 소리는 **내 차례에만**(상대가 얼마나 고민하는지 소리로 알 수 없게)
9. 봉인 화면의 내 칩 떨어지는 애니메이션(`drop2`)에는 칸마다 소리를 붙이지 않음
10. 개봉 소리 순서·간격은 양쪽 폰이 같음(이미 같은 연출 시간표)

### 4-4. 볼륨 단계 (0dB = 가장 큰 효과음 기준)

| 단계 | 상대 음량 | 소리 |
|---|---|---|
| 1 | 0 ~ −2dB | stone_place, reward_stamp, 징글(−1~−5) |
| 2 | −3 ~ −4dB | seal_break, seal_lock, coin_land, timer_out, mm_found |
| 3 | −6 ~ −8dB | fx_chime, coin_flip, reward_gem, shop_buy, stone_void, fx_myturn, notify, timer_tick, tier_snap |
| 4 | −10 ~ −12dB | chip_click, chip_sweep, ui_confirm, ui_error, fx_sparkle, shop_equip, emote_pop, stone_tick |
| 5 | −14 ~ −16dB | ui_tap, ui_open, ui_close, ui_toggle |
| BGM | −18 ~ −22dB | 배경음 6곡. 징글이 나오는 동안 −8dB 더 줄였다가 1초에 걸쳐 복귀(덕킹) |

### 4-5. 반복 피로도

- 돌 소리 3개 번갈아 + 피치 흔들기 → 한 턴 3번이 기계음처럼 안 들림
- 칩: 길게 누르기 반복은 220ms에 1번까지만. 같은 파일은 50ms 안에 다시 안 냄(겹침 방지), 동시에 최대 8개
- 타이머: 10초에 1번, 5초부터만 매초. 알림: 3초에 1번까지
- 배경음: 로비·대국 곡은 60초 이상 루프(짧으면 금방 질림). 대국이 15분 넘게 이어지면 bgm_game −3dB(선택 사항)
- 끌기·슬라이더처럼 빠른 연속 동작은 −16dB + 80~100ms 간격 제한

---

## 5. 점수 (2차: 1회 검토 → 수정 → 최종)

### 2차 첫 검토

| 담당 | 점수 | 지적 |
|---|---|---|
| 사운드 디자이너 | 87 | 첫 안은 58개 파일. 열기·창·시트·프로필을 따로 만들어 비슷한 소리가 많았음 → 계열 통합 필요 |
| 게임 오디오 기획 | 85 | 순간 목록에 함수 이름은 있으나 개발팀 합성음 키와 연결이 없어 "어느 소리를 어느 파일로 바꾸는지" 불분명. 무승부·기권처럼 지금 소리가 빠지는 경우를 안 짚음 |
| 작곡가 | 89 | 결과 화면·친구 대기·복기 장면 배경음 누락. 징글끼리 조가 섞임 |
| UX 담당 | 86 | **동점 때 소리를 따로 내면 상대 금액이 드러남.** 코드의 +5·+10 칩 소리 차이도 미지적. 볼륨이 % 두 개뿐 |

### 수정한 내용

1. 58개 → **43개**: 열기 계열은 ui_open 하나 + 피치, ui_close는 뒤집기, 오목 완성은 돌+종 겹치기로 전용 파일 없앰, 개봉 바람 소리(whoosh)는 도장 깨짐과 겹쳐 빼기
2. 순간 표와 파일 표에 **현재 SND 키** 열 추가, 아직 안 불리는 키 7개와 무음 구간(무승부·기권·나감·부재승·관전자) 명시
3. bgm_result 추가, 친구 대기=bgm_match·복기=bgm_puzzle 재사용, 징글·음이 있는 효과음 조 통일(C major / A minor)
4. 심리전 규칙 10개로 확대(동점 소리 금지, 칩 소리 통일, AI 매칭 동일, 타이머 내 차례만 등), 5단계 볼륨표와 덕킹 규칙

### 최종 점수

| 담당 | 점수 | 95점 이상 근거 |
|---|---|---|
| 사운드 디자이너 | 96 | 250개 순간을 43개 파일로 빠짐없이 덮음(버튼 130개 모두 매핑 검증), 계열별 질감 통일, 파일마다 Suno Sounds 프롬프트 + 대안 프롬프트 |
| 게임 오디오 기획 | 96 | 모든 순간에 함수·data-act·SND 키 연결 → 개발팀이 키→파일만 바꾸면 됨. 우선순위 1만 넣어도 대국 한 판 전체가 소리 남. 하루 단위 계획, 라이선스 기록 규칙 |
| 작곡가 | 95 | 배경음 6곡이 11장면 덮음, 조 통일로 크로스페이드·겹침 자연스러움, 곡마다 마디 단위 자르기 길이까지 계산 |
| UX 담당 | 97 | 코드에서 정보가 새는 지점 2건 찾아 규칙화, 5단계 볼륨·덕킹·간격 제한·피치 흔들기로 피로도 관리, 진동·첫 터치·숨김 처리 정리 |

---

## 6. 전수 조사: 소리가 날 수 있는 순간 250개

표기: "현재 SND"는 개발팀 합성음 키(없으면 지금 무음). 파일 이름의 `.mp3`는 생략.

### 6-1. 게임 진행·시스템 순간 (100개)

| # | 영역 | 순간 | 연결 위치(함수·조건) | 현재 SND | 파일 | 재생 방법 |
|---|---|---|---|---|---|---|
| 1 | 동전 | 튀기기+회전 시작 | `showCoin() — firstBy=coin, 움직임 줄이기 아님` | coinFlip | sfx_coin_flip | 0초 |
| 2 | 동전 | 착지 | `showCoin() setTimeout 1750ms` | coinLand | sfx_coin_land | 1.75초 |
| 3 | 동전 | 결과 글자(선 플레이어 ○○) | `showCoin() 1950ms #ctext` | 없음 | sfx_fx_myturn / 무음 | 내가 선이면 myturn, 아니면 무음 |
| 4 | 동전 | 지난 판 진 쪽이 먼저(동전 안 돌림) | `showCoin() loser 분기` | coinLand | sfx_coin_land | 바로 |
| 5 | 동전 | 움직임 줄이기 설정 | `showCoin() prefers-reduced-motion` | coinLand | sfx_coin_land | 바로 |
| 6 | 세 칸 지정 | 내 차례 알림(세 칸 고르기) | `showMyTurn(vs,"세 칸 고르기") + vibrate 25ms` | turn | sfx_fx_myturn | 개봉 연출 끝난 뒤 |
| 7 | 세 칸 지정 | 칸 탭(선택·옮김) | `onCellTap() → setSel()` | 없음(pick 미연결) | sfx_stone_tick | 기본 |
| 8 | 세 칸 지정 | 빈칸 아님 | `onCellTap() toast "빈칸만 가능"` | 없음 | sfx_ui_error | -14dB |
| 9 | 세 칸 지정 | 세 칸 불가 자리 | `onCellTap() toast "여기선 세 칸 불가"` | 없음 | sfx_ui_error | -14dB |
| 10 | 세 칸 지정 | 방향만 골랐는데 둘 곳 없음 | `data-act=dir toast "그 방향은 둘 곳 없음"` | tap | sfx_ui_error | -14dB(탭음 대신) |
| 11 | 세 칸 지정 | 끌어서 세 칸 옮기기 | `#board pointerdown 드래그 → setSel` | 없음 | sfx_stone_tick | -16dB, 같은 칸이면 무음, 80ms 간격 제한 |
| 12 | 세 칸 지정 | 지정 확정 | `data-act=dconfirm → T.designated / L.startBet / wmine("c")` | stone | sfx_stone_tick ×3 | 0/60/120ms 피치 1.0/1.06/1.12 (돌 소리는 개봉 때만) |
| 13 | 세 칸 지정 | 이미 확정됨/시간 초과로 거절 | `dconfirm toast "이미 확정됨"·"시간 초과"` | stone | sfx_ui_error | -12dB |
| 14 | 세 칸 지정 | 시간 초과 자동 지정 | `L.startBet() 앞 toast("시간 초과 · 세 칸 자동") / 온라인 cl.sd` | 없음(timeout 미연결) | sfx_timer_out | 기본 |
| 15 | 세 칸 지정 | 선택 취소 | `현재 코드에 별도 "취소" 액션 없음(다른 칸 탭=옮김)` | — | (생기면) sfx_stone_tick | 피치 0.85 |
| 16 | 베팅 | 내 차례 알림(베팅) | `showMyTurn(vs,"베팅")` | turn | sfx_fx_myturn | 기본 |
| 17 | 베팅 | 칸(A·B·C) 고르기 | `data-act=bcol / #bi0~2 focusin` | soft | sfx_ui_tap | 피치 0.75 -16dB |
| 18 | 베팅 | 직접 숫자 입력 | `#bi input 이벤트` | 없음 | 무음 | 키보드 소리와 겹침 |
| 19 | 베팅 | 합계 초과(남은 칩 음수가 처음 될 때) | `updateBetSum() left<0` | 없음(over 미연결) | sfx_ui_error | -12dB, 초과 상태로 바뀔 때 1번 |
| 20 | 베팅 | 길게 눌러 연속 변경 | `pointerdown 반복 110ms` | chipUp 등 | sfx_chip_click | 220ms에 1번까지만 |
| 21 | 베팅 | 봉인 직후 600ms 이중 탭 무시 | `data-t0 검사` | — | 무음 | — |
| 22 | 베팅 | 상대 봉인 완료 | `renderPlayers() oppStatus=봉인(UI.oppSealK 턴당 1번)` | oppSeal | sfx_seal_lock | 피치 1.25 -16dB |
| 23 | 베팅 | 상대가 칩 올림/내림/입력 | `(상대 쪽 조작)` | — | **금지·무음** | 심리전 보호 |
| 24 | 베팅 | 시간 초과 자동 봉인(칸마다 1칩) | `renderPanel() waitBox("시간 초과 · 칸마다 1") / cl.sb` | 없음 | sfx_timer_out | 기본 |
| 25 | 베팅 | "개봉 전 닫지 마세요" 안내 | `bsubmit !LS_OK toast` | — | 무음 | — |
| 26 | 개봉 | A칸 도장 깨짐 | `startReveal() i=0, 0초` | crack | sfx_seal_break | 피치 1.0 |
| 27 | 개봉 | A칸 돌 착지 | `startReveal() 0.57초 + vibrate 15ms` | stone | sfx_stone_place_1 | 흑 0.97/백 1.03 |
| 28 | 개봉 | B칸 도장 깨짐 | `0.38초` | crack | sfx_seal_break | 피치 1.04 |
| 29 | 개봉 | B칸 돌 착지 | `0.95초` | stone | sfx_stone_place_2 | 흑/백 피치 |
| 30 | 개봉 | C칸 도장 깨짐 | `0.76초` | crack | sfx_seal_break | 피치 1.08 |
| 31 | 개봉 | C칸 돌 착지 | `1.33초` | stone | sfx_stone_place_3 | 흑/백 피치 |
| 32 | 개봉 | 카드 눌러 연출 건너뛰기 | `.rvcards click(capture) → UI.rv.until=now` | — | 남은 예약 소리 취소 + stone 1번 | 예약한 setTimeout 정리 필요 |
| 33 | 개봉 | 동점 → 후 플레이어 돌 | `settle() sunB==huB → hu` | — | **전용 소리 금지** | 동점 소리=상대 금액 노출 |
| 34 | 개봉 | 내 돌/상대 돌 | `h.win[i]` | — | 같은 돌 소리 | 이김·짐 따로 소리 X(흑백 피치만) |
| 35 | 판정 | 오목 완성(정확히 5) | `startReveal() over: (3·RS+RL)+0.25초` | five | stone_place_1 + sfx_fx_chime×3 | 돌 뒤 80ms부터 아르페지오 |
| 36 | 판정 | 동시 오목 | `end(...,"동시 오목")` | five | 오목 완성과 같음 | — |
| 37 | 판정 | 6목 이상 빨간 줄 | `renderBoard() overs → OVSEEN 처음(60ms 뒤)` | voidLine | sfx_stone_void | 같은 줄은 한 번만 |
| 38 | 종료 | 승리 | `startReveal() WIN_T.sheet 3.7초, winner===me` | win | jg_win → bgm_result | BGM -8dB 덕킹 |
| 39 | 종료 | 패배 | `같은 위치 winner!==me` | lose | jg_lose → bgm_result | 덕킹 |
| 40 | 종료 | 무승부(둘 곳 없음·최대 턴·둘 다 시간 초과) | `startReveal() winner==null — 지금은 소리 없음` | 없음 | jg_draw | **연결 필요** |
| 41 | 종료 | 무효(확인 불일치) | `end(null,"확인 불일치")` | 없음 | jg_draw | 연결 필요 |
| 42 | 종료 | 기권승·상대 나감·부재승 | `reason 기권/나감/상대 부재 — 판(hist)이 안 바뀌어 startReveal을 안 거침` | 없음 | jg_win | -3dB, **연결 필요** |
| 43 | 종료 | 기권패(내가 기권) | `data-act=resign → dlgok → L.resign / wmine("resign")` | 없음 | jg_lose | 연결 필요 |
| 44 | 종료 | 시간 초과 3회 패/승 | `resolve end "시간 초과 3회"(개봉 거침)` | win/lose | jg_win / jg_lose | — |
| 45 | 종료 | 봉인 불일치·지정 변경·잘못된 지정 | `resolve end(...)` | 상황따라 | jg_win / jg_lose | 이유와 무관하게 승패로 |
| 46 | 종료 | 관전자에게 끝난 판 | `startReveal() vs.spect / vs.me 없음 — 지금은 무음` | 없음 | jg_draw | -6dB 중립 |
| 47 | 종료 | 부재승 신청 결과 | `claimAbs() 성공` | 없음 | jg_win | -3dB |
| 48 | 종료 | 상대도 다시 하기 → 새 판 입장 | `effects() m.next → enterGame` | 없음 | sfx_notify | -6dB |
| 49 | 종료 | 랭크 점수·티어 변화 줄 | `tierMove() 결과 줄 표시` | 없음 | (아래 승급/강등) | — |
| 50 | 타이머 | 10초 남음 | `renderTimer() ck.left===10 (say)` | 없음 | sfx_timer_tick | 피치 0.8 -12dB + 진동 30ms |
| 51 | 타이머 | 5·4·3·2초 | `renderTimer() late` | tick | sfx_timer_tick | 기본, 내 차례만 |
| 52 | 타이머 | 1초 | `renderTimer() ck.left===1` | tickLate | sfx_timer_tick | 피치 1.25 -5dB + 진동 20ms |
| 53 | 타이머 | 내 시간 끝 | `renderTimer() ck.left<=0 처음 / toast("시간 초과")` | 없음 | sfx_timer_out | 1번 |
| 54 | 타이머 | 상대 시간 | `(상대 차례 링은 안 보임)` | — | 무음 | 상대 고민 길이 노출 방지 |
| 55 | 랭크 | 매칭 시작 | `data-act=mm → mmStart() 성공` | tap | sfx_ui_confirm + bgm_match | BGM 1초 페이드인 |
| 56 | 랭크 | 매칭 취소 | `mm(MM.on) → mmStop() / local·solo 중 "랭크 매칭 취소됨"` | tap | sfx_ui_close | bgm_match 페이드아웃 |
| 57 | 랭크 | 상대 찾음(사람) | `mmHost() → enterGame` | match | sfx_mm_found | — |
| 58 | 랭크 | 상대 찾음(AI) | `mmBot()` | match | sfx_mm_found | 사람과 똑같이 |
| 59 | 랭크 | 상대 미입장 · 다시 찾는 중 | `effects() 20초 → toast` | 없음 | sfx_ui_error | -12dB |
| 60 | 랭크 | 점검 중 / 이용 불가 / 연결 확인 중 | `mmStart() 앞부분 dialog·toast` | 없음 | sfx_ui_error | -12dB |
| 61 | 랭크 | 랭크 잠김 안내 | `rankLockDlg()` | 없음 | sfx_ui_open | — |
| 62 | 랭크 | 랭크 처음 열림 | `rankIntro()` | 없음 | jg_tier_up | -8dB |
| 63 | 랭크 | 승급·배치 완료 등장 | `tierUp() → tupShow() s0 0.35/0.55초` | tierUp | jg_tier_up | BGM 덕킹 |
| 64 | 랭크 | 문양 조각 단계별 | `tupShow() data-st 1..n, 간격 g 0.13~0.18초` | 없음(tierPiece 미연결) | sfx_tier_snap | 단계 k 피치 1+0.06k |
| 65 | 랭크 | 문양 완성 번쩍 | `tupShow() fin 시점` | 없음 | sfx_fx_sparkle | — |
| 66 | 랭크 | 마스터·챌린저 | `tupShow() top / chalPop()` | tierUp | jg_tier_top | jg_tier_up 대신 |
| 67 | 랭크 | 연출 건너뛰기 | `tupShow() skip()` | — | 남은 snap 취소 → sparkle 바로 | — |
| 68 | 랭크 | 강등 | `tierMove() up=false` | 없음(tierDown 미연결) | jg_tier_down | — |
| 69 | 랭크 | 시즌 결산 | `recapShow()` | 없음 | jg_season → bgm_result | — |
| 70 | 보상 | 출석 도장(자동) | `attAuto() → attStamp() → attShow(at>0)` | stamp+reward | sfx_reward_stamp → 0.35초 뒤 sfx_reward_gem | — |
| 71 | 보상 | 7·14·21·28일째 | `attAmt(k) 50~120` | stamp+reward | stamp + gem×3 + sparkle | — |
| 72 | 보상 | 과제 완료 | `ecoMisClaim() add>0` | 없음 | sfx_fx_chime | -8dB |
| 73 | 보상 | 업적 달성 | `ecoAch()` | 없음 | sfx_fx_chime + sparkle | -6dB |
| 74 | 보상 | 받기 실패 | `ecoClaim() false / attFail` | 없음 | sfx_ui_error | -12dB |
| 75 | 상점 | 옥돌 부족 | `ecoItemTap() need>0 dialog` | 없음 | sfx_ui_error | 창 소리 대신 |
| 76 | 상점 | 지갑 불러오는 중 | `ecoItemTap() !ECO.ok` | 없음 | sfx_ui_open | — |
| 77 | 상점 | 구매 성공/실패 | `ecoBuy() ok / "사지 못했어요"` | buy / error | sfx_shop_buy / sfx_ui_error | — |
| 78 | 상점 | 장착/해제 | `ecoEquip(c,id) / id=""` | equip / soft | sfx_shop_equip | 해제 피치 0.85 |
| 79 | 상점 | 닉네임 변경(유료) | `nickCommit() chg && 성공` | 없음 | sfx_shop_buy | 첫 변경 무료면 ui_confirm |
| 80 | 상점 | 닉네임 오류(옥돌 부족·중복) | `nickCommit() err` | 없음 | sfx_ui_error | — |
| 81 | 친구 | 친구 요청 받음 | `frChanged() "친구 요청을 보냈어요"` | 없음 | sfx_notify | — |
| 82 | 친구 | 친구 됨 | `frChanged() "친구가 됐어요"` | 없음 | sfx_notify | — |
| 83 | 친구 | 메시지 받음 | `frChanged() 새 메시지(채팅 보는 중 제외)` | msg | sfx_notify | 피치 1.25 -6dB, 3초에 1번 |
| 84 | 친구 | 메시지 보냄 | `#chForm submit → frSend() true` | 없음 | sfx_ui_open | 피치 1.3 -8dB |
| 85 | 친구 | 메시지 막힘(링크·전화번호·도배·하루 한도) | `frSend() toast` | 없음 | sfx_ui_error | — |
| 86 | 친구 | 대국 신청 받음 | `frInvBanner() 새 신청(로비)` | 없음 | sfx_notify ×2 | 180ms 간격 |
| 87 | 친구 | 내 신청 거절당함 | `frChanged() "거절했어요"` | 없음 | sfx_ui_error | -12dB |
| 88 | 친구 | 관전 시작 | `frWatch()` | 없음 | sfx_ui_open | — |
| 89 | 친구 | 방 닫힘 | `frTick() toast "방이 닫혔어요"` | 없음 | sfx_ui_error | -12dB |
| 90 | 묘수 | 정답 | `fxpzgo → pzJudge() ok` | correct | sfx_fx_chime×3 + sparkle | — |
| 91 | 묘수 | 오답 | `pzJudge() !ok` | wrong | sfx_stone_void | — |
| 92 | 튜토리얼 | 튜토리얼 안 지정·봉인·개봉 | `T.designated / T.submit` | 실제와 같음 | 실제 대국과 같은 소리 | 소리로도 규칙 학습 |
| 93 | 튜토리얼 | 완료 단계 | `TUT end → bo-tut-done` | 없음 | sfx_fx_chime | — |
| 94 | 이모트 | 받기 | `emoShow(fromMe=false), 이모트 끄기면 무음` | pop | sfx_emote_pop | -4dB 추가, 종류별 피치 |
| 95 | 이모트 | 쿨타임 중 | `emoSend() toast "n초 뒤"` | 없음 | sfx_ui_error | -16dB |
| 96 | 공통 | 오류 토스트 전반(저장 실패·오프라인·권한) | `wmine catch / toast` | 없음 | sfx_ui_error | -12dB |
| 97 | 공통 | 정보 토스트(복사됨 등) | `toast()` | 없음 | 무음 | 버튼 소리로 충분 |
| 98 | 공통 | 업데이트 알림 띠 | `#updBar` | 없음 | 무음 | — |
| 99 | 공통 | 화면 읽기 알림 | `say()` | — | 무음 | — |
| 100 | 공통 | 첫 화면·환영 | `showWelcome()` | — | 첫 터치 뒤 bgm_lobby 시작 | 브라우저 정책 |

### 6-2. 버튼 data-act 전체 (130개) → 파일

기본값은 sfx_ui_tap. 아래는 액션별로 정한 파일(코드의 `SND_ACT` 표를 이 표로 바꾸면 됨).

| 파일 | 재생 방법 | data-act | 개수 |
|---|---|---|---|
| sfx_chip_click | +1·+5·+10 모두 같은 소리 | `b5`, `bp`, `bq`, `fxpzb` | 4 |
| sfx_chip_click | 피치 0.9 | `bm` | 1 |
| sfx_chip_sweep | 기본 | `breset` | 1 |
| sfx_chip_sweep | 피치 1.1 | `beven` | 1 |
| sfx_emote_pop | 종류별 피치 | `fxemo` | 1 |
| sfx_reward_gem ×3 | 90ms 간격 피치 1.0/1.08/1.16 | `ecosz`, `rwclaim` | 2 |
| sfx_seal_lock | fxpzgo는 뒤이어 정답/오답 | `bsubmit`, `fxpzgo`, `lsubmit`, `tsubmit` | 4 |
| sfx_shop_equip | 해제 피치 0.85 | `ecoeq` | 1 |
| sfx_stone_place_1~3 | -10dB(돌이 놓이는 느낌, 지금은 page) | `rvnext` | 1 |
| sfx_stone_tick | -12dB | `rvprev` | 1 |
| sfx_stone_tick | 방향 1.08 / 밀기 0.95 | `dir`, `fxpzpick`, `nudge` | 3 |
| sfx_stone_tick ×3 | 0/60/120ms | `dconfirm` | 1 |
| sfx_ui_close | -16dB (지금은 soft) | `dlgno` | 1 |
| sfx_ui_close | 닫기·거절·나가기 | `frbk`, `frcancel`, `frdel`, `frinvcan`, `frinvno`, `frno`, `fxrcx`, `hintx`, `leave`, `lobby`, `rvclose`, `shclose`, `tskip`, `wskip` | 14 |
| sfx_ui_confirm | 진행되는 버튼(없으면 ui_tap) | `again`, `archexp`, `copycode`, `copyroom`, `copyvfy`, `create`, `dlgok`, `emlink`, `emlogin`, `emreset`, `enter`, `fradd`, `frchinv`, `frcopy`, `frcopylink`, `frinvok`, `frinvp`, `frok`, `frrep`, `frshare`, `fxrcshare`, `glink`, `invite`, `join`, `joincode`, `lagain`, `lnext`, `loadcode`, `local`, `lrank`, `lresume`, `nickok`, `remm`, `solo`, `tdone`, `tsolo`, `tut`, `wglink`, `wtut` | 39 |
| sfx_ui_confirm / sfx_ui_close | 시작=confirm+bgm_match, 취소=close | `mm` | 1 |
| sfx_ui_open | -16dB | `fxemobtn` | 1 |
| sfx_ui_open | page: 피치 1.15 -8dB | `tprev` | 1 |
| sfx_ui_open | page: 피치 1.3 -8dB | `tnext` | 1 |
| sfx_ui_open | 메시지 보냄: 피치 1.3 -8dB | `frrxs` | 1 |
| sfx_ui_open | 오늘 안 찍었으면 stamp+gem | `ecoatt` | 1 |
| sfx_ui_open | 창·시트·대화상자 열기 | `abclaim`, `acc`, `admusers`, `arc`, `delacct`, `ecocat`, `ecoitem`, `ecoopen`, `frbklist`, `frchat`, `frchmenu`, `frchprof`, `frinv`, `frprof`, `frrepo`, `fxpuz`, `prof`, `resign`, `review`, `rkacc`, `sheet`, `uncover`, `wemail` | 23 |
| sfx_ui_tap | 기본 | `admdl`, `admflt`, `ecotab`, `fradmrep`, `frgame`, `frrx`, `frunbk`, `qinfo`, `rkmore`, `tretry` | 10 |
| sfx_ui_tap | 피치 0.75 -16dB | `bcol` | 1 |
| sfx_ui_tap | 피치 0.75 -4dB(soft). 잠긴 레벨은 ui_error | `level`, `preset` | 2 |
| sfx_ui_tap | 피치 0.9 | `tab`, `tabback`, `zout` | 3 |
| sfx_ui_tap | 피치 1.1 | `zin` | 1 |
| sfx_ui_toggle | 켬 1.0 / 끔 0.85 | `aitime`, `frsetg`, `full`, `fxrvai`, `peek`, `showcode`, `theme` | 7 |
| 무음 | 새로고침 | `reload` | 1 |
| 무음 | 현재 빈 동작(동전 소리는 showCoin에서) | `coin` | 1 |
| | | **합계** | **130** |

### 6-3. 설정 스위치 (9개)

`setBig`, `setVib`, `setSnd`, `setHint`, `setEmo`, `emoMute`, `frSetReq`, `frSetSt`, `privRoom` → 모두 **sfx_ui_toggle**(켬 1.0 / 끔 0.85). `setSnd`는 켤 때만 미리듣기로 sfx_fx_chime(끌 때는 무음).

### 6-4. 배경음 장면 (11개)

| 장면 | 조건 | 파일 |
|---|---|---|
| 로비(모든 탭) | `show("lobby")` | bgm_lobby |
| 대국(온라인·AI·한 폰·랭크) | `show("game")` | bgm_game |
| 마지막 위협 | `판에 막히지 않은 4(공개 판 정보만)` | bgm_tension |
| 결과 화면 | `phase over + 징글 끝` | bgm_result |
| 랭크 매칭 대기 | `MM.on` | bgm_match |
| 친구 신청 대기 | `frMyInv 대기 중(G.meta.status open)` | bgm_match |
| 묘수 풀이 | `openSheet("puz")` | bgm_puzzle |
| 복기 | `UI.review` | bgm_puzzle -4dB |
| 튜토리얼 | `UI.mode==="tut"` | bgm_lobby -4dB |
| 시즌 결산 | `recapShow()` | jg_season → bgm_result |
| 앱 가림/탭 전환 | `visibilitychange hidden` | 모든 소리 일시정지 |

전환 규칙: 장면이 바뀌면 1초 크로스페이드(긴장 ↔ 대국은 2초). 대국 BGM은 개봉 중에도 끊지 않음.

### 6-5. 이모트 종류별 (sfx_emote_pop 하나로)

| 이모트 | 뜻 | 피치 | 이모트 | 뜻 | 피치 |
|---|---|---|---|---|---|
| 안녕 | 인사 | 1.05 | 최고 | 칭찬 | 1.12 |
| 깜짝 | 놀람 | 1.2 | 메롱 | 놀리기 | 0.95 |
| 덤벼 | 도발 | 0.88 | 아쉽다 | 아쉬움 | 0.9 |
| 힘내 | 응원 | 1.08 | 음… | 생각 중 | 0.85 |
| 하하 | 웃음 | 1.15 | 분해 | 분함 | 0.82 |
| 고마워 | 고마움 | 1.05 | 박수 | 박수 | 3번 연속(70ms) 1.1 |

긍정은 높게, 도발·분함은 낮게. 받은 이모트는 −4dB 더, 설정에서 이모트를 끄면 무음.

---

## 7. 최종 파일 목록 (43개)

| # | 파일명 | 분류 | 우선 | 길이 | 음량(dB) | 현재 SND | 쓰는 곳 | 1순위 도구 |
|---|---|---|---|---|---|---|---|---|
| 1 | `bgm_lobby.mp3` | BGM | 1 | 60~90초 루프 | -18 (BGM 기준) | (없음·새로) | 로비 전체(홈·랭크·기록·규칙·보상·상점·친구 탭), 튜토리얼(-4dB), 첫 환영 화면(첫 터치 뒤) | Suno 곡 |
| 2 | `bgm_game.mp3` | BGM | 1 | 60~90초 루프 | -20 | (없음·새로) | 대국 화면 전체(온라인·AI·한 폰·랭크전), 개봉 연출 중에도 계속 | Suno 곡 |
| 3 | `jg_win.mp3` | 징글 | 1 | 3~4초 | -2 | win | 내가 이김(오목·동시 오목 판정승·상대 시간 초과 3회·기권승·부재승·나감) | Suno Sounds(먼저) → Suno 곡 |
| 4 | `jg_lose.mp3` | 징글 | 1 | 2~3초 | -4 | lose | 내가 짐(오목 당함·시간 초과 3회·기권패·지정 변경·봉인 불일치 패) | Suno Sounds(먼저) → Suno 곡 |
| 5 | `sfx_ui_tap.mp3` | UI | 1 | 0.05초 | -14 | tap / tab / soft | 일반 버튼 기본음(아래 표에서 따로 정하지 않은 모든 data-act). 탭 이동은 피치 0.9, soft(레벨·프리셋 등)는 피치 0.75·-4dB | Suno Sounds → Kenney |
| 6 | `sfx_ui_open.mp3` | UI | 1 | 0.12~0.15초 | -14 | open / page | 시트·창·대화상자·프로필·채팅·복기·묘수 창 열기, 메시지 보내기(피치 1.3·-8dB), 튜토리얼/복기 넘김 page(피치 1.3·-8dB) | Suno Sounds → Kenney |
| 7 | `sfx_ui_close.mp3` | UI | 1 | 0.12초 | -15 | close | 시트 닫기·대화상자 취소·창 닫기·거절·나가기·매칭 취소 | Audacity로 sfx_ui_open 뒤집기(새로 안 만들어도 됨) → 또는 Suno Sounds |
| 8 | `sfx_ui_error.mp3` | UI | 1 | 0.15~0.2초 | -10 | error / over | 오류·불가 토스트(빈칸만 가능·세 칸 불가·옥돌 부족·저장 실패·방 코드 오류·링크 금지 등), 베팅 합계 초과(-12dB) | Suno Sounds → Kenney |
| 9 | `sfx_stone_place_1.mp3` | 돌 | 1 | 0.2~0.4초 | 0 (기준) | stone | 개봉 때 돌 놓임(A칸), 오목 완성 첫 음, 복기 다음 수(-10dB). 흑=피치 0.97 / 백=피치 1.03 | Suno Sounds(먼저) → 직접 녹음 |
| 10 | `sfx_stone_place_2.mp3` | 돌 | 1 | 0.2~0.4초 | 0 | stone | 개봉 B칸(같은 소리 반복 피로 방지용 변형) | Suno Sounds(먼저) → 직접 녹음 |
| 11 | `sfx_stone_place_3.mp3` | 돌 | 1 | 0.2~0.4초 | 0 | stone | 개봉 C칸(변형 3) | Suno Sounds(먼저) → 직접 녹음 |
| 12 | `sfx_stone_tick.mp3` | 돌 | 1 | 0.05~0.08초 | -12 | pick(아직 연결 안 됨) | 세 칸 고르기: 칸 탭·방향·한 칸 밀기·끌어 옮기기(-16dB, 80ms 간격 제한), 지정 확정=3번 연속(0/60/120ms, 피치 1.0/1.06/1.12), 묘수 칸 선택, 복기 이전 수 | Suno Sounds → 직접 녹음 |
| 13 | `sfx_chip_click.mp3` | 칩 | 1 | 0.08~0.15초 | -10 | chipUp / chipDown / chipStack | 베팅 +1·+5·+10·−1, 길게 누르기 반복(220ms에 1번까지), 묘수 풀이 칩. **+1/+5/+10 모두 같은 소리**, −는 피치 0.9만 | Suno Sounds(먼저) → 직접 녹음 / Kenney Casino Audio |
| 14 | `sfx_seal_lock.mp3` | 칩 | 1 | 0.3~0.5초 | -4 | seal / oppSeal | 내 봉인(bsubmit·lsubmit·tsubmit), 묘수 제출. 상대 봉인 완료=피치 1.25·-16dB(금액과 무관, 한 턴에 1번) | Suno Sounds(먼저) → ElevenLabs |
| 15 | `sfx_seal_break.mp3` | 칩 | 1 | 0.1~0.2초 | -3 | crack | 개봉: 칸마다 도장 깨짐(A 0초·B 0.38초·C 0.76초, 피치 1.0/1.04/1.08) | Suno Sounds(먼저) → ElevenLabs |
| 16 | `sfx_coin_flip.mp3` | 동전 | 1 | 1.7~1.9초 | -6 | coinFlip | 선 정하기: 엄지로 튕김 + 공중 회전(showCoin 시작, 착지음 1.75초 전까지) | Suno Sounds(먼저) → 직접 녹음 |
| 17 | `sfx_coin_land.mp3` | 동전 | 1 | 0.6~0.9초 | -4 | coinLand | 동전 착지 + 흔들리다 멈춤(showCoin 1.75초 / 진 쪽 먼저·움직임 줄이기 설정이면 이것만) | Suno Sounds(먼저) → 직접 녹음 |
| 18 | `sfx_timer_tick.mp3` | 타이머 | 1 | 0.03~0.05초 | -8 | tick / tickLate | 내 차례 남은 10초(피치 0.8·-12dB, 1번), 5·4·3·2초(기본), 1초(피치 1.25·-5dB) | Suno Sounds → Kenney |
| 19 | `sfx_fx_chime.mp3` | 연출 | 1 | 0.8~1.2초 | -6 | five / correct / reward 일부 | 오목 완성(3번 아르페지오: 피치 1.0/1.26/1.5, 70ms 간격, 돌 소리 뒤), 묘수 정답(+sparkle), 과제 완료·업적(-8dB), 튜토리얼 완료, 소리 켜기 미리듣기 | Suno Sounds → ElevenLabs |
| 20 | `sfx_fx_myturn.mp3` | 연출 | 1 | 0.3~0.4초 | -8 | turn | 내 차례 알림(showMyTurn: 세 칸 고르기·베팅), 동전 결과 내가 선 플레이어일 때 | Suno Sounds → ElevenLabs |
| 21 | `bgm_tension.mp3` | BGM | 2 | 30~60초 루프 | -19 | (없음·새로) | 판에 막히지 않은 4(다음 턴 오목 위협)가 생겼을 때 bgm_game에서 2초 크로스페이드 → 위협이 사라지면 복귀 | Suno 곡 |
| 22 | `bgm_match.mp3` | BGM | 2 | 20~30초 루프 | -18 | (없음·새로) | 랭크 매칭 찾는 중(MM.on, 최대 20초), 친구 대국 신청 보내고 기다리는 중 | Suno 곡 |
| 23 | `jg_draw.mp3` | 징글 | 2 | 2~3초 | -5 | draw(아직 연결 안 됨) | 무승부(둘 곳 없음·최대 턴 도달·둘 다 시간 초과), 무효(확인 불일치), 관전자에게 끝난 판(승패 무관 중립) | Suno Sounds(먼저) → Suno 곡 |
| 24 | `jg_tier_up.mp3` | 징글 | 2 | 4~5초 | -2 | tierUp | 승급(tierUp→tupShow), 배치 완료(첫 티어), 랭크 열림 안내 rankIntro(-8dB) | Suno Sounds(먼저) → Suno 곡 |
| 25 | `jg_tier_down.mp3` | 징글 | 2 | 2초 | -8 | tierDown(아직 연결 안 됨) | 강등(tierMove 결과 up=false, "○○으로 내려감") | Suno Sounds |
| 26 | `sfx_ui_toggle.mp3` | UI | 2 | 0.06초 | -16 | toggleOn / toggleOff | 설정 스위치 9종·테마·전체 판·상대 정보 보기·코드 보기·AI 훈수. 켬=피치 1.0, 끔=피치 0.85 | Suno Sounds → Kenney |
| 27 | `sfx_ui_confirm.mp3` | UI | 2 | 0.2초 | -10 | (없음·새로 — 지금은 tap) | 확인·시작·만들기·입장·수락·복사·공유처럼 "일이 진행되는" 버튼 | Suno Sounds → Kenney |
| 28 | `sfx_stone_void.mp3` | 돌 | 2 | 0.4~0.6초 | -6 | voidLine / wrong | 6목 이상 빨간 줄(OVSEEN 처음 한 번만), 묘수 풀이 오답 | Suno Sounds → ElevenLabs |
| 29 | `sfx_chip_sweep.mp3` | 칩 | 2 | 0.25~0.35초 | -10 | chipReset | 1씩 되돌리기(breset), 균등 나누기(beven, 피치 1.1) | Suno Sounds(먼저) → 직접 녹음 |
| 30 | `sfx_timer_out.mp3` | 타이머 | 2 | 0.4~0.5초 | -4 | timeout(아직 연결 안 됨) | 내 시간 초과(자동 지정·칸마다 1칩 자동 봉인·"시간 초과" 토스트) | Suno Sounds → ElevenLabs |
| 31 | `sfx_reward_stamp.mp3` | 보상 | 2 | 0.3~0.5초 | -2 | stamp | 출석체크 도장 쾅(attShow at>0) | Suno Sounds(먼저) → 직접 녹음 |
| 32 | `sfx_reward_gem.mp3` | 보상 | 2 | 0.5~0.8초 | -6 | reward / coin1 | 옥돌 받기(도장 0.35초 뒤), 모두 받기(3번, 90ms 간격, 피치 1.0/1.08/1.16), 시즌 보상, 구매 앞부분 | Suno Sounds(먼저) → 직접 녹음 |
| 33 | `sfx_shop_buy.mp3` | 상점 | 2 | 0.4~0.6초 | -6 | buy | 상점 구매 성공(ecoBuy ok), 닉네임 유료 변경 성공 | Suno Sounds → ElevenLabs |
| 34 | `sfx_notify.mp3` | 알림 | 2 | 0.3~0.5초 | -8 | notify(아직 연결 안 됨) / msg | 친구 요청 받음·친구 됨·대국 신청 받음(2번, 180ms 간격)·상대도 다시 하기, 채팅 메시지 받음(피치 1.25·-6dB 짧게, 3초에 1번까지) | Suno Sounds → Kenney |
| 35 | `sfx_mm_found.mp3` | 랭크 | 2 | 0.6~0.8초 | -4 | match | 랭크 상대 찾음(사람 mmHost·AI mmBot 똑같이), 친구 대국 신청 수락돼 입장 | Suno Sounds → ElevenLabs |
| 36 | `sfx_tier_snap.mp3` | 랭크 | 2 | 0.06~0.1초 | -8 | tierPiece(아직 연결 안 됨) | 승급 문양 조각이 끼워질 때마다(단계 k마다 피치 1+0.06k, 간격 0.13~0.18초) | Suno Sounds → ElevenLabs |
| 37 | `bgm_puzzle.mp3` | BGM | 3 | 60초 루프 | -20 | (없음·새로) | 오늘의 묘수 풀이 창, 복기 화면(-4dB) | Suno 곡 |
| 38 | `bgm_result.mp3` | BGM | 3 | 30~45초 루프 | -22 | (없음·새로) | 승리·패배·무승부 화면에서 징글이 끝난 뒤(징글 4초 뒤 페이드인), 시즌 결산 창 뒤 | Suno 곡 |
| 39 | `jg_tier_top.mp3` | 징글 | 3 | 5~6초 | -1 | tierUp(top) | 마스터·챌린저 승급(tupShow top=true), 챌린저 진입 chalPop() | Suno Sounds(먼저) → Suno 곡 |
| 40 | `jg_season.mp3` | 징글 | 3 | 4~5초 | -3 | (없음·새로) | 시즌 결산 창 recapShow() | Suno Sounds(먼저) → Suno 곡 |
| 41 | `sfx_fx_sparkle.mp3` | 연출 | 3 | 0.5~0.8초 | -10 | (없음·새로) | 승급 문양 완성 번쩍(tupShow fin), 묘수 정답, 업적, 출석 7·14·21·28일째 | Suno Sounds → ElevenLabs |
| 42 | `sfx_emote_pop.mp3` | 연출 | 3 | 0.1~0.15초 | -10 | pop | 이모트 보내기/받기(받기는 -4dB 추가, 이모트 끄기면 무음). 종류별 피치는 6장 표 | Suno Sounds → Kenney |
| 43 | `sfx_shop_equip.mp3` | 상점 | 3 | 0.2~0.3초 | -10 | equip | 장착(ecoEquip id 있음), 해제=피치 0.85 | Suno Sounds → ElevenLabs |

---

## 8. 파일별 프롬프트 전부 (복사해서 쓰기)

### 공통 사용법

- **먼저 요금제 확인**: Pro 이상에서 만들어야 게임(광고 붙인 구글 플레이 포함)에 쓸 수 있음.
- **배경음(Suno 곡)**: https://suno.com/create → Advanced(Custom) → **Instrumental 켬** → Style 칸에 영어 원문 → 가사 칸 비움 → 고급 옵션 Exclude 칸에 적힌 단어 → 2~3번 생성(4~6곡) → 10장 기준으로 1곡 → Crop·루프 자르기(9장)
- **효과음·징글(Suno Sounds)**: https://suno.com/create → 위쪽 **Sounds** → One Shot 또는 Loop → (적혀 있으면) BPM·Key 입력 → 프롬프트 붙여넣기 → 한 번에 2개 → 2번(4개) 뽑아 고르기
- **대안 프롬프트**는 ElevenLabs Sound Effects(유료 플랜)용. Kenney라고 적힌 파일은 Kenney 무료 팩에서 비슷한 소리를 골라도 됨(CC0).

### 우선순위 1

#### `bgm_lobby.mp3` — BGM · 60~90초 루프 · -18 (BGM 기준)dB
- 쓰는 곳: 로비 전체(홈·랭크·기록·규칙·보상·상점·친구 탭), 튜토리얼(-4dB), 첫 환영 화면(첫 터치 뒤)
- 1순위: Suno 곡 · 설정: Advanced · Instrumental 켬 · Exclude: vocals, choir, EDM drop, distorted guitar, heavy drums, rap · 제목 Jade Hall Lobby · 1분 이상 나오면 인트로 뒤 16마디(53.3초) 또는 24마디(80초) Crop
```
calm elegant ambient, soft felt piano, gentle gayageum plucks, warm pads, 72 BPM, C major, minimal, relaxed, loopable
```
- 대안(Suno Sounds(Loop)):
```
[Suno Sounds · Loop · BPM 72 · Key C major] calm ambient piano and gayageum loop, warm pad, minimal, seamless
```

#### `bgm_game.mp3` — BGM · 60~90초 루프 · -20dB
- 쓰는 곳: 대국 화면 전체(온라인·AI·한 폰·랭크전), 개봉 연출 중에도 계속
- 1순위: Suno 곡 · 설정: Advanced · Instrumental 켬 · Exclude: vocals, choir, EDM drop, distorted guitar, heavy drums, rap, bright bells · 제목 Quiet Board · 20마디(60초) 또는 28마디(84초) Crop
```
minimal focused ambient, deep soft pads, sparse wooden plucks, light ticking percussion, 80 BPM, A minor, mysterious, calm
```
- 대안(Suno Sounds(Loop)):
```
[Suno Sounds · Loop · BPM 80 · Key A minor] minimal dark ambient pad loop, sparse wooden plucks, soft ticks, no melody
```

#### `jg_win.mp3` — 징글 · 3~4초 · -2dB
- 쓰는 곳: 내가 이김(오목·동시 오목 판정승·상대 시간 초과 3회·기권승·부재승·나감)
- 1순위: Suno Sounds(먼저) → Suno 곡 · 설정: Suno Sounds · One Shot · Key C major · 안 되면 Advanced·Instrumental로 만들고 앞 4초 Crop + 끝 0.4초 페이드
```
short victory sting, warm strings and soft brass, gayageum flourish, bright major chord ending, elegant, 4 seconds
```
- 대안(ElevenLabs):
```
Short elegant victory jingle, warm strings and soft brass, plucked zither flourish, ends on a bright major chord, 4 seconds
```

#### `jg_lose.mp3` — 징글 · 2~3초 · -4dB
- 쓰는 곳: 내가 짐(오목 당함·시간 초과 3회·기권패·지정 변경·봉인 불일치 패)
- 1순위: Suno Sounds(먼저) → Suno 곡 · 설정: Suno Sounds · One Shot · Key A minor · 안 되면 Advanced·Instrumental 후 앞 3초 Crop
```
short gentle defeat sting, soft descending piano, low cello, minor chord, calm, dignified, 3 seconds
```
- 대안(ElevenLabs):
```
Short gentle defeat sting, soft descending piano notes with low cello, calm and dignified, not comedic, 3 seconds
```

#### `sfx_ui_tap.mp3` — UI · 0.05초 · -14dB
- 쓰는 곳: 일반 버튼 기본음(아래 표에서 따로 정하지 않은 모든 data-act). 탭 이동은 피치 0.9, soft(레벨·프리셋 등)는 피치 0.75·-4dB
- 1순위: Suno Sounds → Kenney · 설정: Suno Sounds · One Shot · BPM·Key 비움 · 앞 무음 0.01초 이내로 자르기
```
soft subtle UI tap, muted wooden click, very short, clean, dry, mobile app button
```
- 대안(Kenney Interface Sounds / ElevenLabs):
```
Soft subtle mobile UI tap, muted wooden click, very short, dry, 0.05 seconds
```

#### `sfx_ui_open.mp3` — UI · 0.12~0.15초 · -14dB
- 쓰는 곳: 시트·창·대화상자·프로필·채팅·복기·묘수 창 열기, 메시지 보내기(피치 1.3·-8dB), 튜토리얼/복기 넘김 page(피치 1.3·-8dB)
- 1순위: Suno Sounds → Kenney · 설정: Suno Sounds · One Shot
```
soft airy swoosh up, gentle paper slide, UI panel opening, short, clean, dry
```
- 대안(Kenney Interface Sounds / ElevenLabs):
```
Soft airy upward swoosh, gentle paper slide, UI panel opening, 0.15 seconds
```

#### `sfx_ui_close.mp3` — UI · 0.12초 · -15dB
- 쓰는 곳: 시트 닫기·대화상자 취소·창 닫기·거절·나가기·매칭 취소
- 1순위: Audacity로 sfx_ui_open 뒤집기(새로 안 만들어도 됨) → 또는 Suno Sounds · 설정: Audacity: 효과 → 뒤집기(Reverse) 후 끝 0.02초 페이드 / 또는 Suno Sounds · One Shot
```
soft airy swoosh down, gentle paper slide, UI panel closing, short, clean, dry
```
- 대안(ElevenLabs):
```
Soft airy downward swoosh, gentle paper slide, UI panel closing, 0.12 seconds
```

#### `sfx_ui_error.mp3` — UI · 0.15~0.2초 · -10dB
- 쓰는 곳: 오류·불가 토스트(빈칸만 가능·세 칸 불가·옥돌 부족·저장 실패·방 코드 오류·링크 금지 등), 베팅 합계 초과(-12dB)
- 1순위: Suno Sounds → Kenney · 설정: Suno Sounds · One Shot · Key A minor
```
soft low muted wooden thud, gentle UI error, short, not harsh, dry
```
- 대안(Kenney Interface Sounds / ElevenLabs):
```
Soft low muted wooden double thud, gentle UI error, not harsh, 0.2 seconds
```

#### `sfx_stone_place_1.mp3` — 돌 · 0.2~0.4초 · 0 (기준)dB
- 쓰는 곳: 개봉 때 돌 놓임(A칸), 오목 완성 첫 음, 복기 다음 수(-10dB). 흑=피치 0.97 / 백=피치 1.03
- 1순위: Suno Sounds(먼저) → 직접 녹음 · 설정: Suno Sounds · One Shot · 2회(4개) 생성 → 가장 깨끗한 1개. 녹음본과 들어 보고 더 좋은 쪽
```
single slate go stone placed on thick wooden go board, crisp clack, close mic, dry, very short
```
- 대안(직접 녹음 / ElevenLabs):
```
A single slate go stone firmly placed on a thick wooden go board, sharp clean clack, close-up, dry room, 0.3 seconds
```

#### `sfx_stone_place_2.mp3` — 돌 · 0.2~0.4초 · 0dB
- 쓰는 곳: 개봉 B칸(같은 소리 반복 피로 방지용 변형)
- 1순위: Suno Sounds(먼저) → 직접 녹음 · 설정: Suno Sounds · One Shot · place_1과 같은 세션 결과 중 다른 개체 사용
```
single go stone set down on wooden board, slightly softer clack, close mic, dry, very short
```
- 대안(직접 녹음 / ElevenLabs):
```
A go stone set down on a wooden board, slightly softer clack, close-up, dry, 0.3 seconds
```

#### `sfx_stone_place_3.mp3` — 돌 · 0.2~0.4초 · 0dB
- 쓰는 곳: 개봉 C칸(변형 3)
- 1순위: Suno Sounds(먼저) → 직접 녹음 · 설정: Suno Sounds · One Shot
```
single go stone snapped onto wooden board, firm bright clack, close mic, dry, very short
```
- 대안(직접 녹음 / ElevenLabs):
```
A go stone snapped firmly onto a wooden board, bright crisp clack, close-up, dry, 0.3 seconds
```

#### `sfx_stone_tick.mp3` — 돌 · 0.05~0.08초 · -12dB
- 쓰는 곳: 세 칸 고르기: 칸 탭·방향·한 칸 밀기·끌어 옮기기(-16dB, 80ms 간격 제한), 지정 확정=3번 연속(0/60/120ms, 피치 1.0/1.06/1.12), 묘수 칸 선택, 복기 이전 수
- 1순위: Suno Sounds → 직접 녹음 · 설정: Suno Sounds · One Shot
```
light fingertip tap on wooden board, tiny soft tick, very short, dry
```
- 대안(직접 녹음 / ElevenLabs):
```
Light fingertip tap on a wooden board, tiny soft tick, dry, 0.06 seconds
```

#### `sfx_chip_click.mp3` — 칩 · 0.08~0.15초 · -10dB
- 쓰는 곳: 베팅 +1·+5·+10·−1, 길게 누르기 반복(220ms에 1번까지), 묘수 풀이 칩. **+1/+5/+10 모두 같은 소리**, −는 피치 0.9만
- 1순위: Suno Sounds(먼저) → 직접 녹음 / Kenney Casino Audio · 설정: Suno Sounds · One Shot
```
single clay poker chip tapped on chip stack, short soft click, close mic, dry
```
- 대안(직접 녹음 / Kenney Casino Audio / ElevenLabs):
```
One clay poker chip tapped onto a small stack, short soft click, close-up, 0.12 seconds
```

#### `sfx_seal_lock.mp3` — 칩 · 0.3~0.5초 · -4dB
- 쓰는 곳: 내 봉인(bsubmit·lsubmit·tsubmit), 묘수 제출. 상대 봉인 완료=피치 1.25·-16dB(금액과 무관, 한 턴에 1번)
- 1순위: Suno Sounds(먼저) → ElevenLabs · 설정: Suno Sounds · One Shot
```
small wooden box lid closing with soft latch click, satisfying, short, dry
```
- 대안(ElevenLabs):
```
A small wooden box lid closing with a soft latch click, satisfying, 0.4 seconds
```

#### `sfx_seal_break.mp3` — 칩 · 0.1~0.2초 · -3dB
- 쓰는 곳: 개봉: 칸마다 도장 깨짐(A 0초·B 0.38초·C 0.76초, 피치 1.0/1.04/1.08)
- 1순위: Suno Sounds(먼저) → ElevenLabs · 설정: Suno Sounds · One Shot
```
small wax seal cracking, crisp snap with tiny crumble, short, close mic
```
- 대안(ElevenLabs):
```
A small wax seal cracking open, crisp snap with a tiny crumble, close-up, 0.15 seconds
```

#### `sfx_coin_flip.mp3` — 동전 · 1.7~1.9초 · -6dB
- 쓰는 곳: 선 정하기: 엄지로 튕김 + 공중 회전(showCoin 시작, 착지음 1.75초 전까지)
- 1순위: Suno Sounds(먼저) → 직접 녹음 · 설정: Suno Sounds · One Shot · 1.75초 지점에서 자르고 끝 0.05초 페이드
```
coin flicked with thumb, metallic ting then fast spinning whirr in the air slowing down, 2 seconds
```
- 대안(직접 녹음(500원) / ElevenLabs):
```
A coin flicked with a thumb, metallic ting followed by spinning whirr in the air, 1.8 seconds
```

#### `sfx_coin_land.mp3` — 동전 · 0.6~0.9초 · -4dB
- 쓰는 곳: 동전 착지 + 흔들리다 멈춤(showCoin 1.75초 / 진 쪽 먼저·움직임 줄이기 설정이면 이것만)
- 1순위: Suno Sounds(먼저) → 직접 녹음 · 설정: Suno Sounds · One Shot
```
coin landing on wooden table, small bounce and settling wobble, metallic, short
```
- 대안(직접 녹음(500원) / ElevenLabs):
```
A coin landing on a wooden table, small bounce and settling wobble, metallic, 0.8 seconds
```

#### `sfx_timer_tick.mp3` — 타이머 · 0.03~0.05초 · -8dB
- 쓰는 곳: 내 차례 남은 10초(피치 0.8·-12dB, 1번), 5·4·3·2초(기본), 1초(피치 1.25·-5dB)
- 1순위: Suno Sounds → Kenney · 설정: Suno Sounds · One Shot
```
small clean clock tick, soft wooden woodblock tick, very short, dry
```
- 대안(Kenney Interface Sounds / ElevenLabs):
```
Small clean woodblock clock tick, very short, dry, 0.04 seconds
```

#### `sfx_fx_chime.mp3` — 연출 · 0.8~1.2초 · -6dB
- 쓰는 곳: 오목 완성(3번 아르페지오: 피치 1.0/1.26/1.5, 70ms 간격, 돌 소리 뒤), 묘수 정답(+sparkle), 과제 완료·업적(-8dB), 튜토리얼 완료, 소리 켜기 미리듣기
- 1순위: Suno Sounds → ElevenLabs · 설정: Suno Sounds · One Shot · Key C major(C음)
```
single clear bright bell chime, gentle, short decay, elegant
```
- 대안(ElevenLabs):
```
Single clear temple bell chime, gentle and bright, short decay, 1 second
```

#### `sfx_fx_myturn.mp3` — 연출 · 0.3~0.4초 · -8dB
- 쓰는 곳: 내 차례 알림(showMyTurn: 세 칸 고르기·베팅), 동전 결과 내가 선 플레이어일 때
- 1순위: Suno Sounds → ElevenLabs · 설정: Suno Sounds · One Shot · Key C major
```
two soft wooden block notes rising, gentle attention cue, short, calm
```
- 대안(ElevenLabs):
```
Two soft rising wooden block notes, gentle attention cue, calm, 0.35 seconds
```

### 우선순위 2

#### `bgm_tension.mp3` — BGM · 30~60초 루프 · -19dB
- 쓰는 곳: 판에 막히지 않은 4(다음 턴 오목 위협)가 생겼을 때 bgm_game에서 2초 크로스페이드 → 위협이 사라지면 복귀
- 1순위: Suno 곡 · 설정: Advanced · Instrumental 켬 · Exclude: vocals, choir, EDM drop, distorted guitar, heavy drums, rap · 제목 Last Threat · 12마디(30초) 또는 24마디(60초) Crop
```
dark minimal suspense, pulsing low synth, soft heartbeat kick, clock ticks, tense strings, 96 BPM, A minor, restrained
```
- 대안(Suno Sounds(Loop)):
```
[Suno Sounds · Loop · BPM 96 · Key A minor] low pulsing suspense loop, soft heartbeat kick, ticking, restrained
```

#### `bgm_match.mp3` — BGM · 20~30초 루프 · -18dB
- 쓰는 곳: 랭크 매칭 찾는 중(MM.on, 최대 20초), 친구 대국 신청 보내고 기다리는 중
- 1순위: Suno 곡 · 설정: Advanced · Instrumental 켬 · Exclude: vocals, choir, EDM drop, distorted guitar, heavy drums, rap · 제목 Finding Rival · 8마디(21.3초) 또는 12마디(32초) Crop
```
light anticipation loop, soft pulsing plucks, airy pads, subtle ticking, 90 BPM, A minor, hopeful suspense, minimal
```
- 대안(Suno Sounds(Loop)):
```
[Suno Sounds · Loop · BPM 90 · Key A minor] light pulsing pluck loop, airy pad, subtle ticking, anticipation
```

#### `jg_draw.mp3` — 징글 · 2~3초 · -5dB
- 쓰는 곳: 무승부(둘 곳 없음·최대 턴 도달·둘 다 시간 초과), 무효(확인 불일치), 관전자에게 끝난 판(승패 무관 중립)
- 1순위: Suno Sounds(먼저) → Suno 곡 · 설정: Suno Sounds · One Shot · Key C major
```
short neutral resolve sting, soft piano and warm pad, suspended chord gently resolving, calm, balanced, 3 seconds
```
- 대안(ElevenLabs):
```
Short neutral musical sting, soft piano and warm pad, suspended chord resolving gently, calm, 3 seconds
```

#### `jg_tier_up.mp3` — 징글 · 4~5초 · -2dB
- 쓰는 곳: 승급(tierUp→tupShow), 배치 완료(첫 티어), 랭크 열림 안내 rankIntro(-8dB)
- 1순위: Suno Sounds(먼저) → Suno 곡 · 설정: Suno Sounds · One Shot · Key C major · 정점(가장 큰 순간)이 2.5초 근처인 것을 고름(문양 조립 끝과 맞춤)
```
rising ceremonial sting, deep taiko hit, shimmering bells, string swell, majestic but tasteful, bright ending, 5 seconds
```
- 대안(ElevenLabs):
```
Rising ceremonial fanfare sting, deep taiko hit, shimmering bells and string swell, majestic but tasteful, peak at 2.5 seconds, 5 seconds
```

#### `jg_tier_down.mp3` — 징글 · 2초 · -8dB
- 쓰는 곳: 강등(tierMove 결과 up=false, "○○으로 내려감")
- 1순위: Suno Sounds · 설정: Suno Sounds · One Shot · Key A minor
```
short soft descending chime, muted piano, low warm pad, minor, calm, gentle, 2 seconds
```
- 대안(ElevenLabs):
```
Short soft descending chime, muted piano and low warm pad, gentle, not sad, 2 seconds
```

#### `sfx_ui_toggle.mp3` — UI · 0.06초 · -16dB
- 쓰는 곳: 설정 스위치 9종·테마·전체 판·상대 정보 보기·코드 보기·AI 훈수. 켬=피치 1.0, 끔=피치 0.85
- 1순위: Suno Sounds → Kenney · 설정: Suno Sounds · One Shot
```
tiny crisp switch click, small plastic toggle, very short, clean, dry
```
- 대안(Kenney Interface Sounds / ElevenLabs):
```
Tiny crisp plastic toggle switch click, very short, dry, 0.06 seconds
```

#### `sfx_ui_confirm.mp3` — UI · 0.2초 · -10dB
- 쓰는 곳: 확인·시작·만들기·입장·수락·복사·공유처럼 "일이 진행되는" 버튼
- 1순위: Suno Sounds → Kenney · 설정: Suno Sounds · One Shot · Key C major
```
soft positive UI confirm, two-note wooden marimba blip rising, short, clean
```
- 대안(Kenney Interface Sounds / ElevenLabs):
```
Soft positive confirm sound, two rising wooden marimba notes, clean, 0.2 seconds
```

#### `sfx_stone_void.mp3` — 돌 · 0.4~0.6초 · -6dB
- 쓰는 곳: 6목 이상 빨간 줄(OVSEEN 처음 한 번만), 묘수 풀이 오답
- 1순위: Suno Sounds → ElevenLabs · 설정: Suno Sounds · One Shot · Key A minor
```
low muted wooden knock with soft descending tone, short, gentle, not a buzzer
```
- 대안(ElevenLabs):
```
Low dull wooden knock followed by a soft downward tone, subtle, not alarming, 0.5 seconds
```

#### `sfx_chip_sweep.mp3` — 칩 · 0.25~0.35초 · -10dB
- 쓰는 곳: 1씩 되돌리기(breset), 균등 나누기(beven, 피치 1.1)
- 1순위: Suno Sounds(먼저) → 직접 녹음 · 설정: Suno Sounds · One Shot
```
handful of poker chips gently sliding together on felt, short soft shuffle, dry
```
- 대안(직접 녹음 / ElevenLabs):
```
A few poker chips gently sliding together on felt, short soft shuffle, 0.3 seconds
```

#### `sfx_timer_out.mp3` — 타이머 · 0.4~0.5초 · -4dB
- 쓰는 곳: 내 시간 초과(자동 지정·칸마다 1칩 자동 봉인·"시간 초과" 토스트)
- 1순위: Suno Sounds → ElevenLabs · 설정: Suno Sounds · One Shot · Key A minor
```
soft low gong-like thud, muted, time is up, short, not alarming
```
- 대안(ElevenLabs):
```
Soft low muted gong thud signalling time is up, not alarming, 0.5 seconds
```

#### `sfx_reward_stamp.mp3` — 보상 · 0.3~0.5초 · -2dB
- 쓰는 곳: 출석체크 도장 쾅(attShow at>0)
- 1순위: Suno Sounds(먼저) → 직접 녹음 · 설정: Suno Sounds · One Shot
```
heavy wooden stamp slammed on paper on desk, deep thump, short, dry
```
- 대안(직접 녹음 / ElevenLabs):
```
Heavy wooden rubber stamp slammed on paper on a desk, deep thump, 0.4 seconds
```

#### `sfx_reward_gem.mp3` — 보상 · 0.5~0.8초 · -6dB
- 쓰는 곳: 옥돌 받기(도장 0.35초 뒤), 모두 받기(3번, 90ms 간격, 피치 1.0/1.08/1.16), 시즌 보상, 구매 앞부분
- 1순위: Suno Sounds(먼저) → 직접 녹음 · 설정: Suno Sounds · One Shot
```
few small jade stones rolling and clinking into ceramic bowl, bright, short
```
- 대안(직접 녹음(바둑알+사기그릇) / ElevenLabs):
```
A few small glass stones rolling and clinking into a ceramic bowl, bright, 0.7 seconds
```

#### `sfx_shop_buy.mp3` — 상점 · 0.4~0.6초 · -6dB
- 쓰는 곳: 상점 구매 성공(ecoBuy ok), 닉네임 유료 변경 성공
- 1순위: Suno Sounds → ElevenLabs · 설정: Suno Sounds · One Shot · Key C major
```
gentle purchase confirm, soft click and warm two-note chime, calm, short
```
- 대안(ElevenLabs):
```
Purchase confirmation, gentle soft click followed by a warm two-note chime, calm, 0.5 seconds
```

#### `sfx_notify.mp3` — 알림 · 0.3~0.5초 · -8dB
- 쓰는 곳: 친구 요청 받음·친구 됨·대국 신청 받음(2번, 180ms 간격)·상대도 다시 하기, 채팅 메시지 받음(피치 1.25·-6dB 짧게, 3초에 1번까지)
- 1순위: Suno Sounds → Kenney · 설정: Suno Sounds · One Shot · Key C major
```
soft two-note notification chime, clear, calm, mobile app, short
```
- 대안(Kenney Interface Sounds / ElevenLabs):
```
Soft two-note notification chime for a mobile app, clear and calm, 0.4 seconds
```

#### `sfx_mm_found.mp3` — 랭크 · 0.6~0.8초 · -4dB
- 쓰는 곳: 랭크 상대 찾음(사람 mmHost·AI mmBot 똑같이), 친구 대국 신청 수락돼 입장
- 1순위: Suno Sounds → ElevenLabs · 설정: Suno Sounds · One Shot · Key C major
```
match found cue, bright rising three-note chime with soft wooden hit, short, exciting but calm
```
- 대안(ElevenLabs):
```
Match found cue, bright rising three-note chime with a soft wooden hit, 0.7 seconds
```

#### `sfx_tier_snap.mp3` — 랭크 · 0.06~0.1초 · -8dB
- 쓰는 곳: 승급 문양 조각이 끼워질 때마다(단계 k마다 피치 1+0.06k, 간격 0.13~0.18초)
- 1순위: Suno Sounds → ElevenLabs · 설정: Suno Sounds · One Shot
```
crisp jade piece snapping into place, small metallic click, very short, dry
```
- 대안(ElevenLabs):
```
A crisp jade piece snapping into place, small metallic click, dry, 0.08 seconds
```

### 우선순위 3

#### `bgm_puzzle.mp3` — BGM · 60초 루프 · -20dB
- 쓰는 곳: 오늘의 묘수 풀이 창, 복기 화면(-4dB)
- 1순위: Suno 곡 · 설정: Advanced · Instrumental 켬 · Exclude: vocals, choir, EDM drop, distorted guitar, heavy drums, rap · 제목 Daily Myosu · 16마디(60초) Crop
```
contemplative zen ambient, breathy daegeum flute, soft piano, slow 64 BPM, D minor, quiet, thoughtful, spacious
```
- 대안(Suno Sounds(Loop)):
```
[Suno Sounds · Loop · BPM 64 · Key D minor] quiet zen loop, breathy bamboo flute, soft piano, spacious
```

#### `bgm_result.mp3` — BGM · 30~45초 루프 · -22dB
- 쓰는 곳: 승리·패배·무승부 화면에서 징글이 끝난 뒤(징글 4초 뒤 페이드인), 시즌 결산 창 뒤
- 1순위: Suno 곡 · 설정: Advanced · Instrumental 켬 · Exclude: vocals, choir, EDM drop, distorted guitar, heavy drums, rap · 제목 After the Game · 8마디(27.4초) 또는 12마디(41초) Crop
```
soft reflective ambient, warm piano chords, gentle gayageum, airy pad, 70 BPM, C major, calm afterglow, minimal
```
- 대안(Suno Sounds(Loop)):
```
[Suno Sounds · Loop · BPM 70 · Key C major] warm reflective piano loop, gentle gayageum, airy pad, calm
```

#### `jg_tier_top.mp3` — 징글 · 5~6초 · -1dB
- 쓰는 곳: 마스터·챌린저 승급(tupShow top=true), 챌린저 진입 chalPop()
- 1순위: Suno Sounds(먼저) → Suno 곡 · 설정: Suno Sounds · One Shot · Key C major
```
grand ceremonial sting, deep taiko, golden brass swell, shimmering bells, gayageum glissando, majestic, tasteful, 6 seconds
```
- 대안(ElevenLabs):
```
Grand ceremonial fanfare, deep taiko drums, golden brass swell, shimmering bells, zither glissando, majestic yet tasteful, 6 seconds
```

#### `jg_season.mp3` — 징글 · 4~5초 · -3dB
- 쓰는 곳: 시즌 결산 창 recapShow()
- 1순위: Suno Sounds(먼저) → Suno 곡 · 설정: Suno Sounds · One Shot · Key C major
```
reflective ceremonial sting, warm strings, soft bells, gayageum glissando, nostalgic and proud, 5 seconds
```
- 대안(ElevenLabs):
```
Reflective ceremonial sting, warm strings, soft bells, zither glissando, nostalgic and proud, 5 seconds
```

#### `sfx_fx_sparkle.mp3` — 연출 · 0.5~0.8초 · -10dB
- 쓰는 곳: 승급 문양 완성 번쩍(tupShow fin), 묘수 정답, 업적, 출석 7·14·21·28일째
- 1순위: Suno Sounds → ElevenLabs · 설정: Suno Sounds · One Shot · Key C major
```
soft magical sparkle shimmer, tiny glass bells, short, elegant
```
- 대안(ElevenLabs):
```
Soft magical sparkle shimmer of tiny glass bells, elegant, 0.6 seconds
```

#### `sfx_emote_pop.mp3` — 연출 · 0.1~0.15초 · -10dB
- 쓰는 곳: 이모트 보내기/받기(받기는 -4dB 추가, 이모트 끄기면 무음). 종류별 피치는 6장 표
- 1순위: Suno Sounds → Kenney · 설정: Suno Sounds · One Shot
```
soft rounded bubble pop, subtle, very short, clean
```
- 대안(Kenney Interface Sounds / ElevenLabs):
```
Soft rounded bubble pop, subtle, clean, 0.12 seconds
```

#### `sfx_shop_equip.mp3` — 상점 · 0.2~0.3초 · -10dB
- 쓰는 곳: 장착(ecoEquip id 있음), 해제=피치 0.85
- 1순위: Suno Sounds → ElevenLabs · 설정: Suno Sounds · One Shot
```
smooth jade bead clicking into place, soft fabric rustle, short, satisfying
```
- 대안(ElevenLabs):
```
A smooth jade bead clicking into place with a soft fabric rustle, 0.25 seconds
```

---

## 9. 루프 자르기·녹음 방법

**루프 자르기(Audacity, https://www.audacityteam.org/download/)**
1. Suno에서 WAV(없으면 MP3)로 받기 → Audacity에 넣기
2. 인트로·엔딩(페이드아웃)은 버리고 연주가 꽉 찬 가운데 구간 고르기
3. `1마디 = 240 ÷ BPM 초` → 64=3.75초, 70=3.43초, 72=3.33초, 80=3초, 90=2.67초, 96=2.5초. **마디의 정수배**로 자르기(7장 설정 칸에 곡별 길이 적어 둠)
4. 자르는 점은 파형이 0을 지나는 곳(선택 후 `Z` 키)으로 → "틱" 잡음 방지
5. 10번 반복 재생해 이음새 확인, 튀면 1박씩 옮기기
6. 징글은 앞 무음 0.05초 이내, 끝 0.3~0.5초 페이드아웃. 효과음은 앞 무음 0.01초 이내(눌렀는데 늦게 나는 느낌 방지)

**직접 녹음(돌·칩·동전·도장·옥돌)**
- 폰 녹음 앱(가능하면 고음질), 소리 나는 곳에서 20~30cm, 이불·커튼 많은 방, 냉장고·에어컨 끄기
- 바둑돌: 실제 바둑판(없으면 두꺼운 원목 도마)에 같은 세기로 15~20번 + 세기 바꿔 15번. 흑돌·백돌 따로. 좋은 것 3개 → stone_place_1~3, 손가락 끝 톡 → stone_tick
- 칩: 포커칩 1개를 칩 더미에 "톡"(없으면 바둑알을 통에). 여러 개 쓸어 모으기 → chip_sweep
- 동전: 500원을 엄지로 튕겨 책상에 떨어뜨림. 튕김~공중(1.75초까지) → coin_flip, 착지~멈춤 → coin_land
- 도장: 나무 도장을 종이 깐 책상에 "쾅"(입력이 빨간색까지 안 가게) → reward_stamp
- 옥돌: 바둑알 여러 개를 사기그릇에 "또르륵" → reward_gem
- 정리: 앞뒤 무음 자르기 → 노이즈 감소(약하게) → 노멀라이즈 최대 −3dB → 모노 저장

---

## 10. 고르는 기준 (같은 프롬프트로 4~6개 뽑은 뒤)

| 분류 | 합격 | 탈락 |
|---|---|---|
| 배경음 | 처음 10초에 큰 소리 없음, 음량 고름, 30초 틀어 두고 오목 생각이 방해 안 됨, 페이드아웃 전 연주 구간이 길다 | 멜로디가 귀에 꽂힘, 중간에 드럼이 터짐, 보컬·허밍 섞임 |
| 징글 | 정해진 길이 안에 "끝났다" 화음이 분명, 첫 0.1초 안에 소리 시작 | 팡파르처럼 시끄러움, 끝이 애매하게 이어짐 |
| 돌·칩 | 소리 시작이 날카롭고 짧음, 울림·잡음 적음, 폰 스피커로도 또렷 | 꼬리(잔향) 길다, 둔탁, 쇳소리 |
| UI | 0.1초 안팎, 작게 틀어도 들림, 30번 연속 눌러도 안 거슬림 | 높은 "삑" 소리, 음이 너무 뚜렷함 |
| 알림·연출 | 같은 조(C major)로 어울림, 다른 소리와 겹쳐도 지저분하지 않음 | 휴대폰 기본 알림음과 비슷, 너무 김 |

공통: **폰 스피커와 이어폰 둘 다**로 듣기. 같은 분류는 연달아 틀어 보고 질감이 맞는 쪽을 고름.

---

## 11. 만드는 순서 (하루 1~2시간 분량 기준, 팀 추정)

| 날 | 할 일 | 파일 |
|---|---|---|
| 1일 | Suno 요금제 확인(Pro 이상) → 배경음·징글 우선순위 1 | bgm_lobby, bgm_game, jg_win, jg_lose |
| 2일 | Suno Sounds로 우선순위 1 효과음 전부 1차 생성 | ui_tap, ui_open, ui_error, stone_place_1~3, stone_tick, chip_click, seal_lock, seal_break, coin_flip, coin_land, timer_tick, fx_myturn, fx_chime |
| 3일 | 녹음(돌·칩·동전) → Suno 결과와 비교해 고르기 → ui_close 뒤집기 → 자르기·음량 맞추기 → **우선순위 1 (20개) 개발팀 전달** | (우선순위 1 마무리) |
| 4일 | 우선순위 2 배경음·징글 | bgm_tension, bgm_match, jg_draw, jg_tier_up, jg_tier_down |
| 5일 | 우선순위 2 효과음(도장·옥돌은 녹음 비교) → 전달 | ui_toggle, ui_confirm, stone_void, chip_sweep, timer_out, notify, mm_found, reward_stamp, reward_gem, shop_buy, tier_snap |
| 6일 | 우선순위 3 → 전체 음량 다시 맞추기 → 폰으로 한 판 해 보며 점검 → 전달 | bgm_puzzle, bgm_result, jg_tier_top, jg_season, fx_sparkle, shop_equip, emote_pop |

Suno 크레딧이 하루에 얼마나 드는지는 확인 못 함(요금제·Sounds 소모량 모름). 모자라면 날을 나눠서.

---

## 12. 이름 규칙·넘겨주는 방법

- 이름: 소문자 영어 + 밑줄. `bgm_장면` / `jg_이름` / `sfx_계열_이름[_번호]` (7장 표 그대로)
- 폴더: `sounds/bgm/`(bgm·jg), `sounds/sfx/`(sfx), 원본 WAV는 `sounds/raw/`(게임엔 안 올림)
- 후보를 고를 땐 `bgm_lobby_a`, `bgm_lobby_b`처럼 붙였다가, **고른 것만 원래 이름으로**. `v2`·`v3` 같은 버전 번호는 안 붙이고 같은 이름으로 덮어쓰기(덮어쓰면 게임이 새 소리를 씀)
- 형식: mp3. 배경음 128kbps 스테레오, 효과음 96kbps 모노
- `sounds/LICENSES.txt`에 한 줄씩: `파일명 | 도구(Suno 곡/Suno Sounds/녹음/Kenney/ElevenLabs) | 요금제·라이선스 | 만든 날짜 | 원본 링크`
- 넘겨줄 때: 폴더째 압축하거나 GitHub 저장소 `sounds/`에 올림. 일부만 와도 됨(없는 건 합성음이 대신 나옴)

---

## 13. 라이선스 체크리스트

- [ ] Suno: 생성 당시 Pro 이상(무료 때 만든 건 사용 금지). 만든 즉시 내려받아 보관(약관·다운로드 한도 변경 중)
- [ ] ElevenLabs: 유료 플랜에서 생성
- [ ] Freesound: CC0 우선, CC BY면 크레딧 표기, CC BY-NC 금지 / Kenney: CC0
- [ ] 직접 녹음: 제한 없음(남의 음악·TV 소리가 섞이지 않게)
- [ ] 구글 플레이 광고 = 상업적 이용 → 위 조건 필수. 출시 전 [구글 플레이 AI 생성 콘텐츠 정책](https://support.google.com/googleplay/android-developer/answer/14094294) 확인(AI로 만든 배경음 자체를 막는 조항은 이번에 확인 못 함)

---

## 14. 개발팀 연결 메모 (코드 작업은 안 함)

1. **파일 우선, 없으면 합성음**: `snd(키)` 안에서 키→파일 표(7장 "현재 SND" 열)를 보고 파일이 로딩돼 있으면 파일, 아니면 지금 합성음. 피치·음량·반복은 6장 "재생 방법" 열대로
2. 로딩: 우선순위 1 효과음은 첫 화면에서 fetch + `decodeAudioData`로 미리. 배경음은 그 장면에 들어갈 때 불러옴
3. 루프: mp3는 앞뒤에 짧은 빈칸이 붙어 `<audio loop>`면 끊김 → AudioBuffer `loop=true`로 재생
4. 설정: 지금 있는 `bo-snd`(효과음 켜기)·`bo-vib`(진동)에 **배경음 켜기/음량 `bo-bgm`, 효과음 음량 `bo-sfxv`** 추가(기본 배경음 35%, 효과음 70%). 배경음과 효과음 따로 조절
5. 브라우저 정책: 첫 터치 전엔 소리 안 남(이미 처리됨). 배경음도 첫 터치 뒤 시작
6. 진동: 지금처럼 착지 15ms·내 차례 25ms + 10초 경고 30ms·마지막 1초 20ms 추가 제안. 아이폰 사파리는 웹 진동이 안 되는 것으로 알고 있음(검증 못 함) → 소리·화면 효과로 대신
7. 화면 숨김·탭 전환 때 배경음도 멈춤(효과음은 이미 `document.hidden` 검사)
8. 용량 목표: 효과음 37개 합계 약 0.5MB 이하(개당 10~30KB), 배경음 6곡 합계 약 7MB 이하(곡당 1~1.5MB, 나눠서 로딩)
9. **연결이 필요한 곳**: 무승부·무효·관전자(jg_draw), 기권승·나감·부재승(jg_win), 기권패(jg_lose), pick·over·timeout·notify·tierPiece·tierDown 키 호출, +5·+10 칩 소리 통일(규칙 2)
