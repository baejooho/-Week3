# 늘봄(Elder Care) — 아키텍처 설계 문서

## 1. 개요

시스템은 **Flutter 클라이언트**와 **Spring Boot 서버**로 구성된다.
클라이언트는 역할별 화면을 제공하고, 서버는 REST API·AI 대화·FCM·
(선택) WebSocket을 담당한다.

## 2. 시스템 구성도

```
[어르신 앱(Flutter)]          [보호자 앱(Flutter)]
        \                          /
         \                        /
          v                      v
           [Spring Boot Backend]
            |- ElderController
            |- CallHistoryController
            |- ConversationController / ChatController
            |- FCMController
            |- GeminiService  ---> [Google Gemini API]
            |- FCMService     ---> [Firebase Cloud Messaging]
            |- JPA Repositories
                    |
                    v
              [PostgreSQL]
```

## 3. 모듈 설명

### 3.1 Flutter (`flutter_app/lib`)
- `main.dart`: Firebase 초기화, FCM 초기화, 로그인 상태에 따른 홈 분기
- `services/`: `api_service`, `auth_service`, `fcm_service`
- `screens/`: 로그인/회원가입, 홈, AI 채팅, 통화, 건강, 보호자 관리 등

### 3.2 Backend (`backend/src/main/java/...`)
- `controller`: REST 엔드포인트
- `service`: 비즈니스 로직 (Elder, CallHistory, Gemini, FCM)
- `entity` / `repository`: JPA 매핑
- `config`: Firebase Admin, WebSocket

### 3.3 외부 연동
- Gemini: 어르신 대화 응답 생성
- FCM: 보호자/디바이스 푸시
- PostgreSQL: 어르신·통화이력 등 영속 데이터

## 4. 주요 API (구현 기준)

- Elder: 목록/상세/등록/검색/건강상태(`health-status`)/attention-needed
- Call History: 최근/전체/오늘/저장
- FCM: 토큰 등록, 테스트 발송
- Conversation/Chat: 대화 처리 및 실시간 메시징 구성

## 5. 데이터 흐름 예시 (AI 대화)

1. 어르신 앱이 메시지 입력
2. Flutter `ApiService.chat` 또는 서버 Conversation API 호출
3. `GeminiService`가 시스템 프롬프트 + 사용자 문장으로 Gemini 호출
4. 응답 텍스트를 앱 화면에 표시
5. (옵션) 대화/통화 이력을 DB에 저장

## 6. 설계상 특징

- **역할 분리 UX**: 어르신/보호자 플로우를 처음부터 분리
- **AI는 서버 중심**: API 키를 앱에 넣지 않고 백엔드에서 호출
- **푸시 연동**: FCM으로 보호자 알림 확장 가능
- **점진적 완성**: AI Mock 응답을 두어 서버 장애 시에도 UI 검증 가능

## 7. 향후 아키텍처 변화

- API Gateway/인증 토큰 표준화 (JWT 등)
- 이벤트 기반 알림(무응답 감지 스케줄러)
- 관측성(로깅, 메트릭) 추가
