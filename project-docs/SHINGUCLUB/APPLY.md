# SHINGUCLUB에 적용 방법

본인 PC의 SHINGUCLUB 레포에서:

```bash
cp firebase/config.js /path/to/SHINGUCLUB/firebase/config.js
cp uploadClubs.js /path/to/SHINGUCLUB/uploadClubs.js
cp .env.example /path/to/SHINGUCLUB/.env.example
# .gitignore에 !.env.example 추가되어 있는지 확인
cp .env.example /path/to/SHINGUCLUB/.env.local
# .env.local에 기존 Firebase 값 입력 후
cd /path/to/SHINGUCLUB && npm run dev
```

`.env.local`은 절대 GitHub에 push하지 말 것.
