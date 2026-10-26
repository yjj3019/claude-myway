# 단건 리포트 형식 (동결)

> 동결 상태. 사용자가 "스킬/규칙/포맷을 수정해줘"라고 명시한 경우에만 변경한다. 단순 리포트 요청은 이 규칙을 100% 그대로 적용하는 요청이다. 규칙으로 처리할 수 없는 상황이면 임의로 판단하지 말고 사용자에게 먼저 확인한다.
>
> v2.0.0 변경(2026-09-16, 사용자 명시 결정): 5번 표 7컬럼 단일화, NVR epoch 제거, 출처는 실제 조회 URL, 표 안 서식 기호 금지, 1번 표 기본 행 고정.

파일: `CVE-YYYY-NNNNN_리포트.md` (claude.ai는 `/mnt/user-data/outputs/`, 그 외 현재 작업 디렉터리) → `python3 scripts/check_report.py <파일>` 통과 → claude.ai는 `present_files`, 그 외는 경로 안내.

## 전체 구조

```
# CVE-YYYY-NNNNN 보안 취약점 리포트

## 1. 개요
## 2. 심각도(CVSS) 비교
## 3. 실제 악용 가능성 (EPSS · CISA KEV)
## 4. 완화 방법 (Mitigation)
## 5. 영향받는 제품 및 패치
## 6. 출처
```

H2는 정확히 이 6개, 이 순서, 이 문구. 그 외 H2·H3 추가 금지(1번의 `### 취약점 설명`만 허용).

## 공통 금지

- HTML 태그 금지 (`<div>`, `<p align>`, `<br>` 등)
- 표 정렬 지정 금지 (`|:---|`, `|---:|`, `|:---:|`). 구분선은 `|---|`만
- "권장 조치 순서" 등 임의 섹션 추가 금지
- 5번 표 아래에 날짜·생성일·타임스탬프 등 메타정보 금지
- 표 안에 굵게(`**`), 이모지, 백틱 금지
- 문체: 한국어 존댓말 평서형 설명체. 기술 용어는 괄호로 영어 병기 가능

## 1. 개요

표 컬럼 `항목 | 내용`, 행은 아래 순서 고정. 값이 없으면 "정보 없음".

| 항목 | 값 출처 |
|---|---|
| CVE ID | 입력 |
| 컴포넌트 | Hydra package_state/affected_release의 소스 패키지명. 제품별로 다르면 "nmap (OpenShift Container Platform 4는 rhcos)"처럼 병기 |
| 요약 | 취약점 유형과 영향을 한 줄로 |
| Red Hat 심각도 | threat_severity를 "Moderate (보통)"처럼. 매핑: Critical (긴급) / Important (높음) / Moderate (보통) / Low (낮음) |
| 공개일 | Red Hat public_date (YYYY-MM-DD) |
| 최종 갱신일 | CSAF `document.tracking.current_release_date` → 없으면 Bugzilla Modified. 둘 다 없으면 "정보 없음" |
| CWE 분류 | Red Hat CWE → "CWE-125 (경계 밖 읽기)" 형식. CNA CWE가 다르면 병기 |

그 아래 `### 취약점 설명` (문구 고정) + 서술 문단 2~3개.
- 무엇이, 어떤 조건에서, 어떤 결과로 이어지는지. Description 한정어를 빠뜨리지 않는다.
- 공격 성립 조건(로컬/원격, 권한, 사용자 동작)을 한 문단으로 정리한다.
- 원문에 없는 영향(예: 코드 실행)을 과장하지 않는다.

## 2. 심각도(CVSS) 비교

표 컬럼 정확히 `평가 기관 | 버전 | 점수 | 벡터 | 등급`.
- 행 순서: Red Hat → NVD → cve.org. 기관 행은 3개 모두 유지하고, 한 기관이 여러 버전(v3.1, v4.0)을 제공하면 버전별로 행을 추가한다.
- 버전 표기 `CVSS v3.1`, 벡터는 `CVSS:3.1/...` 전체 문자열.
- NVD가 채점하지 않았으면 해당 행의 버전·점수·벡터·등급 모두 "정보 없음".
- cve.org 행의 평가 기관은 "cve.org (CNA명)" 형식.

표 아래 `>` 인용구 1줄: 기관 간 점수·벡터 차이의 이유를 단정형으로. 차이가 없으면 "기관별 평가가 일치합니다." 식으로 짧게.

## 3. 실제 악용 가능성 (EPSS · CISA KEV)

표 컬럼 정확히 `지표 | 값 | 조회 기준일`, 행은 정확히 3개, 이 순서:

| 지표 | 값 형식 | 조회 기준일 |
|---|---|---|
| EPSS 점수 | `1.367%` (원자료 정밀도 유지, 소수점 이하 최대 셋째 자리) 또는 "정보 없음" | EPSS 응답 date 또는 미러 score_date |
| EPSS 백분위 | `70.356%` 또는 "정보 없음" | 위와 동일 |
| CISA KEV 등재 여부 | "미등재" 또는 "등재됨 (등재일 YYYY-MM-DD, 조치 기한 YYYY-MM-DD)" | 조회일 (카탈로그 배포일 YYYY-MM-DD) |

