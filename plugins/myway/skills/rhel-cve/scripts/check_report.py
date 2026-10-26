#!/usr/bin/env python3
"""단건 CVE 리포트(CVE-YYYY-NNNNN_리포트.md)가 report-format.md 규칙을 지키는지 검사한다.

사용법:
    python3 check_report.py /mnt/user-data/outputs/CVE-YYYY-NNNNN_리포트.md

통과 시 exit 0, 위반이 하나라도 있으면 위반 목록을 출력하고 exit 1.
"""
import re
import sys
from pathlib import Path

TITLE_RE = re.compile(r"^# CVE-\d{4}-\d{4,} 보안 취약점 리포트$")
H2 = [
    "## 1. 개요",
    "## 2. 심각도(CVSS) 비교",
    "## 3. 실제 악용 가능성 (EPSS · CISA KEV)",
    "## 4. 완화 방법 (Mitigation)",
    "## 5. 영향받는 제품 및 패치",
    "## 6. 출처",
]
OVERVIEW_ROWS = ["CVE ID", "컴포넌트", "요약", "Red Hat 심각도", "공개일", "최종 갱신일", "CWE 분류"]
CVSS_HEADER = ["평가 기관", "버전", "점수", "벡터", "등급"]
EXPLOIT_HEADER = ["지표", "값", "조회 기준일"]
EXPLOIT_ROWS = ["EPSS 점수", "EPSS 백분위", "CISA KEV 등재 여부"]
PRODUCT_HEADER = ["제품", "컴포넌트", "상태", "근거", "RHSA", "수정 버전(x86_64)", "발행일"]
STATES = {
    "수정됨(Fixed)", "영향 있음(Affected)", "패치 보류(Fix deferred)",
    "패치 계획 없음(Will not fix)", "지원 범위 밖(Out of support scope)",
    "조사 중(Under investigation)", "영향 없음(Not affected)",
}
FIXED_QUOTE = ('> 이 목록에서 명시적으로 "영향 없음(not affected)"으로 표기되지 않은 이상, '
               '목록에 포함된 제품의 모든 마이너 업데이트 스트림에 포함된 기존 패키지 버전은 '
               '전체 분석이 수행되지 않았더라도 취약한 것으로 간주해야 합니다.')
HTML_RE = re.compile(r"</?[a-zA-Z][a-zA-Z0-9]*(\s[^>]*)?/?>")
EPOCH_RE = re.compile(r"(?<![A-Z]{2}[SBE]A)(?<=[A-Za-z0-9_.+])-\d+:\d")
EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\u2705\u274C]")
ALIGN_RE = re.compile(r"^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?$")


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def strip_code(lines):
    """코드 블록 안의 줄은 빈 문자열로 바꿔 줄 번호를 유지한다."""
    out, in_code = [], False
    for line in lines:
        if line.strip().startswith("```"):
            in_code = not in_code
            out.append("")
            continue
        out.append("" if in_code else line)
    return out


def tables(section):
    """(시작 줄 번호, [행 문자열...]) 목록. 구분선 행은 제외하지 않는다."""
    found, cur, start = [], [], None
    for no, line in section:
        if line.lstrip().startswith("|"):
            if not cur:
                start = no
            cur.append(line)
        elif cur:
            found.append((start, cur))
            cur = []
    if cur:
        found.append((start, cur))
    return found


def source_category(line):
    low = line.lower()
    if "bugzilla" in low:
        return 2
    if "support/policy/updates/errata" in low or "생명주기" in line:
        return 4
    if "epss" in low:
        return 5
    if "kev" in low:
        return 6
    if "access.redhat.com/security/cve" in low:
        return 1
    return 3


