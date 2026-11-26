# 베팅 오목 음향팀 회의록

- 일시: 2026-11-26
- 안건: 배경음·효과음 전체 목록, Suno로 만들 것 / 다른 방법으로 만들 것 구분, Suno 프롬프트, 게임에 넣을 때 주의점
- 참석(역할): 사운드 디자이너(효과음), 게임 오디오 기획(목록·우선순위·라이선스), 작곡가(배경음·징글), UX 담당(볼륨·설정·접근성·심리전 보호)
- 기준: 담당자 4명 모두 95점 이상일 때 확정
- 실제 코드 작업은 하지 않음(이번 회의는 기획과 프롬프트만)

---

## 1. 회의 전에 확인한 사실 (웹 검색, 2026-11-26 기준)

| 항목 | 확인 내용 | 출처 |
|---|---|---|
| 연주곡(목소리 없는 곡) | Custom 모드에서 **Instrumental** 켜면 목소리 없이 만들어짐 | [blakecrosley Suno 가이드](https://blakecrosley.com/guides/suno) |
| 스타일 입력 | Style 칸에 장르·악기·분위기를 4~7개 정도 쓰는 걸 권장. "~빼 줘" 같은 부정 표현은 잘 안 먹고, 고급 옵션의 **Exclude** 칸을 쓰라고 함. **글자 수 제한은 확인 못 함** | 같은 가이드 |
| 곡 길이 | v5는 최대 약 8분까지 만들 수 있다고 안내. **"정확히 3초로 끝내기" 같은 짧은 길이 지정이 지켜지는지는 확인 못 함** | [Suno 공식 Introducing v5](https://help.suno.com/en/articles/8105153) |
| 편집 기능 | Song Editor에 Extend(이어 만들기), Crop(자르기), Replace Section(구간 다시 만들기)이 있음 | [blakecrosley Suno 가이드](https://blakecrosley.com/guides/suno) |
| 효과음 | **Suno Sounds(베타)** 가 있음: Create → 위쪽 Sounds 탭. 효과음·악기 샘플·환경음 생성. **One Shot(한 번 짧게)** / **Loop(끊김 없이 반복)** 선택, BPM·키(조) 지정 가능, 한 번에 2개씩 나옴. 아직 베타라 정확도는 다듬는 중이라고 공식 안내. **어느 요금제에서 쓸 수 있는지, 최대 길이는 확인 못 함** | [Suno 공식 Suno Sounds](https://help.suno.com/en/articles/10625537) |
| 상업적 이용 | **Pro·Premier(·Platinum) 같은 유료 플랜으로 만든 곡만 상업적 이용 가능.** 무료(Basic)로 만든 곡은 Suno 소유, 비상업용만. 비디오게임에 넣는 것도 상업적 이용에 포함 | [Suno 공식: 상업적 이용](https://help.suno.com/en/articles/2425345), [Suno 공식: 소유권](https://help.suno.com/en/articles/2416769), [Suno 공식: 유료 플랜](https://help.suno.com/en/articles/14617153) |
| 업그레이드·해지 | 유료 구독 중 만든 곡은 해지해도 상업적 이용 유지. **무료일 때 만든 곡은 나중에 업그레이드해도 상업용이 되지 않음** | [Suno 공식: 소유권](https://help.suno.com/en/articles/2416769), [dynamoi 정리](https://dynamoi.com/learn/ai-music-distribution/suno-commercial-rights-explained) |
| 다운로드 제한·향후 변경 | 2026년부터 다운로드 횟수 제한(무료는 매우 적거나 없음, 유료는 월 한도)이 생긴다는 보도. 앞으로 나올 라이선스 모델은 조건이 달라질 수 있다고 함. **정확한 현재 한도는 출처마다 달라 확인 못 함 → [가격 페이지](https://suno.com/pricing)에서 직접 확인 필요** | [dynamoi 정리](https://dynamoi.com/learn/ai-music-distribution/suno-commercial-rights-explained), [blakecrosley 가이드](https://blakecrosley.com/guides/suno) |
| ElevenLabs 효과음 | 효과음 생성 도구. 무료 플랜 결과물은 상업적 이용 불가(출처 표기 필요), 유료 플랜이면 게임·앱에 넣어 쓸 수 있음. 효과음 파일만 따로 파는 건 금지 | [ElevenLabs 도움말](https://help.elevenlabs.io/hc/en-us/articles/13313564601361), [ElevenLabs 효과음 약관](https://elevenlabs.io/sound-effects-terms) |
| 무료 효과음 | Freesound는 CC0·CC BY는 상업 게임에 가능(BY는 출처 표기), **CC BY-NC는 상업 불가**. Kenney 에셋은 CC0(표기 불필요). Pixabay는 표기 없이 사용 가능하나 일부는 Content ID 등록돼 있을 수 있음 | [Cinevva 게임 사운드 라이선스 정리](https://app.cinevva.com/guides/free-sound-effects-music), [Kenney Interface Sounds](https://kenney.nl/assets/interface-sounds), [Kenney Casino Audio](https://kenney.nl/assets/casino-audio) |

**모른다고 적어 둘 것**
- 사용자가 지금 Suno **어느 플랜**인지 모름 → 무료라면 게임(광고 붙인 구글 플레이 출시 포함)에 넣으면 안 됨. 만들기 **전에** Pro 이상인지 확인.
- Suno로 만든 곡이 끝과 처음이 자연스럽게 이어지는 "루프"로 나오는지는 공식 안내가 없음(Sounds의 Loop 모드는 있음). → 직접 잘라서 이어 붙이는 작업이 필요하다고 보고 계획함.
- Suno Sounds 결과물에도 일반 곡과 같은 상업적 이용 조건이 적용되는지 따로 명시된 문장은 못 찾음(유료 플랜 조건을 따를 것으로 보이지만 확정 아님).

---

## 2. 안 비교 → 결정

| 안 | 내용 | 장점 | 단점 |
|---|---|---|---|
| A. 전부 Suno | 배경음·징글·효과음 모두 Suno(Sounds 포함) | 도구 하나, 분위기 통일 | 효과음은 베타라 '딱' 같은 짧고 깨끗한 소리가 잘 안 나올 수 있음, 앞뒤 잔향·잡음 정리 필요 |
| B. 섞어 쓰기 | **음악은 Suno**, **돌·칩은 직접 녹음**, **버튼·알림은 Kenney(CC0) 또는 ElevenLabs**, Suno Sounds는 '시도해 볼 것'으로 | 각 소리에 가장 잘 맞는 방법, 실제 바둑돌 소리가 게임의 얼굴이 됨 | 도구가 여러 개, 라이선스 기록 관리 필요 |
| C. 전부 무료 라이브러리 | Freesound·Pixabay·Kenney만 | 돈이 안 듦 | 배경음 분위기 통일이 어렵고, 남들 게임과 같은 소리가 됨, 라이선스 하나하나 확인 |

**결정: B안.**
- 근거1: 착수음은 이 게임에서 가장 많이 듣는 소리(한 턴에 돌 3개) → 진짜 바둑돌 녹음이 품질·고유성 모두 1등.
- 근거2: Suno는 음악 생성기로서 확실하고, 효과음(Sounds)은 공식적으로 베타 → 효과음을 Suno에만 걸면 위험.
- 근거3: 버튼 클릭류는 이미 CC0 팩이 충분하고, 표기 의무도 없음.
- 보완: Suno Sounds로도 같은 효과음을 한 번씩 뽑아 보고, 녹음/팩보다 좋으면 바꿔 씀(비교용 프롬프트를 5장에 둠).

**사운드 콘셉트(작곡가 제안 → 전원 합의): "조용한 옥(玉) 대국실"**
- 차분한 제이드 그린·다크 모드에 맞춰 **피아노 + 은은한 가야금/대금 + 부드러운 패드**. 국악 느낌은 '살짝'만(과하면 사극처럼 들림).
- 대국 배경음은 **멜로디를 거의 없게**(생각을 방해하지 않게). 템포 70~96 BPM.
- 대국·긴장·매칭 배경음은 **같은 조(A minor)** 로 맞춰서 서로 자연스럽게 넘어가게(크로스페이드).
- 시끄러운 EDM 드롭, 보컬, 일렉 기타는 전부 제외.

---

## 3. 점수 (1차 → 수정 → 최종)

### 1차 점수 (초안 기준)
| 담당 | 점수 | 지적 |
|---|---|---|
| 사운드 디자이너 | 86 | 착수 소리가 한 개뿐 → 한 턴에 3개 연속으로 나면 기계처럼 들림. 6목 무효 소리가 '실패음'처럼 너무 셈 |
| 게임 오디오 기획 | 84 | Suno 플랜 확인 없이 "Suno로 다 만들자"로 시작 → 무료 플랜이면 출시 불가. 라이선스 기록 방법 없음 |
| 작곡가 | 88 | 징글을 일반 곡으로 만들면 1~2분짜리가 나와 자르기 어려움. 배경음끼리 조가 달라 전환이 어색 |
| UX 담당 | 82 | **칩 거는 소리가 금액에 따라 달라지면, 같은 방에서 하는 상대에게 내 베팅이 소리로 새어 나감(심리전 훼손).** 첫 터치 전 소리 막힘 대책 없음, 진동 대안 없음 |

### 수정한 내용
1. 착수음 **3~4가지 변형** 녹음 + 개봉 때 A→B→C 순서로 0.12~0.15초 간격으로 재생(긴장감 연출, 겹침 방지).
2. 6목 무효는 '실패 부저' 대신 **낮고 짧은 나무 '툭' + 살짝 내려가는 음** 으로(빨간 줄 연출과 함께, '무효' 글씨처럼 한 번만).
3. 시작 전 체크: **Suno 유료 플랜 확인 → 그 뒤에 생성**. `sounds/LICENSES.txt`에 파일별 출처·플랜·날짜 기록 규칙 추가.
4. 징글은 **Suno Sounds One Shot을 먼저**, 안 되면 일반 곡으로 만들고 앞부분 3~5초 Crop.
5. 대국·긴장·매칭 배경음은 A minor 통일, 로비는 C major(같은 음 계열이라 넘어가도 안 어색).
6. **칩 소리는 금액과 상관없이 한 번 탭 = 같은 소리 1번**, 봉인·개봉도 금액 무관. 상대의 칩 조작 소리는 절대 안 냄(상대 봉인 '완료' 알림만). 이어폰 없는 대면 플레이도 고려.
7. 첫 터치 전 소리 막힘 대책, 소리 설정(배경음/효과음 따로), 진동 대체를 기술 메모에 추가.

### 최종 점수
| 담당 | 점수 | 95점 이상 근거 |
|---|---|---|
| 사운드 디자이너 | 96 | 핵심 소리(돌·칩)는 실제 녹음으로 고유성 확보, 변형·간격 재생으로 반복 피로 해결, 무효음 톤 조정, 녹음 방법 구체화 |
| 게임 오디오 기획 | 95 | 우선순위 1·2·3로 나눠 1단계만으로도 게임이 완성되게 함, 플랜·라이선스 확인을 생성 '전' 단계로 이동, 확인 못 한 것 명시 |
| 작곡가 | 96 | 콘셉트 하나로 전 곡 통일, 조 통일로 전환 해결, 곡마다 Style·Exclude·루프 자르는 법·고르는 기준 제공 |
| UX 담당 | 97 | 심리전 정보가 소리로 새지 않게 규칙화, 기본 볼륨 낮게(무난한 톤), 첫 터치·무음 모드·진동·설정 분리까지 정리 |

---

## 4. 소리 목록

길이는 목표치. 루프 = 끊김 없이 반복.

### 4-1. 배경음(BGM)·징글

| 우선 | 이름 | 쓰는 순간 | 길이 | 느낌 | 루프 | 만드는 도구 |
|---|---|---|---|---|---|---|
| 1 | 로비 | 메인·상점·친구·출석 화면 | 60~90초 | 편안, 고급, 따뜻 | O | Suno |
| 1 | 대국 중 | 대국 화면 기본 | 60~90초 | 집중, 미스터리, 아주 조용 | O | Suno |
| 1 | 승리 징글 | 승리 화면 진입 | 3~5초 | 밝고 품위 있게 | X | Suno(Sounds 먼저) |
| 1 | 패배 징글 | 패배 화면 진입 | 2~4초 | 담담, 슬프거나 우스꽝스럽지 않게 | X | Suno(Sounds 먼저) |
| 2 | 긴장 구간 | 누군가 4목(마지막 위협)이 생겼을 때 대국 BGM에서 크로스페이드 | 30~60초 | 낮은 긴장, 심장박동 | O | Suno |
| 2 | 랭크 매칭 대기 | 매칭 찾는 중(최대 20초) | 20~30초 | 기대감, 가벼운 긴장 | O | Suno |
| 2 | 승급 징글 | 티어 승급(문양 조립 연출) | 4~6초 | 웅장하지만 절제 | X | Suno |
| 3 | 오늘의 묘수 풀이 | 묘수 풀이 화면 | 60초 | 고요, 사색 | O | Suno |
| 3 | 강등 징글 | 티어 강등 | 2~3초 | 담담 | X | Suno(Sounds) |

### 4-2. 효과음(SFX)

| 우선 | 이름 | 쓰는 순간 | 길이 | 느낌 | 루프 | 1순위 도구 | 대안 |
|---|---|---|---|---|---|---|---|
| 1 | 착수(돌 놓기) ×3~4종 | 개봉 후 돌이 놓일 때(A→B→C 간격 재생) | 0.15~0.4초 | 맑고 단단한 '딱' | X | **직접 녹음** | ElevenLabs, Suno Sounds |
| 1 | 칸 지정 | 선 플레이어가 A·B·C 칸 고를 때 | 0.1초 | 아주 가벼운 나무 '똑' | X | Kenney/녹음(판 손가락 톡) | ElevenLabs |
| 1 | 칩 걸기 | 칩 +/− 누를 때(금액 무관 같은 소리) | 0.1~0.2초 | 작은 '착' | X | **직접 녹음**(포커칩/바둑알 통) | Kenney Casino Audio |
| 1 | 봉인 | 내 베팅 봉인 버튼 | 0.4~0.6초 | 닫히는 '착' + 짧은 잠금음 | X | ElevenLabs | Kenney + 녹음 합성 |
| 1 | 상대 봉인 완료 | 상대가 봉인했을 때(정보 없이 상태만) | 0.2~0.3초 | 낮고 작은 '톡' | X | Kenney | ElevenLabs |
| 1 | 개봉 | 동시 개봉 순간 | 0.6~1초 | 짧은 '스윽' 바람 + 맑은 울림 | X | ElevenLabs | Suno Sounds |
| 1 | 버튼 탭 | 일반 버튼 | 0.05~0.1초 | 부드럽고 작은 클릭 | X | Kenney Interface Sounds | 직접 합성 |
| 1 | 타이머 경고 | 남은 시간 5초부터 1초마다 | 0.1초 | 작은 '틱'(마지막 1초만 살짝 높게) | X | Kenney | ElevenLabs |
| 1 | 오목 완성 | 5목 완성(승리 징글 직전) | 0.8~1.2초 | 돌 '딱' + 맑은 종소리 | X | 녹음 돌 + ElevenLabs 종 합성 | Suno Sounds |
| 1 | 동전 던지기 | 선 정하기 | 0.8~1.5초 | 튕김 '팅' + 굴러 멈춤 | X | 직접 녹음(실제 동전) | Kenney/Freesound CC0 |
| 2 | 6목 무효 | 6목 이상 빨간 줄 | 0.5~0.8초 | 낮은 '툭' + 살짝 내려가는 음, 부저 X | X | ElevenLabs | Suno Sounds |
| 2 | 출석 도장 | 출석체크 '쾅' | 0.3~0.5초 | 묵직한 도장 '쾅'(저음 위주) | X | **직접 녹음**(도장·책상) | ElevenLabs |
| 2 | 보상 받기(옥돌) | 옥돌 획득 | 0.5~0.8초 | 옥돌 구르는 '또르륵' + 반짝 | X | 녹음(바둑알 여러 개 떨어뜨리기) | ElevenLabs |
| 2 | 구매 완료 | 상점 구매 | 0.4~0.6초 | 차분한 '찰칵' + 짧은 화음 | X | ElevenLabs | Kenney |
| 2 | 알림(친구 채팅·대국 신청) | 새 메시지·신청 | 0.3~0.5초 | 맑은 2음 '띵동' 작게 | X | Kenney | ElevenLabs |
| 2 | 불가/오류 | 이어지지 않은 칸 선택 등 | 0.15초 | 낮고 짧은 '툭' | X | Kenney | ElevenLabs |
| 2 | 승급 문양 조립 | 문양이 '촥촥' 맞춰질 때(징글 아래) | 조각마다 0.1~0.2초 | 금속/옥 '착' 연속 | X | ElevenLabs | Suno Sounds |
| 3 | 이모트 | 이모트 보내기/받기 | 0.2~0.4초 | 귀엽지 않게, 작은 '뽁' | X | Kenney | ElevenLabs |
| 3 | 탭 전환·창 열기/닫기 | 메뉴 이동, 팝업 | 0.1~0.2초 | 부드러운 '슉' | X | Kenney | 직접 합성 |
| 3 | 토글(켜기/끄기) | 설정 스위치 | 0.05초 | 작은 '딸깍' | X | Kenney | 직접 합성 |

---

## 5. Suno 프롬프트 (전체)

### 공통 사용법
1. **요금제 확인**: Pro 이상에서 만들어야 게임에 쓸 수 있음(무료 때 만든 건 나중에 업그레이드해도 상업용 안 됨).
2. Create → **Advanced(Custom)** → **Instrumental 켜기** → Style 칸에 아래 영어 원문 붙여넣기 → 가사 칸은 비움.
3. **Exclude 칸(고급 옵션)** 공통: `vocals, choir, EDM drop, distorted guitar, heavy drums, rap`
4. 같은 프롬프트로 **2~3번(=4~6곡)** 뽑아서 아래 '고르는 기준'으로 1개 선택.
5. 마음에 드는 곡이 길면 Song Editor의 **Crop**으로 줄이고, 루프는 6장 방법으로 정리.

### 고르는 공통 기준 (배경음)
- 처음 10초에 **갑자기 큰 소리·드럼 필인**이 없는 것
- 대국 중에 30초 틀어 놓고 **오목 생각이 방해 안 되는 것**(멜로디가 귀에 꽂히면 탈락)
- **음량이 처음부터 끝까지 고른 것**(중간에 크게 터지면 탈락)
- 끝부분이 **페이드아웃되지 않고** 연주가 이어지는 구간이 있는 것(루프 자르기 쉬움)
- 폰 스피커로 들었을 때 저음이 뭉개지지 않는 것

---

### [우선순위 1] 로비 BGM
- Instrumental: **켜기**
- 제목 예시: `Jade Hall Lobby`
- Style:
```
calm elegant ambient, soft felt piano, gentle gayageum plucks, warm pads, 72 BPM, C major, minimal, relaxed, loopable
```
- 길이·루프: 1~2분 곡이 나오면 인트로 뒤 **안정된 60~90초 구간**만 잘라 루프. 박자 단위(72 BPM이면 4마디≈13.3초)로 자르면 이음새가 자연스러움.
- 고르는 기준: 피아노가 주인공이고 가야금은 '양념'인 것. 국악 느낌이 너무 강하면 탈락.

### [우선순위 1] 대국 중 BGM
- Instrumental: **켜기**
- 제목 예시: `Quiet Board`
- Style:
```
minimal focused ambient, deep soft pads, sparse wooden plucks, light ticking percussion, 80 BPM, A minor, mysterious, calm
```
- 길이·루프: 60~90초 루프. 80 BPM이면 4마디=12초 → 60초(20마디) 또는 84초(28마디)로 자르기.
- 고르는 기준: **멜로디가 거의 없는 것**이 1등. 착수 '딱' 소리와 음역이 겹치지 않게 고음 타악기가 적은 것.

### [우선순위 1] 승리 징글
- 1차 시도: **Suno Sounds → One Shot**, 프롬프트에 그대로 넣기
- 2차(안 되면): Advanced + Instrumental 켜기로 만든 뒤 **앞 3~5초 Crop**, 끝 0.5초 페이드아웃
- 제목 예시: `Jade Victory`
- Style:
```
short victory sting, warm strings and soft brass, gayageum flourish, bright major chord ending, elegant, 4 seconds
```
- 고르는 기준: 4초 안에 '끝났다'는 느낌(마지막 화음)이 분명한 것, 팡파르처럼 시끄럽지 않은 것.

### [우선순위 1] 패배 징글
- 1차: Suno Sounds One Shot / 2차: Advanced + Instrumental 후 Crop
- 제목 예시: `Quiet Defeat`
- Style:
```
short gentle defeat sting, soft descending piano, low cello, minor chord, calm, dignified, 3 seconds
```
- 고르는 기준: 슬프거나 '뿌잉' 같은 우스운 느낌이 아니라 **담담하게 마무리**되는 것(다시 하고 싶게).

### [우선순위 2] 긴장 구간 BGM (마지막 위협)
- Instrumental: **켜기**, 제목 예시: `Last Threat`
- Style:
```
dark minimal suspense, pulsing low synth, soft heartbeat kick, clock ticks, tense strings, 96 BPM, A minor, restrained
```
- 길이·루프: 30~60초 루프. 대국 BGM과 같은 A minor라 1~2초 크로스페이드로 넘어감.
- 고르는 기준: 무섭지 않고 '조여 오는' 정도. 심장박동 킥이 너무 크면 탈락(타이머 '틱'과 겹침).

### [우선순위 2] 랭크 매칭 대기
- Instrumental: **켜기**, 제목 예시: `Finding Rival`
- Style:
```
light anticipation loop, soft pulsing plucks, airy pads, subtle ticking, 90 BPM, A minor, hopeful suspense, minimal
```
- 길이·루프: 대기 최대 20초 → **20~30초 루프** 하나면 충분. Suno Sounds의 **Loop + BPM 90 + A minor** 로도 시도해 볼 것.
- 고르는 기준: 반복돼도 초조하지 않은 것.

### [우선순위 2] 승급 징글
- 1차: Suno Sounds One Shot / 2차: Advanced + Instrumental 후 Crop
- 제목 예시: `Tier Ascend`
- Style:
```
rising ceremonial sting, deep taiko hit, shimmering bells, string swell, majestic but tasteful, bright ending, 5 seconds
```
- 고르는 기준: 문양 조립 애니메이션(약 1~2초) 뒤에 '쾅'하고 정점이 오는 구조. 정점 위치를 애니메이션 타이밍에 맞춰 자르기.

### [우선순위 3] 오늘의 묘수 풀이
- Instrumental: **켜기**, 제목 예시: `Daily Myosu`
- Style:
```
contemplative zen ambient, breathy daegeum flute, soft piano, slow 64 BPM, D minor, quiet, thoughtful, spacious
```

### [우선순위 3] 강등 징글
- Suno Sounds One Shot, 제목 예시: `Tier Down`
- Style:
```
short soft descending chime, muted piano, low warm pad, minor, calm, gentle, 2 seconds
```

---

### 효과음 – Suno Sounds로 '시도해 볼 것' (One Shot 선택)
결과가 녹음/Kenney보다 좋을 때만 바꿔 씀. 한 번에 2개씩 나오니 2번(4개) 뽑아 비교.

| 소리 | Suno Sounds 프롬프트 |
|---|---|
| 착수 | `single go stone placed on wooden go board, crisp clack, close mic, dry, no reverb, very short` |
| 개봉 | `soft airy whoosh reveal with gentle glass chime, elegant, 1 second, clean` |
| 오목 완성 | `crisp wooden stone clack followed by clear bright bell chime, short, elegant` |
| 6목 무효 | `low muted wooden knock with soft descending tone, short, not harsh, no buzzer` |
| 승급 문양 조립 | `series of quick jade stone clicks locking together, metallic shimmer, 1.5 seconds` |

### 효과음 – ElevenLabs Sound Effects용 프롬프트 (유료 플랜에서 생성)
| 소리 | 프롬프트 |
|---|---|
| 착수(녹음 대안) | `A single slate go stone firmly placed on a thick wooden go board, sharp clean clack, close-up, dry room, 0.3 seconds` |
| 칩 걸기(대안) | `One plastic poker chip tapped onto a small stack, short soft click, close-up, 0.15 seconds` |
| 봉인 | `A small wooden box lid closing with a soft latch click, satisfying, short, 0.5 seconds` |
| 개봉 | `Quick soft whoosh followed by a light crystal shimmer, reveal moment, elegant, 0.8 seconds` |
| 오목 완성(종) | `Single clear temple bell chime, gentle, bright, short decay, 1 second` |
| 6목 무효 | `Low dull wooden thud with a slight downward pitch, subtle error, not alarming, 0.6 seconds` |
| 출석 도장 | `Heavy wooden rubber stamp slammed on paper on a desk, deep thump, 0.4 seconds` |
| 보상(옥돌) | `A few small glass stones rolling and clinking into a ceramic bowl, bright sparkle, 0.7 seconds` |
| 구매 완료 | `Purchase confirmation, gentle soft click followed by a warm two-note chime, calm, 0.5 seconds` |
| 알림 | `Soft two-note notification chime, clear, calm, mobile app, 0.4 seconds` |
| 승급 문양 조립 | `Rapid sequence of jade pieces snapping into place, crisp clicks, rising, 1.5 seconds` |

---

## 6. 루프 만들기·자르기 팁 (작곡가)
1. 무료 편집기 **Audacity**(https://www.audacityteam.org/download/)에 Suno 파일(가능하면 WAV)을 넣는다.
2. 인트로(곡 처음 몇 초)와 엔딩(페이드아웃)을 버리고, **연주가 꽉 찬 가운데 구간**을 고른다.
3. BPM으로 마디 길이 계산: `1마디(4박) = 240 ÷ BPM 초` → 72 BPM=3.33초, 80 BPM=3초, 90 BPM=2.67초, 96 BPM=2.5초. **마디의 정수배**로 자른다.
4. 자르는 점은 파형이 0을 지나는 곳(Audacity: 선택 후 `Z` 키 = 영점 찾기)으로 맞춰 '틱' 소리 방지.
5. 처음과 끝을 이어 붙여 10번 반복해 들어 보고 튀면 위치를 1박씩 옮긴다.
6. 징글은 끝에 0.3~0.5초 페이드아웃만, 앞부분은 무음 0.05초 이내로 바짝 자른다(눌렀는데 늦게 나는 느낌 방지).

---

## 7. 직접 녹음 방법 (사운드 디자이너)
- **장비**: 폰 녹음 앱(기본 녹음기면 충분, 가능하면 '고음질/무손실' 설정). 폰은 소리 나는 곳에서 **20~30cm**.
- **장소**: 옷장 안이나 이불·커튼 많은 방(울림 적게), 냉장고·에어컨 끄기, 밤에 조용할 때.
- **바둑돌 착수**: 실제 바둑판(없으면 두꺼운 원목 도마). 손가락 끝으로 **같은 세기로 15~20번**, 세기를 조금씩 바꿔 또 15번. 그중 좋은 3~4개를 변형으로 사용. 흑돌·백돌 둘 다 녹음(소재가 다르면 소리도 다름 — 흑/백 소리를 구분하면 더 고급).
- **칩**: 포커칩이 있으면 1개를 칩 더미에 '톡'. 없으면 바둑알을 바둑통에 1개 떨어뜨리기.
- **동전**: 500원 동전을 책상 위로 튕겨 굴러 멈출 때까지.
- **도장**: 나무 도장을 종이 깐 책상에 '쾅'. 너무 세면 소리가 찢어지니 입력이 빨간색까지 안 가게.
- **옥돌 보상**: 바둑알 여러 개를 사기그릇에 '또르륵'.
- **정리**: Audacity에서 ① 앞뒤 무음 자르기 ② 잡음 제거(효과 → 노이즈 감소, 약하게) ③ 노멀라이즈(최대 −3dB) ④ 모노로 저장.
- **장점**: 직접 녹음한 소리는 라이선스 걱정이 없고, 다른 게임과 겹치지 않음.

---

## 8. 라이선스 체크리스트 (게임 오디오 기획)
- [ ] Suno: **생성할 때 Pro 이상**이었는지(곡 만든 날짜와 구독 기간 기록). 무료 때 만든 곡은 사용 금지.
- [ ] ElevenLabs: **유료 플랜에서 생성**했는지. 무료 결과물은 상업 불가.
- [ ] Freesound: 파일마다 **CC0인지** 확인(CC BY면 앱 '정보/크레딧'에 작성자 표기, **CC BY-NC는 사용 금지**).
- [ ] Kenney: CC0(표기 불필요, 그래도 크레딧에 감사 표기 권장).
- [ ] Pixabay: 사용 가능하지만 소리 파일만 따로 배포·판매 금지. 일부 곡은 유튜브 Content ID에 걸릴 수 있음(게임 홍보 영상 올릴 때 주의).
- [ ] `sounds/LICENSES.txt` 에 `파일명 | 출처(도구/사이트) | 플랜·라이선스 | 만든 날짜 | 원본 링크` 기록.
- [ ] 구글 플레이: 광고를 붙이면 상업적 이용이므로 위 조건 필수. (구글 플레이 정책에서 'AI로 만든 배경음 자체'를 막는 조항은 이번에 확인하지 못함 — 생성형 AI 정책은 주로 앱 안에서 AI가 콘텐츠를 만들어 주는 기능 대상이라고 알고 있으나, 출시 전 [구글 플레이 AI 생성 콘텐츠 정책](https://support.google.com/googleplay/android-developer/answer/14094294) 확인 권장.)
- [ ] Suno 약관은 2026년 바뀌는 중(라이선스 모델 전환·다운로드 한도). **만든 파일은 바로 내려받아 보관**.

---

## 9. 기술 메모 (짧게, UX·개발 참고)
1. **파일 형식**: 기본 **mp3**(모든 브라우저 지원). 배경음 128kbps 스테레오, 60~90초 ≈ **1~1.5MB 이하**. 효과음 모노 96kbps, 개당 **10~30KB**, 효과음 전체 **300KB 이하** 목표.
2. **mp3 루프 주의**: mp3는 앞뒤에 아주 짧은 빈칸이 붙어 `<audio loop>`로 돌리면 '뚝' 끊김이 생길 수 있음 → Web Audio API로 디코딩해 `loop` 재생(또는 m4a 함께 준비).
3. **불러오기 순서**: 효과음 P1은 첫 화면에서 미리 로딩, 배경음은 필요할 때 로딩(첫 화면 빨리 뜨게).
4. **볼륨 균형(기본값)**: 배경음 **35~40%**, 효과음 **70%**. 효과음이 배경음보다 확실히 크게. 징글이 나올 때 배경음은 잠깐 줄였다가(덕킹) 복귀. 착수음이 기준(가장 또렷), 버튼음은 그보다 작게.
5. **브라우저 자동재생 정책**: 사용자가 **화면을 한 번 터치/클릭하기 전에는 소리가 막힘**(크롬·사파리 공통). → 첫 터치(시작 버튼 등) 때 오디오를 '깨우고' 그 뒤에 로비 BGM 시작.
6. **설정 메뉴**: 전체 소리 끄기 / 배경음 슬라이더 / 효과음 슬라이더 / 진동 켜기·끄기. 값은 기기에 저장(다음 접속 때 유지).
7. **진동**: 착수(짧게 10~20ms), 개봉, 오목 완성, 타이머 마지막 3초에만. 안드로이드 크롬은 진동 API 지원, **아이폰 사파리는 웹 진동이 안 되는 것으로 알고 있음**(이번에 따로 검증은 못 함) → 아이폰은 소리·화면 효과로 대체.
8. **기타**: 앱이 뒤로 가거나 탭을 바꾸면 배경음 일시정지. 아이폰 무음 스위치를 켜면 웹 소리가 안 날 수 있음(기기별 확인 필요). 같은 효과음이 동시에 여러 번 겹치지 않게 최소 간격(약 50ms).
9. **심리전 보호(필수)**: 칩·봉인·개봉 소리는 **금액과 무관하게 항상 같은 소리**. 상대의 칩 조작은 소리로 알리지 않고 '봉인 완료'만.

---

## 10. 작업 순서 제안
1. Suno 플랜 확인(Pro 이상) → 2. 우선순위 1 배경음·징글 4개 생성·선택 → 3. 바둑돌·칩·동전 녹음 → 4. Kenney Interface Sounds 내려받아 버튼·타이머·알림 고르기 → 5. 봉인·개봉·오목 완성은 ElevenLabs 또는 Suno Sounds로 → 6. Audacity로 자르기·음량 맞추기 → 7. 게임에 넣기(개발팀) → 8. 우선순위 2·3 순서로 추가.
