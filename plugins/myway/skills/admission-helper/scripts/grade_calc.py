#!/usr/bin/env python3
"""
대학별 학생부 환산점수 계산기.

대학마다 반영교과 · 학년비율 · 등급점수표가 다르다. 이 스크립트는 그 셋을
입력받아 실질 반영등급과 환산점수를 계산하고, 등급점수표의 비선형 구간
때문에 발생하는 추가 손실을 드러낸다.

사용법
------
1) 교과 평균등급으로 근사 계산 (이수단위 정보가 없을 때):

    python3 grade_calc.py \\
        --subjects "국어=3.0,영어=4.5,수학=5.2,사회=2.8,과학=3.4,한국사=3.0" \\
        --scale steep \\
        --formula "930+70*x/9.8"

2) 학년 가중치가 있는 대학 (1:2:3학년 = 20:30:50):

    python3 grade_calc.py \\
        --by-year "1=4.2,2=3.8,3=3.1" \\
        --year-weights "20:30:50" \\
        --scale linear

3) 이수단위를 아는 경우 (정밀):

    python3 grade_calc.py \\
        --weighted "국어:3.0:12,영어:4.5:10,수학:5.2:14,사회:2.8:18" \\
        --scale steep

내장 등급점수표
--------------
  steep   7등급부터 급락하는 유형 (9.8~0.2). 하위 등급에 불리
  linear  등급을 그대로 사용 (1~9). 대학 고유 표가 없을 때 비교용
  step5   1~5등급 0.5 간격, 6등급 이하 1.0 간격의 흔한 형태

대학 고유 표는 --scale-values 로 직접 넣는다:
    --scale-values "10,9.5,9,8.5,8,7,5,3,1"

주의
----
교과 평균등급으로 계산한 값은 근사다. 정확한 값은 과목별 이수단위가 필요하다.
출력에 APPROX 표시가 붙으면 리포트에도 근사임을 명시할 것.
"""

import argparse
import ast
import operator
import sys

SCALES = {
    "steep":  [9.80, 9.30, 8.80, 8.30, 7.80, 6.80, 4.60, 2.40, 0.20],
    "linear": [1, 2, 3, 4, 5, 6, 7, 8, 9],
    "step5":  [10.0, 9.5, 9.0, 8.5, 8.0, 7.0, 6.0, 5.0, 4.0],
}


_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv, ast.Pow: operator.pow, ast.USub: operator.neg}


