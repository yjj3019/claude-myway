# skill-myway

글쓰기, 문서 작업, 보안 분석, 진학 상담, 개발 이력을 위한 개인 스킬 모음입니다. Claude Code·Codex·Grok Build에서 같은 다섯 개의 스킬을 사용합니다.

## 스킬

| 스킬 | 주요 기능 |
| --- | --- |
| `writing` | 한국어 블로그·기술 기고·게시글·업무 문서 작성과 편집 |
| `office-docs` | PPTX·DOCX·XLSX 작성 규격, 장문 DOCX 빌드, HWP/HWPX 원문 읽기 |
| `rhel-cve` | Red Hat 자료를 바탕으로 RHEL CVE 영향도 분석과 보고서 작성 |
| `admission-helper` | 대학 모집요강 확인과 학생부 성적 산출·지원 자격 검토 |
| `devlog` | Notion에 개발 이력 기록. 연결되지 않으면 `SESSION_LOG.md`에 기록 |

HWP/HWPX 읽기는 이미 설치된 도구를 사용하는 선택 기능입니다. 추출한 내용과 페이지는 원본이나 판본이 확인된 렌더와 대조해야 합니다. 자세한 절차는 [한글 문서 읽기 지침](plugins/myway/skills/office-docs/references/hwp-read.md)을 참고하세요.

## 설치

### Claude Code

Claude Code에서 실행합니다.

```text
/plugin marketplace add yjj3019/skill-myway
/plugin install myway@skill-myway
```

마켓플레이스 갱신: `/plugin marketplace update skill-myway`

### Codex

터미널에서 실행합니다.

```sh
codex plugin marketplace add yjj3019/skill-myway
codex plugin add myway@skill-myway
```

Git 소스 마켓플레이스 갱신은 `codex plugin marketplace upgrade skill-myway`, 제거는 `codex plugin remove myway@skill-myway`를 사용합니다. 로컬 경로 설치와 실제 호출을 확인한 범위는 [검증 현황](docs/VERIFICATION.md)에 기록되어 있습니다.

### Grok Build 또는 스킬 직접 설치

저장소를 내려받은 뒤 해당 디렉터리에서 실행합니다.

```sh
python3 scripts/install_skills.py --target grok   # Grok Build
python3 scripts/install_skills.py --target codex  # Codex
python3 scripts/install_skills.py --target all    # 둘 다
```

각각 `~/.grok/skills`, `~/.agents/skills`에 복사합니다. 같은 이름의 스킬은 기본적으로 건너뛰며, 에이전트를 다시 시작하면 목록에 나타납니다. `--link`는 복사 대신 심볼릭 링크를 만들고 Windows에서는 별도 권한이 필요할 수 있습니다. `--force`는 기존 같은 이름의 스킬을 교체하므로 먼저 내용을 확인하세요.

Grok Build의 임의 저장소 마켓플레이스 추가와 `.grok-plugin/marketplace.json`의 실제 동작은 확인하지 못했습니다.

## 브랜드 프로필

`office-docs`는 요청에서 제공된 값, 작업 디렉터리의 `brand-profile.md`, `~/.claude/myway/brand-profile.md`, 중립 기본값 순서로 브랜드 설정을 찾습니다. 프로필 양식은 [brand-profile.md](plugins/myway/skills/office-docs/references/brand-profile.md)에 있습니다.

## 검증과 유지보수

```sh
python3 scripts/validate_repo.py
python3 scripts/run_tests.py
```

검증기는 매니페스트, 버전 일치, 스킬 지침과 참조 파일, 스크립트 문법 및 민감 패턴을 확인합니다. 저장소에 둘 수 없는 검사 용어는 별도 로컬 파일로 만들고 `--terms 파일` 또는 `MYWAY_BANNED_TERMS_FILE` 환경변수로 전달하세요. 해당 파일은 커밋하지 않습니다.

스킬을 수정할 때는 `VERSION`과 각 플랫폼의 버전 정보를 함께 갱신합니다. 확인된 내용과 미검증 항목은 [docs/VERIFICATION.md](docs/VERIFICATION.md)를 참고하세요.

## 라이선스

[Apache License 2.0](LICENSE)
