// fbuild.js — 2-pass TOC 빌드 엔진
// Pass1: TOC 없이 빌드 → soffice PDF 변환 → gen_toc.py로 페이지 추출
// Pass2: 정적 TOC(페이지번호 포함)를 맨 앞에 붙여 최종 docx 빌드
//
// 사용: node fbuild.js [출력파일명]
// 산출물: $OUT_DIR/<출력파일명>. OUT_DIR 미지정 시 /mnt/user-data/outputs가 있으면 그곳, 없으면 현재 디렉터리.
// 목차가 2페이지 이상이면 TOC_PAGES=<목차 페이지 수>로 지정한다(기본 1).

const fs = require("fs");
const path = require("path");
const os = require("os");
const { execFileSync } = require("child_process");
const {
  Document, Packer, Paragraph, TextRun, TabStopType, TabStopPosition, AlignmentType,
} = require("docx");
const m = require("./fmh");
const { TITLES, chapters } = require("./fcontent");

const OUT_DIR = process.env.OUT_DIR
  || (fs.existsSync("/mnt/user-data/outputs") ? "/mnt/user-data/outputs" : process.cwd());
const TOC_PAGES = Number(process.env.TOC_PAGES || 1);
const SCRIPT_DIR = __dirname;
const outName = process.argv[2] || "RHEL_운영매뉴얼.docx";

function sectionProps() {
  return { page: { size: { width: m.STYLE.page.size.width, height: m.STYLE.page.size.height }, margin: m.STYLE.page.margin } };
}

// TOC 단락: "제목 .......... 페이지" (탭 리더)
function tocEntry(title, page) {
  return new Paragraph({
    tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX, leader: "dot" }],
    spacing: { after: 80 },
    children: [
      new TextRun({ text: title, size: m.STYLE.size.body, font: m.STYLE.bodyFont, color: m.STYLE.color.text }),
      new TextRun({ text: `\t${page ?? "-"}`, size: m.STYLE.size.body, font: m.STYLE.bodyFont, color: m.STYLE.color.text }),
    ],
  });
}

function buildDoc(tocBlocks) {
  const children = [];
  if (tocBlocks) {
    children.push(new Paragraph({ children: [new TextRun({ text: "목차", bold: true, size: m.STYLE.size.h1, font: m.STYLE.bodyFont, color: m.STYLE.color.text })], spacing: { after: 240 } }));
    children.push(...tocBlocks, m.pageBreak());
  }
  children.push(...chapters());
  return new Document({ sections: [{ properties: sectionProps(), children }] });
}

async function save(doc, file) {
  const buf = await Packer.toBuffer(doc);
  fs.writeFileSync(file, buf);
}

(async () => {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "rhelman-"));

  // Pass 1
  const p1docx = path.join(tmp, "pass1.docx");
  await save(buildDoc(null), p1docx);
  console.error("[1/4] Pass1 docx 빌드 완료");

  execFileSync("soffice", ["--headless", "--convert-to", "pdf", "--outdir", tmp, p1docx], { stdio: "inherit" });
  const p1pdf = path.join(tmp, "pass1.pdf");
  console.error("[2/4] PDF 변환 완료");

  const titlesJson = path.join(tmp, "titles.json");
  const tocJson = path.join(tmp, "toc.json");
  fs.writeFileSync(titlesJson, JSON.stringify(TITLES, null, 2));
  execFileSync("python3", [path.join(SCRIPT_DIR, "gen_toc.py"), p1pdf, titlesJson, tocJson], { stdio: "inherit" });
  const toc = JSON.parse(fs.readFileSync(tocJson, "utf-8"));
  console.error("[3/4] toc.json 추출 완료");

  // Pass 2 (TOC가 차지하는 페이지만큼 본문이 밀리므로 TOC_PAGES 보정)
  const tocBlocks = toc.map((e) => tocEntry(e.title, e.page == null ? null : e.page + TOC_PAGES));
  const finalPath = path.join(OUT_DIR, outName);
  await save(buildDoc(tocBlocks), finalPath);
  console.error(`[4/4] 최종 빌드 완료 → ${finalPath}`);
})().catch((e) => { console.error("BUILD FAILED:", e); process.exit(1); });
