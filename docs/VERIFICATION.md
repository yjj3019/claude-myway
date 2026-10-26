# 검증 현황

기준일 2026-10-26, 버전 1.4.0. 확인한 것만 VERIFIED로 적는다.

| 항목 | 상태 | 근거 |
|---|---|---|
| 저장소 구조·버전 일치·민감 패턴 | VERIFIED | `python3 scripts/validate_repo.py` PASS |
| 검증 스크립트 단위 테스트 | VERIFIED | `python3 scripts/run_tests.py` 22건 실행, 실패 0, skip 0 |
| Windows·macOS에서 검증 | VERIFIED(직전 푸시 기준) | 3f6d8b9 커밋의 CI 3개 OS 통과 |
| Claude Code에서 플러그인 설치 | VERIFIED | 로컬 경로와 GitHub 원본 양쪽에서 설치 확인 |
| Codex에서 플러그인 설치 | VERIFIED | 격리된 홈에서 마켓플레이스 추가와 설치 확인 |
| Claude·Codex 대화 중 스킬 실제 호출 | NOT VERIFIED | 설치까지만 확인함 |
| Grok Build 설치·실행 | NOT VERIFIED | CLI가 없어 실행하지 못함 |
