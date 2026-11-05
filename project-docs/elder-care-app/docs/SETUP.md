# 늘봄(Elder Care) — Setup / Deploy / Testing 가이드

## 1. 사전 요구사항

- JDK 21
- Flutter SDK (stable)
- Android Studio / Xcode (대상 플랫폼에 따라)
- PostgreSQL
- (선택) Firebase 프로젝트, Gemini API 키

## 2. Backend 설정

```bash
cd backend
```

`src/main/resources/application.yaml`에 DB·Gemini 설정을 맞춘다.

예시 항목:
- spring datasource (PostgreSQL URL/username/password)
- `gemini.api-key`, `gemini.api-url`
- Firebase Admin 인증 정보(서비스 계정)

실행:

```bash
./gradlew bootRun
```

기본 API 포트는 설정에 따르며, 앱의 `ApiService.baseUrl`과 맞춰야 한다.
(에뮬레이터에서 PC 서버 접속 시 `10.0.2.2` 사용)

## 3. Flutter 앱 설정

```bash
cd flutter_app
flutter pub get
flutter run
```

확인 사항:
- `firebase_options.dart` / Firebase 초기화
- `lib/services/api_service.dart`의 `baseUrl`
- FCM 권한 및 토큰 등록 동작

## 4. 로컬 연동 체크리스트

1. PostgreSQL 기동 및 스키마 자동생성/마이그레이션 확인
2. 어르신 건강상태(`health-status`) API 응답 확인
3. Flutter에서 로그인 → 홈 진입
4. AI 채팅 메시지 송수신
5. (선택) FCM 테스트 발송

## 5. 테스트

- Backend: `./gradlew test`
- Flutter: `flutter test` (위젯 테스트 기본 포함)

현재는 핵심 시나리오 중심의 수동 통합 테스트(시연 스크립트)를
우선하고, 자동화 테스트는 점진 확장한다.

## 6. 배포 시 주의

- Gemini/Firebase 키를 저장소에 커밋하지 말 것
- 프로덕션 DB 자격증명 분리
- HTTPS 및 인증 토큰 도입 권장
- 어르신 개인정보 최소 수집·보관 기간 정책 수립
