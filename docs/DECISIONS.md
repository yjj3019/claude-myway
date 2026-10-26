# 설계 결정

## D-001 플러그인 1개, 스킬 여러 개
관련 작업(글쓰기, 오피스 문서, CVE, 대입 요강 분석, 개발이력)을 `myway` 하나로 설치하고 업데이트하도록 묶었다. 스킬은 용도별로 나눠 트리거가 겹치지 않게 했다.

## D-002 브랜드 값은 프로필로 분리
조직 고유 색상·폰트·서명란은 저장소에 두지 않는다. 기본값은 중립 팔레트이며 조직 값은 로컬 프로필로 주입한다. 이유: 공개 저장소에 특정 기관을 드러내지 않기 위해서다.

## D-003 글쓰기는 공통 기준 + 프로필 3종
말투와 형식이 충돌하는 세 가지 글쓰기 규칙(합니다체/해요체, 이모지 유무)을 프로필로 나눴다. 사실과 개인정보 경계는 모든 프로필에 우선한다.

## D-004 devlog의 Notion 부모 페이지는 하드코딩하지 않는다
사용 여부와 목적지를 첫 기록 전에 사용자에게 확인한다. 값은 요청 또는 `PROGRESS.md`에서만 읽는다.

## D-005 AI-Harness에서 가져온 것
검증 스크립트, 테스트, CI, DECISIONS.md, compound-log.md, CLAUDE.md만 가져왔다. 훅과 서브에이전트는 이 저장소의 범위가 아니라 포함하지 않았다.

## D-006 민감어 검사는 로컬 목록으로
저장소에 금지어 목록을 두면 그 자체가 유출이므로, 일반 패턴만 저장소에 두고 금지어는 `--terms` 로컬 파일로 받는다.

## D-007 Claude Code·Codex 겸용 마켓플레이스
스킬은 `SKILL.md` 표준이라 한 벌을 공유한다. 매니페스트만 플랫폼별로 둔다: Claude는 `.claude-plugin/`, Codex는 `.agents/plugins/marketplace.json`과 `.codex-plugin/plugin.json`(호환 레이아웃, codex-cli 0.164.0에서 설치·스킬 로드 확인). Codex 문서가 권하는 루트 `plugin.json` 포터블 형식은 Claude 쪽 구조와 충돌 여부를 확인하지 못해 쓰지 않았다. 스킬별 `agents/openai.yaml`은 Codex 선택기 표시용이다. `scripts/install_skills.py`는 마켓플레이스를 못 쓰는 환경용 대체 경로로 남긴다.

## D-008 스킬 description은 짧게
Codex는 설치된 스킬이 많으면 description부터 줄이고 일부는 목록에서 뺀다. 트리거 키워드를 앞쪽에 두고 길이를 600자 안팎으로 유지한다.

## D-009 Grok Build 지원 범위
Grok Build는 `~/.grok/skills`의 SKILL.md를 읽는다(문서 확인). 플러그인 카탈로그는 xAI 공식 저장소 PR 방식이고, 임의 저장소를 마켓플레이스로 추가하는 방법은 문서에서 확인하지 못했다. `.grok-plugin/marketplace.json`은 공개된 스키마대로 두되 동작은 미검증으로 표시한다. 확실한 경로는 `install_skills.py --target grok`다. 공식 카탈로그에 올리려면 원격 plugin은 40자 commit sha 고정이 필요하다.

## D-010 rhel-manual을 office-docs에 통합
rhel-manual은 이름과 달리 RHEL 전용이 아니라 장문 DOCX 빌드 파이프라인이다. office-docs의 docx 영역과 겹쳐 트리거가 갈렸다. `references/long-manual.md`와 `scripts/long-manual/`로 옮기고 office-docs description에 매뉴얼 빌드 트리거를 넣었다. rhel-cve는 보안 분석이라 도메인이 달라 따로 둔다.

## D-011 저장소와 마켓플레이스 이름을 skill-myway로 통일
저장소 이름이 skill-myway로 바뀌었고 Claude·Codex·Grok 겸용이라 `claude-` 접두어가 맞지 않는다. 마켓플레이스 이름과 설치 ID(`myway@skill-myway`)를 맞췄다.

## D-012 예시 데이터는 가상 값만
실제 CVE로 만든 리포트 예시를 가상 ID(CVE-2099-00001)와 가상 패키지로 바꿨다. 검증기는 2099 외의 CVE·RHSA 번호를 막는다. 특정 정보는 각 스킬의 "특정 정보가 필요할 때" 절차(묶음 질문, 저장소에 되쓰지 않음)로 받는다.

## D-013 admission-helper 추가
기존 개인 스킬 univ-admission-analysis를 영어 이름 admission-helper(진학 도우미)로 통합했다. 학생 정보는 저장소에 두지 않고 빈 프로필 서식에서 질문/답변으로 받는다. grade_calc.py의 환산식은 `eval` 대신 AST 기반으로 사칙연산과 `x`만 허용한다. 연도 의존 문구(학년도, 권역 목록)는 일반화했다.

## D-014 AI-Harness 2026-10-26 업데이트 반영 범위
가져온 것: 테스트 수 검증(0건·전체 skip은 실패, `scripts/run_tests.py`), 검증 현황표(`docs/VERIFICATION.md`), CLAUDE.md의 지침 충돌·검증 의미·승인 경계 규칙, CI 최소 권한. 가져오지 않은 것: phase-gate와 attestation, ToolBroker, 지식 그래프 평가, evidence-first-harness 스킬. 이 저장소에는 Phase 흐름과 훅·서브에이전트가 없고, 선택 도구는 측정 전에 도입하지 않는다는 원본 문서의 결론을 따랐다.
