#!/bin/bash
# 배포할 때마다 같이 실행: 고치기 쉬운 원본·빌드 도구·가짜 서버·테스트·AI 학습 도구를 저장소 dev/ 폴더에 백업
set -e
R=/home/claude/gh-betting-omok/dev
rm -rf $R && mkdir -p $R/src $R/firebase $R/tests/bt $R/ai $R/notes
cp /home/claude/betting-omok/index.html $R/src/index.html
cp /home/claude/web/firestore.rules $R/src/firestore.rules
cp /home/claude/firebase/*.py /home/claude/firebase/*.js $R/firebase/ 2>/dev/null || true
cp -r /home/claude/firebase/fake $R/firebase/fake
cp /home/claude/tests/*.py $R/tests/ 2>/dev/null || true
cp /tmp/bt/*.py $R/tests/bt/ 2>/dev/null || true
cp /tmp/feattest_m.py $R/tests/ 2>/dev/null || true
cp /home/claude/eval/friend/friendtest.py $R/tests/friendtest_base.py 2>/dev/null || true
cp /home/claude/backup.sh $R/
# AI: 코드·문서·스크립트만(큰 기록 파일 제외)
cd /home/claude/eval/ai && find . -maxdepth 3 \( -name '*.js' -o -name '*.md' -o -name '*.sh' -o -name '*.diff' \) -size -400k -print0 | xargs -0 -I{} cp --parents {} $R/ai/
# 팀 회의록·기획서
for d in econ shop gd2 gd3 friend feat rank3 emb; do [ -f /home/claude/eval/$d/meeting.md ] && cp /home/claude/eval/$d/meeting.md $R/notes/$d-meeting.md; [ -f /home/claude/eval/$d/plan.md ] && cp /home/claude/eval/$d/plan.md $R/notes/$d-plan.md; done
cat > $R/README.md <<'MD'
# 개발용 백업 (자동)
배포할 때마다 함께 갱신됨. 게임 실행에는 쓰이지 않음(웹은 저장소 맨 위의 index.html).
- src/index.html: 고치기 쉬운 원본 → firebase/build_web.py 로 빌드하면 웹용 index.html
- src/firestore.rules: Firebase 콘솔에 게시하는 서버 규칙
- firebase/: 빌드 도구·Firebase 연결(fb-adapter.js)·테스트용 가짜 Firebase(fake/)
- tests/: 자동 테스트(Playwright)
- ai/: AI(Ultimate) 학습·평가 도구와 기록 문서
- notes/: 팀 회의록·기획서
MD
du -sh $R | cut -f1