def safe_eval(expr, x):
    """사칙연산, 거듭제곱, 괄호, 변수 x만 허용한다."""
    def walk(n):
        if isinstance(n, ast.Expression):
            return walk(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if isinstance(n, ast.Name) and n.id == "x":
            return x
        if isinstance(n, ast.BinOp) and type(n.op) in _OPS:
            return _OPS[type(n.op)](walk(n.left), walk(n.right))
        if isinstance(n, ast.UnaryOp) and type(n.op) in _OPS:
            return _OPS[type(n.op)](walk(n.operand))
        raise ValueError("허용되지 않는 식")
    return walk(ast.parse(expr, mode="eval"))


def interp(scale, grade):
    """등급(실수)을 등급점수로 선형보간. 3.4등급 -> 3등급과 4등급 사이."""
    g = max(1.0, min(9.0, float(grade)))
    lo = int(g)
    if lo >= 9:
        return float(scale[8])
    frac = g - lo
    return scale[lo - 1] + (scale[lo] - scale[lo - 1]) * frac


def parse_pairs(text, n=2):
    out = []
    for chunk in text.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        parts = chunk.split("=") if n == 2 else chunk.split(":")
        if len(parts) != n:
            sys.exit(f"형식 오류: '{chunk}'")
        out.append(parts)
    return out


def main():
    ap = argparse.ArgumentParser(description="대학별 학생부 환산점수 계산")
    ap.add_argument("--subjects", help='교과별 평균등급. "국어=3.0,영어=4.5"')
    ap.add_argument("--weighted", help='이수단위 포함. "국어:3.0:12,영어:4.5:10"')
    ap.add_argument("--by-year", help='학년별 등급. "1=5.73,2=6.50,3=5.80"')
    ap.add_argument("--year-weights", help='학년 가중치. "20:30:50" (기본 균등)')
    ap.add_argument("--scale", default="linear", choices=list(SCALES),
                    help="내장 등급점수표 (기본 linear)")
    ap.add_argument("--scale-values", help='대학 고유 표. "9.8,9.3,8.8,..." 9개')
    ap.add_argument("--formula", help='환산식. x는 평균등급점수. 예 "930+70*x/9.8"')
    ap.add_argument("--baseline", type=float, default=None,
                    help="비교 기준선 등급. 학생 프로필에서 가져와 지정한다.")
    args = ap.parse_args()

    if args.scale_values:
        vals = [float(v) for v in args.scale_values.split(",")]
        if len(vals) != 9:
            sys.exit("--scale-values 는 9개 값이어야 한다.")
        scale, scale_name = vals, "custom"
    else:
        scale, scale_name = SCALES[args.scale], args.scale

    items, approx = [], False

    if args.weighted:
        for name, grade, units in parse_pairs(args.weighted, 3):
            items.append((name, float(grade), float(units)))
    elif args.subjects:
        approx = True
        for name, grade in parse_pairs(args.subjects, 2):
            items.append((name, float(grade), 1.0))
    elif args.by_year:
        approx = True
        weights = ([float(w) for w in args.year_weights.split(":")]
                   if args.year_weights else None)
        pairs = parse_pairs(args.by_year, 2)
        for i, (year, grade) in enumerate(pairs):
            w = weights[i] if weights and i < len(weights) else 1.0
            items.append((f"{year}학년", float(grade), w))
    else:
        sys.exit("--subjects, --weighted, --by-year 중 하나가 필요하다.")

    total_w = sum(w for _, _, w in items)
    avg_grade = sum(g * w for _, g, w in items) / total_w
    avg_point = sum(interp(scale, g) * w for _, g, w in items) / total_w

    # 등급점수표를 역으로 풀어 "이 점수에 해당하는 등급"을 구한다.
    # 비선형 표에서는 산술평균 등급과 달라지며, 그 차이가 곧 구조적 손실이다.
    effective = 9.0
    for i in range(8):
        hi, lo = scale[i], scale[i + 1]
        if (hi >= avg_point >= lo) or (hi <= avg_point <= lo):
            span = lo - hi
            effective = (i + 1) + ((avg_point - hi) / span if span else 0)
            break
    else:
        effective = 1.0 if avg_point > scale[0] else 9.0

    print(f"\n등급점수표: {scale_name}  {scale}")
    print("-" * 62)
    print(f"{'항목':<12}{'등급':>8}{'가중':>8}{'등급점수':>12}")
    for name, g, w in items:
        print(f"{name:<12}{g:>8.2f}{w:>8.1f}{interp(scale, g):>12.3f}")
    print("-" * 62)
    print(f"산술평균 등급        {avg_grade:>8.3f}")
    print(f"평균 등급점수        {avg_point:>8.3f}")
    print(f"실질 반영등급        {effective:>8.3f}   <- 리포트에 쓸 값")

    delta = effective - avg_grade
    if abs(delta) >= 0.03:
        direction = "손실" if delta > 0 else "이득"
        print(f"\n[구조적 {direction}] 산술평균 대비 {delta:+.3f}등급.")
        print(f"  등급점수표의 간격이 균등하지 않아 발생한다.")
        print(f"  {'낮은 등급 구간의 급락 때문이다.' if delta > 0 else '완만한 구간에 성적이 몰려 있다.'}")

    if args.baseline is not None:
        diff = effective - args.baseline
        verdict = "유리" if diff < -0.05 else ("불리" if diff > 0.05 else "중립")
        print(f"\n기준선 {args.baseline:.2f} 대비 {diff:+.3f}등급 -> {verdict}")
    else:
        print("\n[기준선 미지정] --baseline 으로 학생의 기준 등급을 넣으면 유불리를 계산한다.")

    if args.formula:
        try:
            score = safe_eval(args.formula, avg_point)
            print(f"환산점수 ({args.formula}) = {score:.3f}")
        except Exception as e:
            print(f"환산식 오류: {e}", file=sys.stderr)

    if approx:
        print("\n[APPROX] 이수단위 미반영 근사값. 리포트에 근사임을 명시할 것.")
    print()


if __name__ == "__main__":
    main()
