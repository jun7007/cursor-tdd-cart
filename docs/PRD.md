# PRD — 장바구니 할인 계산기 (cursor-tdd-cart)

| 항목 | 내용 |
|------|------|
| **문서 버전** | 0.1 (Discovery 단계) |
| **작성일** | 2026-06-24 |
| **상태** | 계약 미확정 — MomTest Discovery 진행 중 |
| **근거 문서** | [Report/01.REPORT.md](../Report/01.REPORT.md), [Report/02.REPORT.md](../Report/02.REPORT.md), [Prompting/01.Export-Transcript.md](../Prompting/01.Export-Transcript.md), [Prompting/02.Export-Transcript.md](../Prompting/02.Export-Transcript.md) |

---

## 1. 제품 개요

**cursor-tdd-cart**는 장바구니 품목과 할인 규칙을 입력받아 **결제 금액을 계산**하는 시스템이다.

- **Entity**: `src/cart.py` — 순수 도메인 로직·불변식 (`INV-*`)
- **Boundary**: `src/app.py` — Flask 주문 폼·입력/UI 계약 (`E-*`, `UC-*`)
- **검증**: pytest 기반 Dual-Track TDD, 계약 ID로 테스트와 구현을 추적

현재(세션 01~02 기준) **구현·테스트는 시작 전**이다. `src/cart.py`는 비어 있고 `tests/` 디렉터리는 없다.

---

## 2. 문제 정의

장바구니 할인 계산에서 다음 유형의 오류가 비즈니스 손실·고객 클레임으로 이어질 수 있다.

- 소계·할인 적용 기준 금액 불일치
- 경계값(임계 금액, 0원, 반올림) 처리 오류
- 잘못된 입력(음수 수량, 빈 장바구니)의 무방비 통과
- 복수 할인 규칙의 적용 순서 혼선

**아직 구체적 사례·수치 근거는 수집되지 않았다.** 본 PRD는 확정 요구사항이 아니라 Discovery 산출물과 개발 원칙을 정리한다.

---

## 3. 목표

| ID | 목표 | 근거 |
|----|------|------|
| G-01 | 테스트 가능한 계약(`INV-*`, `E-*`, `AC-*`)을 MomTest로 발견·확정한다 | [Report/02](../Report/02.REPORT.md), [Prompting/02 Turn 1~2](../Prompting/02.Export-Transcript.md) |
| G-02 | 확정된 계약만 RED → GREEN → REFACTOR 사이클로 구현한다 | [Report/01](../Report/01.REPORT.md), `AGENTS.md` |
| G-03 | Entity 불변식을 Boundary(UI)보다 먼저 검증한다 | [Report/01 §3](../Report/01.REPORT.md), [Report/02 §3](../Report/02.REPORT.md) |

---

## 4. 비목표 (Out of Scope)

근거 없이 구현하지 않는다. [Prompting/02 Turn 2](../Prompting/02.Export-Transcript.md)에서 정의된 OOS 항목:

| OOS ID | 만들지 않을 동작 | 제외 이유 |
|--------|------------------|-----------|
| OOS-01 | 쿠폰·프로모 코드 | 인터뷰·사례 근거 없음 |
| OOS-02 | 세금·부가세 | 근거 없음 |
| OOS-03 | 배송비 | 근거 없음 |
| OOS-04 | 포인트·마일리지 | 근거 없음 |
| OOS-05 | 회원 등급·VIP 할인 | 근거 없음 |
| OOS-06 | 복수 할인 스택·적용 순서 | 실제 사례 없음 |
| OOS-07 | 통화·환율 | 근거 없음 |
| OOS-08 | 재고·품절 검증 | 할인 계산 범위 근거 없음 |
| OOS-09 | 문서 예시 할인(5만 원·10% 등) | `dual-track-tdd.mdc` 예시일 뿐, 도메인 미확정 |
| OOS-10 | Flask UI·라우트 세부 | 폼·에러 표시 실패 사례 없음 |

**원칙:** 계약 ID에 없는 동작은 구현하지 않는다.

---

## 5. 확정 계약 (현재: 0건)

MomTest 분석 시 분석 대상이 플레이스홀더뿐이어서 **확정된 `INV-*` / `E-*` / `AC-*`는 없다.**

