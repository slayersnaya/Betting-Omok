# 베팅 오목

세 칸을 고르고 점수를 몰래 걸어 돌을 놓는 2인 전략 오목입니다.

- 바로 하기: https://slayersnaya.github.io/Betting-Omok/
- 개인정보처리방침: https://slayersnaya.github.io/Betting-Omok/privacy.html
- 문의: slayersnaya@gmail.com · [Issues](https://github.com/slayersnaya/Betting-Omok/issues)

## 구성

| 파일 | 내용 |
|---|---|
| `index.html` | 게임 전체(빌드 결과물). 수정은 원본에서 하고 `tools/build_web.py`로 다시 만듦 |
| `firestore.rules` | Firebase 보안 규칙. 바꾸면 Firebase 콘솔 → Firestore → 규칙에 붙여 넣고 게시 |
| `sw.js`, `manifest.json`, `icons/` | 설치형 웹앱(PWA) 파일 |
| `version.json` | 배포 버전. 앱이 이 값으로 새 버전 알림을 띄움 |
| `privacy.html` | 개인정보처리방침 |
| `tools/` | 빌드 스크립트와 Firebase 연결 코드 원본 |

## 서버

- Firebase(Spark 무료 요금제): 익명·구글 로그인, Firestore(서울)
- 서버 함수는 쓰지 않음. 공정성은 '봉인(해시) → 공개' 방식과 보안 규칙(기록 추가만 허용, 서버 시각 검사)으로 지킴

## 알려진 한계(서버 함수 없이 생기는 것)

- 각 턴이 끝나 베팅을 공개하면, 상대 기기는 그 값으로 남은 점수를 계산할 수 있습니다(화면에는 보여 주지 않음).
- 구글 계정 두 개로 일부러 져 주는 랭크 조작은 완전히 막을 수 없습니다. 같은 상대와 하루에 여러 번 두면 반영을 줄여 효과를 낮춥니다.
