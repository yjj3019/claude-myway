# 검증 현황

기준일 2026-10-28, 버전 1.4.3. 확인한 것만 VERIFIED로 적는다.

| 항목 | 상태 | 근거 |
|---|---|---|
| 저장소 구조·버전 일치·민감 패턴 | VERIFIED | Windows에서 `python scripts/validate_repo.py` PASS |
| 검증 스크립트 단위 테스트 | VERIFIED | Windows에서 `python scripts/run_tests.py` 24건 실행, 실패 0, skip 0 |
| Windows·macOS에서 검증 | VERIFIED(직전 푸시 기준) | 3f6d8b9 커밋의 CI 3개 OS 통과 |
| Claude Code에서 플러그인 설치 | VERIFIED(로컬 경로) | Windows·Claude Code 2.1.310의 격리된 설정에서 작업본 1.4.3 마켓플레이스 추가·설치 확인. 설치된 주요 변경 파일 5개가 작업본과 일치; 원격 배포본과 대화 중 호출은 미검증 |
| Codex에서 플러그인 설치 | VERIFIED(로컬 경로) | Windows의 격리된 CODEX_HOME에서 작업본 1.4.3 마켓플레이스 추가·설치 확인. 설치된 HWP 읽기 지침이 작업본과 일치; 원격 배포본과 대화 중 호출은 미검증 |
| Claude·Codex 대화 중 스킬 실제 호출 | PARTIAL | Windows의 임시 프로젝트에 복사한 office-docs 스킬을 Codex CLI 대화가 발견하고 읽음. HWPX 파일 없이 원본·쪽 대조 지침을 응답; PowerShell 출력 한글이 깨져 JSON 이스케이프로 재확인함. 플러그인 설치 경로의 호출과 Claude 호출은 미검증 |
| writing 비교 평가 | PARTIAL | `writing-evaluation.md`에 가상 원고 1건과 4개 사례의 블라인드 판정 기록. 자동 스킬 호출·반복 검증은 미실행 |
| Office 문서 생성·시각 검증 | NOT VERIFIED | 이번 변경에서 실제 산출물 생성·렌더링·잘림 확인은 하지 않음 |
| HWP/HWPX 선택 도구 읽기 | PARTIAL | Windows·Node 24·kordoc 4.24.13에서 합성 HWPX와 공개 HWP/HWPX 각 1건을 오프라인으로 읽음. 일부 표·경고 확인; 두 대응 PDF와 쪽 수 차이, 판본 일치 미확인. 편집·자동 호출 미검증 |
| 래스터 이미지 OCR | PARTIAL | 같은 환경에서 공개 PDF 쪽을 이미지로 렌더한 1쪽을 오프라인 OCR로 읽음. 실제 스캔은 아님. 저신뢰 줄 폐기 경고, 표 열·셀의 차이와 문자 오인이 있어 원본 대조 필요. 스캔 PDF·반복·입시 요강 미검증 |
| RHEL CVE 판정·보고서 | NOT VERIFIED | 저장소 테스트의 가상 보고서 검사 통과만으로 실제 CVE 출처·판정을 검증하지 않음 |
| 입시 요강·성적 산출 | NOT VERIFIED | 저장소의 산술식 테스트만으로 실제 요강 해석이나 성적 산출을 검증하지 않음 |
| devlog 기록 | NOT VERIFIED | 이번 변경에서 외부 기록 서비스나 로컬 기록 흐름은 실행하지 않음 |
| Grok Build 설치·실행 | NOT VERIFIED | CLI가 없어 실행하지 못함 |
