# 늘봄(Elder Care) — ADR (Architecture Decision Record)

본 문서는 팀 프로젝트에서 내린 주요 기술 의사결정을 기록한다.

---

## ADR-1: 모바일 클라이언트로 Flutter 선택

### 상태
승인됨

### 배경 (Context)
어르신/보호자 모두 스마트폰 사용을 전제로 하며,
안드로이드·iOS를 함께 목표로 하면 네이티브 이중 개발 비용이 크다.

### 결정 (Decision)
Flutter(Dart)로 단일 코드베이스 모바일 앱을 개발한다.

### 이유 (Rationale)
- UI를 빠르게 반복 구현 가능
- 어르신용 큰 글씨·커스텀 테마 적용이 용이
- 팀원 학습 곡선과 일정에 적합

### 결과 (Consequences)
- `flutter_app` 중심으로 화면이 구성됨
- 네이티브 특화 기능은 플러그인/플랫폼 채널이 필요할 수 있음

---

## ADR-2: 백엔드로 Spring Boot + JPA + PostgreSQL

### 상태
승인됨

### 배경 (Context)
어르신 정보, 통화 이력, 알림 연동 등 서버 측 데이터/연동이 필요하다.

### 결정 (Decision)
Spring Boot로 REST API를 구성하고, JPA로 PostgreSQL에 저장한다.

### 이유 (Rationale)
- 컨트롤러/서비스/리포지토리 구조로 역할 분담이 명확
- 팀 수업/전공 스택과 친숙
- WebSocket·Validation 등 확장에 유리

### 결과 (Consequences)
- `backend` 모듈이 독립 실행됨
- DB 스키마·로컬 PostgreSQL 환경 설정이 필요

---

## ADR-3: 대화 AI로 Gemini API 사용

### 상태
승인됨

### 배경 (Context)
어르신과 자연스러운 짧은 대화를 생성할 LLM이 필요하다.

### 결정 (Decision)
서버의 `GeminiService`에서 Google Gemini API를 호출한다.
클라이언트에는 Mock 응답도 두어 개발 중 서버 없이도 UI를 검증한다.

### 이유 (Rationale)
- 짧은 문장 생성에 충분
- API 키를 서버에 둘 수 있어 클라이언트 노출을 줄임
- Mock으로 프론트 개발 병목을 줄임

### 결과 (Consequences)
- 네트워크/할당량에 따라 응답 품질·지연이 달라질 수 있음
- 프롬프트(“친절한 AI 친구, 1~2문장”)로 톤을 고정

---

## ADR-4: 푸시 알림으로 FCM 사용

### 상태
승인됨

### 배경 (Context)
보호자에게 이벤트/이상 신호를 전달할 채널이 필요하다.

### 결정 (Decision)
Firebase Cloud Messaging + firebase-admin으로 토큰 등록·발송을 구현한다.

### 이유 (Rationale)
- 모바일 푸시의 사실상 표준 경로
- Flutter/Firebase 생태계와 잘 맞음

### 결과 (Consequences)
- Firebase 프로젝트·서비스 계정 설정이 필요
- 토큰 생명주기(갱신) 관리가 중요
