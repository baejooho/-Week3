# 늘봄 (Elder Care App) — 독거노인 AI 안심케어 서비스

독거 어르신과 보호자를 연결하는 AI 안심케어 애플리케이션
(학교 팀 프로젝트)

## 프로젝트 개요

늘봄은 홀로 생활하는 어르신의 일상 대화·상태 확인을 돕고,
보호자가 원격으로 안심할 수 있도록 만든 케어 서비스이다.

- **어르신 앱**: 역할 선택 후 로그인, AI 대화, 통화/이력, 건강 관련 화면
- **보호자 앱**: 어르신 목록·상세, 알림, 계정 관리
- **백엔드**: Spring Boot 기반 API + Gemini AI 대화 + FCM 푸시

프론트(모바일)는 Flutter로 구현했으며, 백엔드는 Java/Spring Boot,
데이터는 PostgreSQL, 푸시는 Firebase Cloud Messaging을 사용한다.

자세한 기획은 [docs/PLANNING.md](docs/PLANNING.md)를 참고한다.

## 주요 기능

- 어르신 / 보호자 역할 분리 및 로그인·회원가입
- AI 대화 (Gemini 연동, 일부 Mock 응답 포함)
- 통화 이력 저장·조회
- FCM 토큰 등록 및 푸시 알림
- 어르신 목록/검색/건강상태·관심 필요 대상 조회
- WebSocket 기반 실시간 채팅 구조

## 기술 스택

| 구분 | 기술 |
|------|------|
| Mobile | Flutter (Dart), Firebase (Auth/FCM options) |
| Backend | Spring Boot, Spring Web, JPA, WebSocket |
| AI | Google Gemini API |
| DB | PostgreSQL |
| Push | Firebase Cloud Messaging (firebase-admin) |

## 저장소 구조

```
elder-care-app/
├── flutter_app/   # Flutter 모바일 앱
├── backend/       # Spring Boot API 서버
├── mobile/        # (레거시/보조) Cordova 등 산출물
└── docs/          # 기획·설계 문서
```

## 빠른 실행 (요약)

### Backend
```bash
cd backend
./gradlew bootRun
```

### Flutter
```bash
cd flutter_app
flutter pub get
flutter run
```

상세 절차는 [docs/SETUP.md](docs/SETUP.md)를 참고한다.

## 문서

- [기획서 및 요구사항 정의서](docs/PLANNING.md)
- [WBS 및 일정](docs/WBS.md)
- [아키텍처 설계 문서](docs/ARCHITECTURE.md)
- [ADR (아키텍처 의사결정 기록)](docs/ADR.md)
- [Setup / Deploy / Testing 가이드](docs/SETUP.md)

## 역할 (본인)

팀 프로젝트에서 **프론트엔드(Flutter UI/화면 흐름)** 중심으로 참여.
(정확한 분담이 다르면 README의 역할 문구만 수정하면 된다.)

## 라이선스

본 프로젝트는 학습·팀 프로젝트 목적으로 제작되었습니다.
