# 릴리즈 v2.0.10 - Room 0 조명 제어 수정

## 🐛 치명적 버그 수정

### Room 0 조명이 일괄소등으로 잘못 인식되는 문제 해결

**문제점:**
- v2.0.8 이후 room 0의 일반 조명들(light_0_0, light_0_2 등)이 일괄소등 스위치로 잘못 처리됨
- room 0의 모든 조명 제어가 작동하지 않음

**원인:**
- `generate_command`에서 `room_index == 0`만 확인하여 일괄소등 감지
- 하지만 일반 조명도 room 0에 존재할 수 있음
- room 0의 모든 조명이 일괄소등 명령(0x65/0x66)으로 잘못 전송됨

**해결 방법:**

기존에 정의되어 있던 `DeviceType.LIGHTCUTOFF` (값 2)를 활용:

1. **수신 처리 개선**
   ```python
   # _handle_cutoff_switch에서
   device_type=DeviceType.LIGHTCUTOFF  # LIGHT 대신 LIGHTCUTOFF 사용
   ```

2. **송신 명령 개선**
   ```python
   # generate_command에서
   if device_type == DeviceType.LIGHTCUTOFF:  # room_index == 0 대신
       # 일괄소등 명령 생성
   ```

3. **명확한 구분**
   - 일반 조명: `DeviceType.LIGHT` + `room_index 0~N`
   - 일괄소등: `DeviceType.LIGHTCUTOFF` + `room_index 0`

**수정된 동작:**
- ✅ Room 0의 일반 조명 (`light_0_0`, `light_0_2` 등) 정상 작동
- ✅ 일괄소등 버튼은 `LIGHTCUTOFF` 타입으로 구분
- ✅ 일반 조명과 일괄소등 간 혼동 없음

## 📝 변경된 파일
- `custom_components/kocom_wallpad/controller.py`
- `custom_components/kocom_wallpad/manifest.json`

## 🔄 업그레이드 안내

**v2.0.8 또는 v2.0.9 사용 중이며 room 0 조명이 있는 경우 필수 업그레이드입니다.**

### 증상 확인
다음 증상이 있다면 이 버그에 영향을 받은 것입니다:
- `light.kocom_light_light_0_0` 같은 엔티티가 켜지지 않음
- room 0의 모든 조명이 응답하지 않음
- 로그에 command 0x65/0x66 관련 오류

### 업그레이드 방법
1. v2.0.10으로 업데이트
2. Home Assistant 재시작
3. room 0 조명 정상 작동 확인

### 호환성
- 모든 이전 버전과 호환
- room 0 조명이 없는 경우에도 안전하게 업그레이드 가능
- 모든 기존 기능 정상 작동

## 📊 통계
- **1개 치명적 버그 수정**
- **2개 파일 변경**
- **14개 추가, 14개 삭제**

## 🔗 링크
- **이전 버전**: v2.0.9 (일괄소등 프로토콜 수정)
- **전체 변경사항**: v2.0.9...v2.0.10

---

**중요**: v2.0.8에서 발생한 회귀(regression) 버그가 완전히 수정되었습니다.
