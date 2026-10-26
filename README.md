# skill-myway

개인 작업 흐름을 하나로 묶은 Claude Code·Codex·Grok Build 겸용 플러그인 마켓플레이스입니다. 플러그인 `myway` 하나에 스킬 다섯 개가 들어 있습니다.

| 스킬 | 용도 |
|---|---|
| `writing` | 한국어 블로그·기술 기고·포털 게시글 작성과 편집. 공통 기준 하나에 프로필 셋(개인 블로그, 기술 기고, 포털 게시글) |
| `office-docs` | PPTX·DOCX·XLSX 작성 규격(브랜드 값은 프로필로 분리)과 정적 목차가 있는 장문 DOCX 빌드 |
| `rhel-cve` | RHEL CVE 영향도 분석과 6단계 보고서 |
| `admission-helper` | 대학 모집요강을 읽고 학생부 성적을 산출식에 대입해 지원 가능 여부 판정(진학 도우미) |
| `devlog` | 프로젝트 개발 이력 누적 기록(Notion, 미연결 시 SESSION_LOG.md) |

## 설치

같은 저장소가 Claude Code, Codex, Grok Build 마켓플레이스를 겸합니다.

| | Claude Code | Codex | Grok Build |
|---|---|---|---|
| 마켓플레이스 | `.claude-plugin/marketplace.json` | `.agents/plugins/marketplace.json` | `.grok-plugin/marketplace.json` |
| 플러그인 매니페스트 | `plugins/myway/.claude-plugin/plugin.json` | `plugins/myway/.codex-plugin/plugin.json` | 마켓플레이스 항목으로 대체 |
| 스킬 | `plugins/myway/skills/` (공용) | 공용 | 공용 |

**Claude Code**

```
/plugin marketplace add yjj3019/skill-myway
/plugin install myway@skill-myway
/plugin marketplace update skill-myway
```

**Codex**

```
codex plugin marketplace add yjj3019/skill-myway
codex plugin add myway@skill-myway
codex plugin marketplace upgrade skill-myway
codex plugin remove myway@skill-myway
```

codex-cli 0.164.0에서 로컬 경로로 `marketplace add`, `plugin add`, 스킬 5개 로드(`myway:<스킬>`), `plugin remove`까지 확인했습니다. `upgrade`는 Git 소스 마켓플레이스에만 동작합니다.

**Grok Build**

xAI 문서에는 공식 카탈로그(`xai-org/plugin-marketplace`)를 `/marketplace`로 보고 `grok plugin install <이름> --trust`로 설치하는 방법만 있습니다. 임의 저장소를 마켓플레이스로 추가하는 명령은 확인하지 못했습니다. 그래서 `.grok-plugin/marketplace.json`은 문서화된 형식으로 만들어 두었고(미검증), 확실한 방법은 스킬 복사입니다.

```
python3 scripts/install_skills.py --target grok
```

**마켓플레이스를 못 쓰는 환경**

스킬만 사용자 디렉터리에 넣습니다. Codex는 `~/.agents/skills`, Grok Build는 `~/.grok/skills`입니다.

```
python3 scripts/install_skills.py --target codex   # 기본값
python3 scripts/install_skills.py --target all     # 둘 다
python3 scripts/install_skills.py --link           # 복사 대신 링크(pull로 갱신)
```

스킬을 고치면 `VERSION`과 매니페스트 네 곳의 버전을 함께 올립니다. 검증기가 불일치를 잡습니다.

## 브랜드 프로필

조직 색상·폰트는 저장소에 넣지 않습니다. `office-docs`는 아래 순서로 프로필을 찾습니다.

1. 요청에서 사용자가 준 값
2. 작업 디렉터리의 `brand-profile.md`
3. `~/.claude/myway/brand-profile.md`
4. `references/brand-profile.default.md` (중립 기본값)

양식은 `plugins/myway/skills/office-docs/references/brand-profile.md`에 있습니다.

## 검증

```
python3 scripts/validate_repo.py
python3 scripts/run_tests.py
```

검사 항목: Claude·Codex·Grok 매니페스트 JSON, 버전 일치(`VERSION`), SKILL.md frontmatter와 참조 파일, 스크립트 문법, 민감 패턴.
저장소에 둘 수 없는 용어는 로컬 파일에 적고 `--terms 파일`로 넘깁니다(환경변수 `MYWAY_BANNED_TERMS_FILE`도 가능). 그 파일은 커밋하지 않습니다.

검증 현황과 미검증 항목은 [docs/VERIFICATION.md](docs/VERIFICATION.md)에 있습니다.

## 라이선스

Apache-2.0
