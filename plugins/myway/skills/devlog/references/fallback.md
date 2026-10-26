# Fallback — Notion MCP 미연결 시

Notion MCP가 비활성이면 기록을 유실하지 않도록 SESSION_LOG.md로 폴백한다.

## 원칙

- **날짜별 누적 append만.** 기존 이력 덮어쓰기 절대 금지.
- 파일 경로: 프로젝트 루트의 `SESSION_LOG.md`
- 기록 후 사용자에게 1줄 알림: "Notion 미연결 → SESSION_LOG.md 기록함. 추후 수동 동기화 필요."

## SESSION_LOG.md append 포맷

```
## 📅 세션 백업: YYYY-MM-DD HH:MM
### ✅ 완료 작업 / 🚧 진행 중 / ⏭️ 다음 세션 즉시 실행 항목
### 🧩 런타임 스냅샷: Branch/Path · Last File · Active Errors · Last CMD
### 💬 인계 메모
```

## 동기화 복구

다음 세션에서 Notion MCP가 다시 연결되면, SESSION_LOG.md의 미동기화 블록을
해당 프로젝트 Notion 페이지 `## 개발 이력`에 표준 포맷(SKILL.md 3절)으로 옮긴다.
옮긴 블록은 SESSION_LOG.md에서 `[synced]` 표시만 남기고 삭제하지 않는다(이력 보존).