| ID | 계약 | 근거 레벨 | 계층 | 상태 |
|----|------|-----------|------|------|
| — | *(없음)* | — | — | Discovery 대기 |

인터뷰·버그 사례·요구사항이 들어오면 아래 형식으로 본 표를 갱신한다.

**좋은 계약 예시 (형식 참고용, 미확정):**

- `subtotal == 50000`이면 `apply_discount` 반환값이 `45000`이다.
- `price` 또는 `qty`가 음수이면 인덱스를 포함한 `ValueError`를 발생시킨다.

**나쁜 계약 예시:**

- "할인이 잘 적용되어야 한다."

---

## 6. MomTest Discovery — 미답변 질문

[Report/02](../Report/02.REPORT.md) 세션에서 생성된 질문이다. 유도·예/아니오가 아닌 **실제 사건** 답변을 수집할 때까지 계약 확정을 보류한다.

### 6.1 최근 실제 사례

1. 가장 최근에 금액이 틀렸던 주문은 언제였고, 고객·운영·정산이 각각 어떤 숫자를 기대했으며 실제로는 무엇이 나왔는가?
2. 직접 엑셀이나 계산기로 다시 계산해 본 적이 있다면, 어떤 품목·수량·할인 조합이었고 처음 결과와 어디가 달랐는가?
3. 환불·부분 취소·수량 변경 때문에 금액을 다시 맞춘 사례가 있다면, 그때 어떤 규칙을 기준으로 맞췄는가?

### 6.2 경계값·헷갈림

4. 정확히 기준 금액(예: 5만 원)인 주문에서 할인 적용 여부를 두고 다툰 적이 있는가? 각자 어떤 숫자를 근거로 말했는가?
5. 0원, 1원, 최대 금액 같은 극단값에서 시스템·수기 계산이 어긋난 사례가 있는가?
6. 소수·반올림(예: 10% 할인 후 1원 단위) 때문에 고객 문의나 정산 차이가 난 적이 있는가? 구체 금액은?

### 6.3 잘못된 입력

7. 수량 0, 음수, 빈 칸, 문자열이 실제로 들어온 적이 있는가? 그때 화면·영수증·DB에 무엇이 기록됐고 이후 어떤 손해가 있었는가?
8. 가격이 없는 품목·중복 SKU·품목 목록이 비어 있는 상태로 결제가 진행된 사례가 있는가?

### 6.4 규칙 조합·순서

9. 여러 할인이 동시에 걸린 주문에서, 한쪽만 적용되거나 순서가 바뀌면 금액이 달라진 실제 주문·금액이 있는가?
10. 할인 적용 전 총액 vs 할인 후 총액 중 어느 쪽을 고객·회계가 "맞다"고 한 사례와 틀렸다고 한 사례를 각각 들 수 있는가?

### 6.5 손실·절대 불가 결과

11. 할인 규칙이 깨졌을 때 회사·고객에게 실제로 생긴 손실(과다 할인, 미적용, 클레임)은 무엇이었는가?
12. 절대 나오면 안 된다고 말한 결과(예: 음수 결제액, 할인 후 원가보다 비싼 금액)가 있는가? 그게 나왔던 적이 있는가?
13. 고객이 받아들일 수 없다고 한 화면·영수증 표기는 무엇이었는가?

### 6.6 Boundary (UI·입력 경로)

14. 웹 폼에서 제출한 값과 서버/계산 로직이 받은 값이 달라서 문제가 된 적이 있는가? 어떤 필드였는가?
15. 입력 경로가 다른 채널(모바일·키오스크 등)에서 같은 규칙으로 계산했을 때 결과가 달랐던 사례가 있는가?

### 6.7 근거 레벨 (답변 수집 후 분류)

| 레벨 | 설명 | 현재 |
|------|------|------|
| L0 | 타입·누락·음수·빈 장바구니 등 기본 경계 | 근거 없음 — §6.3 답변 필요 |
| L1 | 단일 비즈니스 규칙(임계값, 비율, 반올림) | 근거 없음 — §6.2 답변 필요 |
| L2 | 복수 규칙·적용 순서 | 근거 없음 — §6.4 답변 필요 |
| L3 | 총액 ≥ 0 등 안전 불변식 | 근거 없음 — §6.5 답변 필요 |

