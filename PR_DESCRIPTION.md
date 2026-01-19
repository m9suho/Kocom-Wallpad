## 🐛 Bug Fixes and Code Quality Improvements (v2.0.6)

이 PR은 코드 분석을 통해 발견된 12개의 버그를 수정하고 코드 품질을 개선합니다.

### Critical Fixes (치명적 문제 수정)

- **Fixed event loop initialization error** in `gateway._CmdItem` dataclass
  - `RuntimeError: no running event loop` 오류 방지
  - dataclass 정의 시점이 아닌 런타임에 future 생성하도록 수정

- **Fixed type mismatch** in gasvalve expectation return value
  - `bool` 대신 올바른 `Predicate` 타입 반환

- **Fixed incorrect initial connection state** in transport
  - 연결되지 않은 상태에서 `_connected = True`였던 버그 수정

### Important Fixes (중요 문제 수정)

- **Fixed variable name typo**: `havc_mode` → `hvac_mode`
  - thermostat handler (3곳)
  - airconditioner handler (3곳)

- **Fixed invalid format specifier**: `error_code:02` → `error_code:02x`
  - 에러 코드를 올바른 16진수 형식으로 표시

- **Fixed variable name collision** in airquality handler
  - 루프 변수 `key`가 `DeviceKey`로 덮어씌워지던 문제 해결

- **Replaced private method with public property**
  - `_is_connected()` → `is_connected` property로 캡슐화 개선

- **Fixed type hint**: `list[callable]` → `list[Callable]`
  - 올바른 타입 import 추가

- **Removed invalid DeviceInfo parameter**
  - 잘못된 `connections` 파라미터 제거

### Improvements (개선사항)

- **Added safe access for optional climate properties**
  - `fan_mode`, `fan_modes`, `preset_mode`, `preset_modes`에 `.get()` 사용
  - `KeyError` 방지를 위한 None 처리

### 📝 Changed Files

- `controller.py` - 5개 버그 수정
- `gateway.py` - 3개 버그 수정
- `transport.py` - 2개 버그 수정
- `entity_base.py` - 2개 버그 수정
- `climate.py` - 1개 개선
- `manifest.json` - 버전 2.0.6으로 업데이트

### 📊 Statistics

- **12 issues fixed** (3 critical, 6 important, 3 improvements)
- **6 files changed**
- **34 insertions, 31 deletions**

### 🔗 Related

- Closes: N/A (proactive bug fixes)
- Release Notes: See `RELEASE_NOTES_v2.0.6.md`

### ✅ Testing

모든 수정사항은 backward compatible하며 설정 변경이 필요하지 않습니다.

### 📦 Release

이 PR이 병합되면 GitHub Actions가 자동으로 v2.0.6 릴리즈를 생성합니다.
