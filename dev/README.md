# 개발용 백업 (자동)
배포할 때마다 함께 갱신됨. 게임 실행에는 쓰이지 않음(웹은 저장소 맨 위의 index.html).
- src/index.html: 고치기 쉬운 원본 → firebase/build_web.py 로 빌드하면 웹용 index.html
- src/firestore.rules: Firebase 콘솔에 게시하는 서버 규칙
- firebase/: 빌드 도구·Firebase 연결(fb-adapter.js)·테스트용 가짜 Firebase(fake/)
- tests/: 자동 테스트(Playwright)
- ai/: AI(Ultimate) 학습·평가 도구와 기록 문서
- notes/: 팀 회의록·기획서