---

## 7. 기술·아키텍처 요구사항

[Report/01](../Report/01.REPORT.md) 및 `AGENTS.md`에서 확정된 구조:

| 계층 | 경로 | 책임 |
|------|------|------|
| Entity | `src/cart.py` | 순수 로직·불변식. Flask 등 Boundary import 금지 |
| Boundary | `src/app.py` | Flask 주문 폼, Entity 재사용 |
| Entity 테스트 | `tests/entity/` | `INV-*` 검증 (`pytest tests/entity -q`) |
| Boundary 테스트 | `tests/boundary/` | `E-*`, `UC-*` 검증 (`pytest tests/boundary -q`) |

**스택:** Python 3.12, pytest, Flask

**계약 ID 규칙:**

| 유형 | ID 패턴 | 설명 |
|------|---------|------|
| Invariant | `INV-n` | 어떤 입력에서도 깨지면 안 되는 규칙 |
| Error Contract | `E-n` | 잘못된 입력에 대한 관측 가능한 동작 |
| Acceptance Criteria | `AC-n` | 사용자가 수용하는 기능 조건 |
| Out of Scope | `OOS-n` | 구현 제외 |

---

## 8. 개발 워크플로

Dual-Track TDD (ARRR):

1. **RED** — `tests/`만 수정, 실패 테스트 추가
2. **GREEN** — `src/` 최소 구현, 구현 줄에 계약 ID 주석
3. **REFACTOR** — 전부 통과 후 구조 정리, `pytest -q`로 동작 불변 확인

커밋 분리: `test`(RED) / `feat`(GREEN) / `refactor`(구조). 구조 변경과 동작 변경을 한 커밋에 섞지 않는다.

---

## 9. 마일스톤

| 단계 | 내용 | 상태 |
|------|------|------|
| M0 | 프로젝트 스캐폴딩·규칙 정의 | 완료 |
| M1 | MomTest Discovery 질문·OOS 정리 | 완료 ([Report/02](../Report/02.REPORT.md)) |
| M2 | 인터뷰·사례 수집 → 계약표 확정 | **대기** |
| M3 | RED: `tests/entity/` 실패 테스트 | 대기 |
| M4 | GREEN: `src/cart.py` 최소 구현 | 대기 |
| M5 | Boundary 계약·`src/app.py` | 대기 |

---

## 10. 다음 액션

[Report/02 §3](../Report/02.REPORT.md) 기준:

1. §6 MomTest 질문에 대한 **사건 중심 답변** 수집 (주문 번호, 입력값, 기대값, 실제값, 손실)
2. 답변 기반 **테스트 가능한 계약표** 작성 및 PRD §5 갱신
3. 확정 계약부터 `tests/entity/` RED → `src/cart.py` GREEN
4. `pytest tests/entity -q` 통과 후 `tests/boundary/` 확장

**답변 입력 형식 예시:**

```text
- 지난주 주문 #1234: 소계 49,999원인데 10% 할인이 적용됐다. 기대는 미적용.
- 수량에 -1 넣으면 500 에러 없이 0원으로 결제됐다.
- 할인은 소계 기준이고, 5만 원 이상만 10%, 1원 단위 반올림은 없음(정수 원).
```

---

## 11. 참고 문서

| 문서 | 설명 |
|------|------|
| [AGENTS.md](../AGENTS.md) | ECB 구조·TDD 워크플로·금지 사항 |
| [.cursor/rules/dual-track-tdd.mdc](../.cursor/rules/dual-track-tdd.mdc) | RED/GREEN/REFACTOR 규칙 |
| [Report/01.REPORT.md](../Report/01.REPORT.md) | 초기 Export·프로젝트 컨텍스트 |
| [Report/02.REPORT.md](../Report/02.REPORT.md) | MomTest Discovery 세션 요약 |
| [Prompting/02.Export-Transcript.md](../Prompting/02.Export-Transcript.md) | Discovery 대화 전문·OOS 원본 |

---

*본 문서는 docs/PRD.md — 장바구니 할인 계산기 Product Requirements Document (Discovery v0.1)입니다.*
