// fmh.js — Format/Markup Helper
// 스타일 토큰을 한 곳에 모으고, 본문 요소를 함수로 캡슐화한다.
// 스타일 변경은 오직 이 파일의 STYLE 객체에서만 한다.

const {
  Paragraph, TextRun, HeadingLevel, AlignmentType, PageBreak,
  Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType,
} = require("docx");

// ─── 스타일 토큰 ────────────────────────────────────────────────
// 강조색은 환경변수 MANUAL_ACCENT(HEX, # 없이)로 바꾼다. 기본값은 중립 블루.
const STYLE = {
  bodyFont: "맑은 고딕",
  codeFont: "Consolas",
  size: { h1: 28, h2: 22, h3: 18, body: 20, code: 18, caption: 16 }, // half-points
  color: { text: "333333", accent: process.env.MANUAL_ACCENT || "1F4E79", codeBg: "F4F5F7", line: "D9D9D9" },
  page: { // A4 세로, 단위 twip (1cm ≈ 567)
    size: { width: 11906, height: 16838 },
    margin: { top: 1134, bottom: 1134, left: 1418, right: 1418 },
  },
};

// ─── 요소 헬퍼 ────────────────────────────────────────────────
function heading(text, level) {
  const map = { 1: HeadingLevel.HEADING_1, 2: HeadingLevel.HEADING_2, 3: HeadingLevel.HEADING_3 };
  const sz = { 1: STYLE.size.h1, 2: STYLE.size.h2, 3: STYLE.size.h3 }[level];
  return new Paragraph({
    heading: map[level],
    spacing: { before: level === 1 ? 360 : 240, after: 120 },
    children: [new TextRun({ text, bold: true, size: sz, font: STYLE.bodyFont, color: STYLE.color.text })],
  });
}

function body(text) {
  return new Paragraph({
    spacing: { after: 120, line: 312 },
    children: [new TextRun({ text, size: STYLE.size.body, font: STYLE.bodyFont, color: STYLE.color.text })],
  });
}

function code(text) {
  const lines = String(text).split("\n");
  return new Paragraph({
    shading: { type: ShadingType.SOLID, color: STYLE.color.codeBg, fill: STYLE.color.codeBg },
    spacing: { before: 80, after: 120 },
    border: { left: { style: BorderStyle.SINGLE, size: 12, color: STYLE.color.accent, space: 6 } },
    children: lines.flatMap((ln, i) => {
      const run = new TextRun({ text: ln, font: STYLE.codeFont, size: STYLE.size.code, color: STYLE.color.text });
      return i === 0 ? [run] : [new TextRun({ break: 1 }), run];
    }),
  });
}

// rows: string[][] (첫 행은 헤더)
function table(rows) {
  const make = (cells, header) => new TableRow({
    children: cells.map((c) => new TableCell({
      width: { size: Math.floor(100 / cells.length), type: WidthType.PERCENTAGE },
      shading: header ? { type: ShadingType.SOLID, color: STYLE.color.accent, fill: STYLE.color.accent } : undefined,
      children: [new Paragraph({ children: [new TextRun({
        text: String(c), bold: header, size: STYLE.size.caption, font: STYLE.bodyFont,
        color: header ? "FFFFFF" : STYLE.color.text,
      })] })],
    })),
  });
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    rows: rows.map((r, i) => make(r, i === 0)),
  });
}

function pageBreak() {
  return new Paragraph({ children: [new PageBreak()] });
}

module.exports = { STYLE, heading, body, code, table, pageBreak };