def check(path):
    raw = Path(path).read_text(encoding="utf-8-sig").splitlines()
    lines = strip_code(raw)
    errors = []

    def err(no, msg):
        errors.append(f"L{no}: {msg}" if no else msg)

    numbered = list(enumerate(lines, 1))
    content = [(n, l) for n, l in numbered if l.strip()]
    if not content or not TITLE_RE.match(content[0][1].strip()):
        err(content[0][0] if content else 0, "첫 줄 제목이 '# CVE-YYYY-NNNNN 보안 취약점 리포트' 형식이 아님")

    # H2 순서·문구
    h2 = [(n, l.strip()) for n, l in numbered if l.startswith("## ")]
    if [t for _, t in h2] != H2:
        err(0, f"H2 불일치. 기대={H2} 실제={[t for _, t in h2]}")
        return errors  # 섹션 분리가 불가능하므로 이후 검사 생략

    bounds = [n for n, _ in h2] + [len(lines) + 1]
    sec = {i + 1: [(n, lines[n - 1]) for n in range(bounds[i] + 1, bounds[i + 1])]
           for i in range(6)}

    # H3
    for n, l in numbered:
        if l.startswith("### "):
            if l.strip() != "### 취약점 설명" or not (bounds[0] < n < bounds[1]):
                err(n, f"허용되지 않은 H3: {l.strip()}")
    if not any(l.strip() == "### 취약점 설명" for _, l in sec[1]):
        err(0, "1번 섹션에 '### 취약점 설명' 없음")

    # 공통: HTML, 표 정렬, 표 안 서식, epoch
    for n, l in numbered:
        if HTML_RE.search(l):
            err(n, f"HTML 태그: {HTML_RE.search(l).group(0)}")
        if l.lstrip().startswith("|"):
            if ALIGN_RE.match(l.strip()) and ":" in l:
                err(n, "표 정렬 지정(:) 사용")
            if "**" in l or "`" in l or EMOJI_RE.search(l):
                err(n, "표 안에 굵게/백틱/이모지 사용")
        if EPOCH_RE.search(l):
            err(n, f"NVR epoch 잔존: {EPOCH_RE.search(l).group(0)}")

    def one_table(s, label):
        t = tables(sec[s])
        if not t:
            err(bounds[s - 1], f"{label} 표 없음")
            return None, []
        start, rows = t[0]
        body = [cells(r) for r in rows[2:]]
        return (start, cells(rows[0])), body

    # 1. 개요 표
    head, body = one_table(1, "1번")
    if head:
        if head[1] != ["항목", "내용"]:
            err(head[0], f"1번 표 컬럼 불일치: {head[1]}")
        if [r[0] for r in body] != OVERVIEW_ROWS:
            err(head[0], f"1번 표 행 불일치. 기대={OVERVIEW_ROWS} 실제={[r[0] for r in body]}")

    # 2. CVSS 표 + 인용구
    head, body = one_table(2, "2번")
    if head:
        if head[1] != CVSS_HEADER:
            err(head[0], f"2번 표 컬럼 불일치: {head[1]}")
        orgs = [r[0] for r in body]
        firsts = []
        for o in orgs:
            key = "Red Hat" if o.startswith("Red Hat") else "NVD" if o.startswith("NVD") else "cve.org" if o.startswith("cve.org") else o
            if not firsts or firsts[-1] != key:
                firsts.append(key)
        if firsts != ["Red Hat", "NVD", "cve.org"]:
            err(head[0], f"2번 표 기관 순서 불일치(Red Hat → NVD → cve.org): {orgs}")
    if not any(l.startswith(">") for _, l in sec[2]):
        err(bounds[1], "2번 표 아래 인용구 없음")

    # 3. EPSS·KEV
    head, body = one_table(3, "3번")
    if head:
        if head[1] != EXPLOIT_HEADER:
            err(head[0], f"3번 표 컬럼 불일치: {head[1]}")
        if [r[0] for r in body] != EXPLOIT_ROWS:
            err(head[0], f"3번 표 행 불일치: {[r[0] for r in body]}")
    s3 = sec[3]
    idx = next((i for i, (_, l) in enumerate(s3) if l.strip() == "**해석**"), None)
    if idx is None:
        err(bounds[2], "3번 섹션에 '**해석**' 없음")
    else:
        bullets = [l for _, l in s3[idx + 1:] if l.startswith("- ")]
        if len(bullets) != 3:
            err(s3[idx][0], f"해석 불릿 수 {len(bullets)}개 (3개여야 함)")

    # 5. 제품 표 + 고정 인용구
    head, body = one_table(5, "5번")
    if head:
        if head[1] != PRODUCT_HEADER:
            err(head[0], f"5번 표 컬럼 불일치: {head[1]}")
        else:
            for i, r in enumerate(body):
                no = head[0] + 2 + i
                if len(r) != 7:
                    err(no, f"5번 표 행 컬럼 수 {len(r)}")
                    continue
                state, rhsa, nvr, date = r[2], r[4], r[5], r[6]
                if state not in STATES:
                    err(no, f"상태 표기 불일치: {state}")
                if state == "수정됨(Fixed)":
                    if not re.match(r"^RH[SBE]A-\d{4}:\d+$", rhsa):
                        err(no, f"수정됨 행 RHSA 형식 오류: {rhsa}")
                    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
                        err(no, f"수정됨 행 발행일 형식 오류: {date}")
                elif state in STATES and (rhsa, nvr, date) != ("-", "-", "-"):
                    err(no, "수정됨이 아닌 행은 RHSA·수정 버전·발행일이 '-'여야 함")
    quotes = [(n, l.strip()) for n, l in sec[5] if l.startswith(">")]
    if len(quotes) != 1 or quotes[0][1] != FIXED_QUOTE:
        err(quotes[0][0] if quotes else bounds[4], "5번 인용구는 고정 문구 1개만 허용")
    elif any(l.strip() for n, l in sec[5] if n > quotes[0][0]):
        err(quotes[0][0], "5번 고정 인용구 뒤에 추가 텍스트(메타정보 등) 존재")

    # 6. 출처
    items = [(n, l) for n, l in sec[6] if re.match(r"^\d+\. ", l)]
    nums = [int(re.match(r"^(\d+)\.", l).group(1)) for _, l in items]
    if nums != list(range(1, len(nums) + 1)):
        err(bounds[5], f"출처 번호가 1부터 연속이 아님: {nums}")
    cats = [source_category(l) for _, l in items]
    if cats != sorted(cats):
        err(bounds[5], f"출처 순서 위반(카테고리 순서 {cats})")
    for need, name in ((1, "Red Hat CVE 페이지"), (5, "EPSS"), (6, "CISA KEV")):
        if need not in cats:
            err(bounds[5], f"출처에 {name} 없음")

    return errors


def main(argv):
    if len(argv) != 1:
        print(__doc__, file=sys.stderr)
        return 2
    errors = check(argv[0])
    if errors:
        print(f"FAIL ({len(errors)}건)")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
