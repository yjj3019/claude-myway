# DOCX 규격

내장 `docx` 스킬(docx-js)로 생성한다. 기존 .docx 편집은 unpack → XML 수정 → repack. 값은 brand-profile에서 가져온다.

## 문서 유형별 골격

### 제안서·가치 제안
1. 표지: 제목, 대상, 일자
2. 목차 (자동 생성)
3. 요약 (1페이지, 핵심 가치와 수치)
4. 배경·현황·문제 정의
5. 제안 솔루션 (구조, 기능)
6. 기대효과 (표와 수치, 출처 명시)
7. 추진 계획·일정
8. 부록

### 기술 검토·점검 문서
1. 개요 (목적, 범위, 환경)
2. 점검·검토 항목
3. 발견사항 (심각도 표기)
4. 조치 방안
5. 결론과 권고

## 스타일 (docx-js)

```javascript
const { Document, Paragraph, TextRun, BorderStyle } = require("docx");
// T: brand-profile 값 (primary, deep, ink, muted, line, pale, heading, body)
const doc = new Document({
  styles: {
    default: { document: { run: { font: T.body, size: 22, color: T.ink } } },  // 11pt
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal",
        run: { font: T.heading, size: 56, color: T.deep, bold: true },
        paragraph: { spacing: { after: 240 } } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal",
        run: { font: T.heading, size: 32, color: T.primary, bold: true },
        paragraph: { spacing: { before: 360, after: 160 },
          border: { bottom: { color: T.line, space: 6, style: BorderStyle.SINGLE, size: 6 } } } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal",
        run: { font: T.heading, size: 26, color: T.deep, bold: true },
        paragraph: { spacing: { before: 240, after: 120 } } },
      { id: "Caption", name: "Caption", basedOn: "Normal",
        run: { font: T.body, size: 18, color: T.muted, italics: true } },
    ],
  },
});
```

## 타이포와 페이지

| 요소 | 크기(pt) | docx size | 폰트 | 색 |
|---|---|---|---|---|
| 표지 제목 | 28 | 56 | heading Bold | deep |
| H1 | 16 | 32 | heading Bold | primary, 하단 구분선 |
| H2 | 13 | 26 | heading Bold | deep |
| 본문 | 11 | 22 | body | ink |
| 캡션·각주 | 9 | 18 | body | muted |

- 줄간격 1.4~1.5, 단락 뒤 간격 8pt.
- A4, 여백 상하 25mm, 좌우 22mm.
- 푸터: 중앙 쪽번호. 우측에 copyright와 confidential(프로필에 있을 때만, muted 8.5pt).

## 표

- 헤더 행: primary 채움 + 흰 글씨 Bold.
- 본문 행: zebra 짝수행 pale, 가로 구분선 line만.
- 셀 패딩을 충분히 두고 숫자는 우측 정렬, 단위를 표기한다.

```javascript
new TableCell({
  shading: { fill: T.primary },
  children: [new Paragraph({ children: [
    new TextRun({ text: "항목", bold: true, color: "FFFFFF", font: T.heading })] })],
});
```

## 강조

별도 요구가 없으면 콜아웃 박스를 쓰지 않는다. 필요하면 본문 단락의 굵은 글씨나 표 한 행으로 처리한다. 리스크·경고 표시가 필요할 때는 표의 해당 셀 글자색을 alert로 쓴다.

## 수치 표기

- 통화와 퍼센트는 단위를 명시한다. "절감액(백만원)", "12.5%".
- 인용 수치는 각주에 출처와 일자를 적는다. 자료에 없는 수치를 만들지 않는다.

## 서명란

`signatureBlock: true`이거나 사용자가 요청할 때만 문서 끝에 작성자·검토자·승인자 표를 둔다.

## 검증

```bash
soffice --headless --convert-to pdf output.docx
pdftoppm -jpeg -r 150 output.pdf page
unzip -p output.docx word/document.xml | grep -iE "lorem|ipsum|xxxx|샘플|TBD" && echo "FIX NEEDED"
```

장문 문서(챕터 다수, 코드 블록, 정적 목차)는 `references/long-manual.md`의 2-pass 파이프라인을 쓴다.
