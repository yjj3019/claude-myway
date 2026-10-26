# 단건 리포트 완성본 예시

- 기준: 가상의 CVE-2099-00001 (실제 데이터가 아닌 형식 예시)
- 용도: 구조·문구·톤 복제용. 데이터는 매번 새로 수집한다. 이 예시의 수치를 재사용하지 않는다.
- 이 파일의 `<!-- REPORT START -->` 아래 내용은 `scripts/check_report.py`를 통과한다.
- 이 예시는 5번 표에 수정됨 행만 있다. 실제 리포트는 Hydra의 모든 항목을 넣는다.

<!-- REPORT START -->
# CVE-2099-00001 보안 취약점 리포트

## 1. 개요

| 항목 | 내용 |
|---|---|
| CVE ID | CVE-2099-00001 |
| 컴포넌트 | examplepkg-a, examplepkg-b |
| 요약 | examplepkg 1.2.3에서 수정된 메모리 안전성(Memory Safety) 결함 |
| Red Hat 심각도 | Important (높음) |
| 공개일 | 2099-06-16 |
| 최종 갱신일 | 2099-07-15 |
| CWE 분류 | 메모리 손상(Memory Corruption) 계열 |

### 취약점 설명

examplepkg가 외부에서 받은 콘텐츠를 처리하는 과정에서 메모리를 잘못 다루는 결함입니다.

공격자가 조작한 콘텐츠를 사용자가 열게 만들면 메모리 손상이 발생합니다. 그 결과 프로그램이 비정상 종료되고, 최악의 경우 임의 코드 실행으로 이어질 수 있습니다.

공격이 성립하려면 사용자가 해당 콘텐츠를 직접 열어야 합니다. 별도의 권한은 필요하지 않습니다.

## 2. 심각도(CVSS) 비교

| 평가 기관 | 버전 | 점수 | 벡터 | 등급 |
|---|---|---|---|---|
| Red Hat | CVSS v3.1 | 7.5 | CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H | High |
| Red Hat | CVSS v2 | 7.6 | AV:N/AC:H/Au:N/C:C/I:C/A:C | High |
| NVD | 정보 없음 | 정보 없음 | 정보 없음 | 정보 없음 |
| cve.org | CVSS v3.1 | 5.3 | CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L | Medium |

> Red Hat은 공격 난이도가 높고 사용자 동작이 필요하다고 보면서도 기밀성·무결성·가용성 영향을 모두 높게 평가해 cve.org보다 점수가 높습니다.

## 3. 실제 악용 가능성 (EPSS · CISA KEV)

| 지표 | 값 | 조회 기준일 |
|---|---|---|
| EPSS 점수 | 0.313% | 2099-08-10 |
| EPSS 백분위 | 23.7% | 2099-08-10 |
| CISA KEV 등재 여부 | 미등재 | 2099-08-11 |

**해석**
- EPSS 0.313%는 향후 30일 내 실제 악용 확률이 매우 낮다는 의미입니다. 백분위 23.7%로 전체 CVE 중 하위권입니다.
- CISA KEV 카탈로그에 포함되어 있지 않아 실제 공격에 쓰였다는 공식 확인은 없습니다.
- CVSS 등급은 High이지만 사용자 동작이 필요하고 악용 지표가 낮아 실질 위험도는 낮은 편입니다.

## 4. 완화 방법 (Mitigation)

공식 완화 조치는 제공되지 않으며 패치가 유일한 근본 해결책입니다. 처리 로직 자체의 결함이라 코드 수정 없이는 근본적으로 막을 수 없습니다. 패치 적용 전까지는 다음 방법으로 노출을 줄일 수 있습니다.

- 출처가 불분명한 콘텐츠를 열지 않습니다.
- 외부 콘텐츠의 자동 처리 옵션이 있으면 비활성화합니다.

## 5. 영향받는 제품 및 패치

| 제품 | 컴포넌트 | 상태 | 근거 | RHSA | 수정 버전(x86_64) | 발행일 |
|---|---|---|---|---|---|---|
| Red Hat Enterprise Linux 10 | examplepkg-a | 수정됨(Fixed) | - | RHSA-2099:27733 | examplepkg-a-1.2.3-1.el10_2 | 2099-06-22 |
| Red Hat Enterprise Linux 10 | examplepkg-b | 수정됨(Fixed) | - | RHSA-2099:30846 | examplepkg-b-1.2.3-1.el10_2 | 2099-06-29 |
| Red Hat Enterprise Linux 10.0 Extended Update Support | examplepkg-a | 수정됨(Fixed) | - | RHSA-2099:36100 | examplepkg-a-1.2.3-1.el10_0 | 2099-07-07 |
| Red Hat Enterprise Linux 10.0 Extended Update Support | examplepkg-b | 수정됨(Fixed) | - | RHSA-2099:38751 | examplepkg-b-1.2.3-1.el10_0 | 2099-07-13 |
| Red Hat Enterprise Linux 9 | examplepkg-a | 수정됨(Fixed) | - | RHSA-2099:27734 | examplepkg-a-1.2.3-1.el9_8 | 2099-06-22 |
| Red Hat Enterprise Linux 9 | examplepkg-b | 수정됨(Fixed) | - | RHSA-2099:29940 | examplepkg-b-1.2.3-1.el9_8 | 2099-06-25 |
| Red Hat Enterprise Linux 8 | examplepkg-a | 수정됨(Fixed) | - | RHSA-2099:27717 | examplepkg-a-1.2.3-1.el8_10 | 2099-06-22 |
| Red Hat Enterprise Linux 8 | examplepkg-b | 수정됨(Fixed) | - | RHSA-2099:33445 | examplepkg-b-1.2.3-1.el8_10 | 2099-06-30 |
| Red Hat Enterprise Linux 8.4 Advanced Mission Critical Update Support | examplepkg-a | 수정됨(Fixed) | - | RHSA-2099:36102 | examplepkg-a-1.2.3-1.el8_4 | 2099-07-07 |
| Red Hat Enterprise Linux 8.4 Advanced Mission Critical Update Support | examplepkg-b | 수정됨(Fixed) | - | RHSA-2099:39428 | examplepkg-b-1.2.3-1.el8_4 | 2099-07-14 |
| Red Hat Enterprise Linux 7 Extended Lifecycle Support | examplepkg-a | 수정됨(Fixed) | - | RHSA-2099:38506 | examplepkg-a-1.2.3-1.el7_9 | 2099-07-13 |

> 이 목록에서 명시적으로 "영향 없음(not affected)"으로 표기되지 않은 이상, 목록에 포함된 제품의 모든 마이너 업데이트 스트림에 포함된 기존 패키지 버전은 전체 분석이 수행되지 않았더라도 취약한 것으로 간주해야 합니다.

## 6. 출처

1. Red Hat CVE 페이지 — https://access.redhat.com/security/cve/CVE-2099-00001
   - CSAF/VEX — https://security.access.redhat.com/data/csaf/v2/vex/2099/cve-2099-00001.json
2. Red Hat Bugzilla — https://bugzilla.redhat.com/show_bug.cgi?id=NNNNNNN
3. 벤더 보안 권고 — 예시 ID
4. Red Hat 생명주기 정책 — https://access.redhat.com/support/policy/updates/errata
5. EPSS — https://api.first.org/data/v1/epss?cve=CVE-2099-00001
6. CISA KEV — https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json
