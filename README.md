# -Week3

## 1. Dart 소개  
- **개발 배경**  
  - 구글이 **자바스크립트 대체**를 목표로 개발  
  - 초기에 외면받았지만, **2017년 플러터(Flutter)** 출시로 전환점  
  - 현재는 **플러터와 함께 급성장**, 구글의 적극 지원  

- **Dart의 특징**  
  - **빠른 성능**: JIT(개발 중) + AOT(배포 시) 컴파일  
  - **Null Safety** 지원 → 런타임 오류 방지  
  - **직관적인 문법** + **강력한 타입 시스템**  
  - **객체지향 언어(OOP)** 기반  
  - **플러터 개발에 필수적인 언어**

---

## 2. 개발 환경  
- **DartPad**  
  - URL: [https://dartpad.dev](https://dartpad.dev)  
  - 브라우저에서 바로 실행 가능  
  - 코드 예시:
    ```dart
    void main() {
      print('Hello, Dart!');
    }
    ```

---

## 3. 변수와 데이터 타입  
- **타입 선언 방식**
  ```dart
  var name = '홍길동';     // 타입 추론
  String job = '개발자';   // 명시적 선언

  ---

## 4. 컬렉션(Collection)  
- **List**
  ```dart
  var list = [1, 2, 3];
  list.add(4);

  ---

## 5. 연산자  
- **산술 연산자**
  ```dart
  print(5 + 3);  // 8
  print(10 - 4); // 6
  print(3 * 4);  // 12
  print(15 / 3); // 5
  print(17 % 5); // 2

  ---

  
  - **비교 연산자**
print(5 > 3);   // true
print(5 <= 3);  // false
print(5 == 5);  // true


