# Release v2.0.10

## 버그 수정

### 🔧 Room 0 조명 제어 오류 수정
- **문제**: light_0_0, light_0_1 등 0번 방 조명 엔티티가 제어되지 않던 문제
- **원인**: `generate_command` 함수에서 LIGHTCUTOFF 타입 처리 시 `REV_DT_MAP`에 없는 키를 참조하여 KeyError 발생
- **해결**:
  - `dest_dev`와 `dest_room` 초기화를 제거하고 각 device type 조건문 안에서 설정
  - LIGHTCUTOFF 타입은 `REV_DT_MAP`을 참조하지 않고 직접 값 설정 (0x0E, 0xFF)
  - 일반 조명(LIGHT)과 일괄소등(LIGHTCUTOFF)을 명확히 구분하여 처리

### 📦 영향받는 컴포넌트
- `controller.py`: `generate_command` 메서드 리팩토링
  - LIGHTCUTOFF: dest_dev=0x0E, dest_room=0xFF 직접 설정
  - LIGHT/OUTLET/THERMOSTAT/AIRCONDITIONER/VENTILATION/GASVALVE: REV_DT_MAP 사용
  - ELEVATOR: 기존 로직 유지

## 테스트

다음 엔티티들이 정상 작동하는지 확인:
- ✅ `light.kocom_light_light_0_0` (0번 방 조명 1)
- ✅ `light.kocom_light_light_0_1` (0번 방 조명 2)
- ✅ `light.kocom_lightcutoff_cutoff_0_0` (일괄소등)
