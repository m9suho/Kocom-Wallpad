# Release v2.0.10-beta.1

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
  - 이제 일괄소등 스위치가 감지되면 자동으로 엔티티 등록됨

## 개선 사항

### 🐛 디버그 로깅 추가
- 조명 패킷 수신 시 상세 로그 출력 (room, command, payload)
- 일괄소등 감지 시 로그 출력

### 📦 영향받는 컴포넌트
- `controller.py`: `generate_command` 메서드 리팩토링 및 디버그 로그 추가
  - LIGHTCUTOFF: dest_dev=0x0E, dest_room=0xFF 직접 설정
  - LIGHT/OUTLET/THERMOSTAT/AIRCONDITIONER/VENTILATION/GASVALVE: REV_DT_MAP 사용
  - ELEVATOR: 기존 로직 유지
- `gateway.py`: LIGHTCUTOFF 타입을 allow_insert 체크에 추가

## 테스트 필요 항목

다음 엔티티들이 정상 작동하는지 확인:
- ✅ `light.kocom_light_light_0_0` (0번 방 조명 1)
- ✅ `light.kocom_light_light_0_1` (0번 방 조명 2)
- ✅ `light.kocom_lightcutoff_cutoff_0_0` (일괄소등 - 버튼 누르면 엔티티 생성됨)

## 설치 방법

이 베타 버전을 테스트하려면:
1. HACS에서 "사용자 정의 저장소" 추가
2. 또는 수동으로 `custom_components/kocom_wallpad` 폴더 교체
3. Home Assistant 재시작
4. 로그 레벨을 debug로 설정하여 상세 로그 확인 권장