표 아래 `**해석**` 한 줄, 그 아래 불릿 정확히 3개:
1. EPSS 수치의 의미(확률과 백분위 위치)
2. KEV 등재 여부와 PoC·실제 악용 보고 여부
3. 공격 성립 조건을 반영한 실질 위험도 종합

## 4. 완화 방법 (Mitigation)

- Red Hat Mitigation에 구체 조치가 있으면: 한국어로 의역해 서술하고, 명령·설정은 코드 블록으로 제시한다.
- 보일러플레이트("not available … do not meet the Red Hat Product Security criteria")이거나 없으면: 첫 문단에 "공식 완화 조치는 제공되지 않으며 패치가 유일한 근본 해결책입니다."를 쓰고, CVE 성격에 맞는 노출 최소화 조치 3~4개를 불릿으로 쓴다.
  - 서버 데몬: 방화벽으로 신뢰할 수 없는 접속 차단, 불필요 서비스 비활성화
  - 클라이언트(브라우저·메일): 출처 불명 콘텐츠 자제, 원격 콘텐츠 자동 로딩 차단
  - 커널·로컬 권한상승: 모듈 블랙리스트(가능 시), 로컬 계정·컨테이너 권한 최소화
  - 도구류: 패키지 설치 여부 확인(`rpm -q`), 미사용 시 제거
- RHSB에 완화 절차가 있으면 그 절차를 우선한다.

## 5. 영향받는 제품 및 패치

표 컬럼 정확히 `제품 | 컴포넌트 | 상태 | 근거 | RHSA | 수정 버전(x86_64) | 발행일`.

포함 범위: Hydra `affected_release`와 `package_state`의 모든 항목. 패치가 나온 제품만 넣지 않는다.

행 작성:
- 제품: product_name 원문 (예: `Red Hat Enterprise Linux 9`, `Red Hat Enterprise Linux 9.4 Extended Update Support`)
- 컴포넌트: 소스 패키지명 (epoch·버전 없이)
- 상태: judgment-rules.md 3절 표기 (예: `수정됨(Fixed)`, `패치 보류(Fix deferred)`)
- 근거: CSAF justification 번역, CONFLICT 내역, ELS 안내 등. 없으면 `-`
- RHSA: 수정됨 행은 RHSA ID(링크 없이). 그 외 `-`
- 수정 버전(x86_64): epoch 제거 NVR. 수정됨이 아니면 `-`. 수정됨인데 NVR 미확보면 "정보 없음"
- 발행일: 수정됨 행은 YYYY-MM-DD. 그 외 `-`

정렬: RHEL 메이저 버전 내림차순(10 → 6) → 같은 메이저 안에서 메인 → EUS/E4S/AUS → ELS → 그 외 Red Hat 제품(가나다·알파벳순).

표 아래 `>` 인용구는 다음 고정 문구 하나만. 요약·해설·정정 문구를 덧붙이지 않는다.

> 이 목록에서 명시적으로 "영향 없음(not affected)"으로 표기되지 않은 이상, 목록에 포함된 제품의 모든 마이너 업데이트 스트림에 포함된 기존 패키지 버전은 전체 분석이 수행되지 않았더라도 취약한 것으로 간주해야 합니다.

## 6. 출처

번호 목록, 아래 순서, 해당 사항 있는 것만. URL은 실제로 조회에 성공한 것만 적는다(생명주기 정책은 고정 참조 문서라 예외). 검색 결과에만 보이고 열어보지 않은 URL은 적지 않는다. 아래 1~6은 카테고리 순서이며, 실제 번호는 포함한 항목 기준으로 1부터 다시 매긴다.

1. Red Hat CVE 페이지 — `https://access.redhat.com/security/cve/CVE-YYYY-NNNNN`
   - 하위 항목(실제 조회한 것만): Hydra JSON/XML, CSAF/VEX, RHSB, errata(RHSA별), 대체 소스 `(대체 소스, 수집 시점 YYYY-MM-DD)`
2. Red Hat Bugzilla — `https://bugzilla.redhat.com/show_bug.cgi?id=NNNNNNN`
3. 업스트림 보안 권고 — Mozilla mfsa, 업스트림 수정 커밋, CNA 권고 등
4. Red Hat 생명주기 정책 — `https://access.redhat.com/support/policy/updates/errata`
5. EPSS — 실제 사용한 URL (api.first.org 또는 GitHub 미러)
6. CISA KEV — 실제 사용한 URL

## 제출 전 체크리스트 (check_report.py가 1~9 자동 검사)

1. 제목과 H2 6개의 문구·순서 일치
2. `### 취약점 설명` 존재, 그 외 H3 없음
3. 2번 표 컬럼 일치
4. 3번 표 컬럼 일치, 행 3개 고정
5. `**해석**` 뒤 불릿 3개
6. 5번 표 컬럼 일치, 고정 인용구 1개만, 인용구 뒤 추가 텍스트 없음
7. HTML 태그·표 정렬 지정·표 안 서식 기호 없음
8. NVR epoch 없음
9. 6번 출처 번호 순서
10. (수동) 5번 표에 원자료에 없는 제품·NVR·RHSA가 없는가
11. (수동) 소스 접근 실패·대체 소스·CONFLICT·커버리지 축소를 대화 응답에 밝혔는가
