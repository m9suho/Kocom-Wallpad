# 릴리즈 v2.0.9 - 일괄소등 프로토콜 수정

## 🐛 버그 수정

### 일괄소등 명령 프로토콜 오류 수정

**문제점:**
- v2.0.8에서 일괄소등 버튼을 추가했지만 잘못된 프로토콜 사용
- command를 `0x00`으로 보내고 있었음 (실제는 `0x65`/`0x66` 필요)
- data 포맷이 잘못됨

**실제 프로토콜 분석:**

실제 KOCOM 일괄소등 패킷:
```
켜기: command 0x65, data all 0x00
끄기: command 0x66, data all 0xFF
```

**수정 내용:**

1. **켜기 명령**
   - command: `0x65`
   - data: 모든 8바이트를 `0x00`으로 설정

2. **끄기 명령**
   - command: `0x66`
   - data: 모든 8바이트를 `0xFF`로 설정

3. **공통**
   - dest_room: `0xFF` (일괄소등 전용)

**코드 변경:**
```python
# Before (v2.0.8)
command = bytes([0x00])  # 잘못됨
data[0] = 0xFF if action == "turn_on" else 0x00

# After (v2.0.9)
if action == "turn_on":
    command = bytes([0x65])
    data = bytearray([0x00] * 8)
else:
    command = bytes([0x66])
    data = bytearray([0xFF] * 8)
```

**효과:**
- ✅ 일괄소등 버튼이 실제로 동작합니다
- ✅ 현장에서 검증된 프로토콜과 일치
- ✅ 켜기/끄기 모두 정상 작동

## 📝 변경된 파일
- `custom_components/kocom_wallpad/controller.py`
- `custom_components/kocom_wallpad/manifest.json`

## 🔄 업그레이드 안내

v2.0.8에서 일괄소등이 작동하지 않았던 사용자는 **반드시 업그레이드**해야 합니다.

### 업그레이드 방법
1. 새 버전으로 업데이트
2. Home Assistant 재시작
3. 일괄소등 버튼 테스트

### 호환성
- v2.0.8과 완전히 호환
- 설정 변경 불필요
- 일괄소등 외 모든 기능 정상 작동

## 📊 통계
- **1개 치명적 버그 수정**
- **2개 파일 변경**
- **8개 추가, 3개 삭제**

## 🔗 링크
- **이전 버전**: v2.0.8 (일괄소등 버튼 추가)
- **전체 변경사항**: v2.0.8...v2.0.9

---

**중요**: 실제 현장 패킷 분석을 통해 올바른 프로토콜로 수정되었습니다.
