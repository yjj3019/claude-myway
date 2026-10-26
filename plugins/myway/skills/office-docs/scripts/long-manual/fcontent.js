// fcontent.js — 콘텐츠 정의 (템플릿)
// 아래 TITLES와 본문은 구조를 보여 주는 예시다. 실제 매뉴얼 내용으로 교체한다.
// ⚠️ 챕터 구조를 바꾸면 TITLES 배열과 chapters() 본문을 함께 수정한다.
//    gen_toc.py의 추출 대상은 이 TITLES와 일치해야 한다.
//
// 실제 본문(챕터 다수 + 부록)을 채울 때:
//   1) TITLES에 정확한 제목 문자열을 순서대로 나열
//   2) chapters()에서 각 제목에 대응하는 본문을 h/b/c/t 헬퍼로 작성
//   3) 제목 문자열은 TOC 매칭 키이므로 본문 heading과 100% 일치시킨다

const m = require("./fmh");

// TOC 매칭 키 = 본문 H1 제목. 순서가 곧 문서 순서.
const TITLES = [
  "1. 개요",
  "2. 시스템 초기 설정",
  "3. 사용자 및 권한 관리",
  "부록 A. 점검 체크리스트",
];

// 각 제목 → 본문 블록 배열. 헬퍼: m.heading/body/code/table/pageBreak
function chapters() {
  const out = [];

  out.push(m.heading(TITLES[0], 1));
  out.push(m.body("본 매뉴얼은 대상 시스템의 RHEL 운영 표준을 기술한다. 신규 운영자가 사전 지식 없이 절차를 따를 수 있도록 설정값과 근거를 포함한다."));
  out.push(m.pageBreak());

  out.push(m.heading(TITLES[1], 1));
  out.push(m.heading("2.1 시간 동기화 (chrony)", 2));
  out.push(m.body("NTP는 chrony로 구성한다. 서버 주소는 환경에 맞게 치환한다."));
  out.push(m.code("# /etc/chrony.conf\nserver <NTP_SERVER> iburst\nmakestep 1.0 3\nrtcsync"));
  out.push(m.body("적용 후 동기화 상태를 확인한다."));
  out.push(m.code("$ chronyc sources -v\n$ timedatectl status"));
  out.push(m.pageBreak());

  out.push(m.heading(TITLES[2], 1));
  out.push(m.body("계정은 최소 권한 원칙에 따라 부여한다. 표준 권한 매트릭스는 다음과 같다."));
  out.push(m.table([
    ["구분", "권한", "비고"],
    ["운영자", "sudo (제한)", "감사 로그 필수"],
    ["배치", "특정 명령만", "NOPASSWD 금지"],
  ]));
  out.push(m.pageBreak());

  out.push(m.heading(TITLES[3], 1));
  out.push(m.body("배포 전 점검 항목을 표로 관리한다."));
  out.push(m.table([
    ["항목", "기준", "상태"],
    ["SELinux", "Enforcing", "□"],
    ["방화벽", "firewalld active", "□"],
  ]));

  return out;
}

module.exports = { TITLES, chapters };
