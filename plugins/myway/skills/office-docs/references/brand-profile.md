# brand-profile 양식

조직이나 개인의 문서 규격을 한 파일로 정의한다. 이 저장소에는 조직 고유 값을 넣지 않는다. 실제 값은 아래 위치에 둔다.

1. 작업 디렉터리의 `brand-profile.md`
2. `~/.claude/myway/brand-profile.md`

두 위치 모두 없으면 `brand-profile.default.md`를 쓴다. 파일을 새로 만들 때는 아래 양식을 복사해 값을 채운다. 비워 둔 항목은 default 값을 쓴다.

## 양식

```markdown
# brand-profile

## 색 (HEX, # 없이)
- primary:       본문 상단 바, 표 헤더, 강조
- deep:          본문 제목 텍스트
- accent:        보조 강조, 차트 2계열
- pale:          표 zebra, 옅은 배경
- ink:           본문 텍스트
- charcoal:      표지 제목
- muted:         푸터 텍스트, 캡션
- line:          구분선, 표 테두리
- footerBg:      푸터 바 배경
- alert:         리스크, 감소 수치
- positive:      증가, 달성 수치

## 폰트
- heading:       제목 폰트
- body:          본문 폰트
- mono:          코드, 숫자
- fallback:      미설치 시 대체 폰트

## 푸터
- copyright:     예: © 2026 조직명. All rights reserved.
- confidential:  예: Confidential (없으면 비움)
- wordmark:      워드마크 텍스트 (없으면 비움)
- wordmarkColor: 워드마크 전용 색. 다른 요소에 쓰지 않는다

## 표지
- arc:           true 이면 우상단 곡선 장식 사용. 기본 false
- badge:         표지 뱃지 문구 (없으면 비움)

## 서식 옵션
- signatureBlock: true 이면 문서 끝에 서명란. 기본 false
```

## 규칙

- 프로필에 없는 색을 임의로 추가하지 않는다.
- wordmarkColor는 워드마크에만 쓴다.
- 프로필에 조직명, 로고, 저작권 문구가 있어도 산출물 외의 공개 저장소나 스킬 파일에 복사하지 않는다.
- 사용자가 기존 템플릿 파일을 주면 그 템플릿의 마스터·테마 값이 프로필보다 우선한다.
- 폰트가 설치되지 않았으면 `fc-list`로 확인한 뒤 fallback을 쓰고, 컨테이너에 모두 없으면 `Noto Sans CJK KR`로 임시 대체하며 그 사실을 한 줄로 알린다.
