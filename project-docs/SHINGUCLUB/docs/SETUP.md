# SHINGUCLUB — Setup / Deploy 가이드

## 1. 사전 요구사항

- Node.js 18 이상
- npm
- Firebase 프로젝트 (Authentication, Firestore, Storage 사용)

## 2. 클론 및 설치

```bash
git clone https://github.com/baejooho/SHINGUCLUB.git
cd SHINGUCLUB
npm install
```

## 3. Firebase 설정

현재는 `firebase/config.js`에 Firebase 웹 설정이 들어 있다.
학습용으로 동작하지만, **운영/공개 저장소에서는 환경변수로 분리**하는 것을 권장한다.

권장 형태 예시 (`.env.local`):

```bash
NEXT_PUBLIC_FIREBASE_API_KEY=...
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=...
NEXT_PUBLIC_FIREBASE_PROJECT_ID=...
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=...
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=...
NEXT_PUBLIC_FIREBASE_APP_ID=...
```

Firebase Console에서 확인할 항목:
- Authentication: Email/Password 활성화
- Firestore: `clubs`, `clubApplications` 등 컬렉션
- (선택) Storage, EmailJS 키

## 4. 실행

```bash
npm run dev
```

`http://localhost:3000` 접속.

## 5. 빌드

```bash
npm run build
npm start
```

## 6. 배포 (권장: Vercel)

1. GitHub 저장소 연결
2. Framework Preset: Next.js
3. 환경변수에 Firebase 공개 설정 등록
4. Deploy

## 7. 주의사항

- Firebase 웹 API 키는 “비밀키”와 다르지만, Firestore Rules가 약하면
  데이터 노출/변조 위험이 있다. Rules를 반드시 점검한다.
- 회장 권한은 클라이언트 체크와 Rules를 함께 적용하는 것이 안전하다.
