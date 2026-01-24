# Release v2.0.10-beta.2

⚠️ **베타 버전**: 이 버전은 테스트 중이며 프로덕션 환경에서 사용 시 주의가 필요합니다.

## 버그 수정

### 🔧 Room 0 조명 제어 오류 수정
- **문제**: light_0_0, light_0_1 등 0번 방 조명 엔티티가 제어되지 않던 문제
- **원인**: `generate_command` 함수에서 LIGHTCUTOFF 타입 처리 시 `REV_DT_MAP`에 없는 키를 참조하여 KeyError 발생
- **해결**:
  - `dest_dev`와 `dest_room` 초기화를 제거하고 각 device type 조건문 안에서 설정
  - LIGHTCUTOFF 타입은 `REV_DT_MAP`을 참조하지 않고 직접 값 설정 (0x0E, 0xFF)
  - 일반 조명(LIGHT)과 일괄소등(LIGHTCUTOFF)을 명확히 구분하여 처리

### 🔧 일괄소등 엔티티 생성 오류 수정
- **문제**: 일괄소등 버튼을 눌러도 `light.kocom_lightcutoff_cutoff_0_0` 엔티티가 생성되지 않음
- **원인**: `gateway.py`의 `on_device_state`에서 LIGHTCUTOFF 타입이 `allow_insert` 체크에 포함되지 않음
- **해결**:
  - `DeviceType.LIGHTCUTOFF`를 `allow_insert` 조건에 추가
  - LIGHTCUTOFF는 항상 `allow_insert=True`로 강제하여 엔티티 등록 보장

### 🔧 강제 재등록 문제 수정 (beta.2)
- **문제**: beta.1에서 매 패킷마다 LIGHTCUTOFF 엔티티를 registry에서 삭제하고 재등록하는 버그
- **원인**: 일괄소등 엔티티가 생성되지 않는 문제 해결 과정에서 과도한 수정 적용
- **해결**:
  - 강제 재등록 코드 제거
  - LIGHTCUTOFF는 최초 1회만 등록되고 이후에는 정상적으로 상태 업데이트만 수행
  - 불필요한 오버헤드 제거 및 안정성 향상

## 개선 사항

### 🐛 디버그 로깅 강화 (beta.2)
- 조명 패킷 수신 시 상세 로그 출력 (room, command, payload)
- 일괄소등 감지 시 로그 출력
- **일괄소등 명령 생성 디버깅 로그 추가**:
  - action (turn_on/turn_off)
  - command byte (0x65/0x66)
  - data payload
  - 최종 생성된 패킷 hex dump
- Registry upsert 결과 로그 추가 (is_new, changed 상태 추적)

### 📦 영향받는 컴포넌트
- `controller.py`: `generate_command` 메서드 리팩토링 및 디버그 로그 추가
  - LIGHTCUTOFF: dest_dev=0x0E, dest_room=0xFF 직접 설정
  - LIGHTCUTOFF 명령 생성 시 상세 디버그 로그 출력
  - LIGHT/OUTLET/THERMOSTAT/AIRCONDITIONER/VENTILATION/GASVALVE: REV_DT_MAP 사용
  - ELEVATOR: 기존 로직 유지
- `gateway.py`: LIGHTCUTOFF 타입 처리 최적화
  - allow_insert 체크에 LIGHTCUTOFF 추가
  - 강제 재등록 코드 제거 (안정성 향상)
  - Registry 상태 추적 로그 추가

## 테스트 필요 항목

다음 엔티티들이 정상 작동하는지 확인:
- ✅ `light.kocom_light_light_0_0` (0번 방 조명 1)
- ✅ `light.kocom_light_light_0_1` (0번 방 조명 2)
- ✅ `light.kocom_lightcutoff_cutoff_0_0` (일괄소등 - 엔티티 생성 및 동작 확인)

**일괄소등 동작 테스트:**
1. 엔티티 생성 확인: 벽패드에서 일괄소등 버튼 1회 누르기
2. 동작 확인: Home Assistant에서 일괄소등 엔티티 켜기/끄기
3. 로그 확인: debug 레벨에서 LIGHTCUTOFF 패킷 생성 로그 확인

## 변경 이력

### beta.2 (현재)
- 강제 재등록 버그 수정
- 일괄소등 명령 생성 디버깅 로그 추가
- Registry 상태 추적 로그 추가

### beta.1
- Room 0 조명 제어 오류 수정
- 일괄소등 엔티티 생성 오류 수정
- 기본 디버그 로깅 추가

## 설치 방법

이 베타 버전을 테스트하려면:
1. HACS에서 "사용자 정의 저장소" 추가
2. 또는 수동으로 `custom_components/kocom_wallpad` 폴더 교체
3. Home Assistant 재시작
4. **로그 레벨을 debug로 설정하여 상세 로그 확인 필수**:
   ```yaml
   logger:
     default: info
     logs:
       custom_components.kocom_wallpad: debug
   ```
