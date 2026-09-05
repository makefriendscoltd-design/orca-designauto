# -*- coding: utf-8 -*-
"""
AIMAX 창업 프로그램 — 기수별 커리큘럼 타임라인 이미지 생성기 (카페 모집글용)

기수가 바뀌면 첫 오프라인 날짜 하나만 주면 2주차까지 계산해
timeline_startup.html 을 복제·치환하고 렌더까지 한다.

    python make_timeline.py --gen 5 --label 9월반 --first 2026-09-06

    1주차 = first        (일요일 · 5시간)
    2주차 = first + 7일   (일요일 · 5시간)

26-08-03 구조 변경 — 두 주가 같은 내용(바이브코딩 + 수익화 병행)이라 회차로 쪼개지 않고
"9월 6일 · 13일 (일)" 한 문자열로 박는다.

**날짜가 박히는 건 오프라인 2주뿐이다.** 온라인 운영 주기와 복습 라이브 시점은
"오프라인 다음 주부터 매일·매주·매달" · "매월 1회" 라는 주기만 쓴다. 날짜로 바꾸지 말 것.

first 가 일요일이 아니면 경고만 하고 진행한다. 오프라인을 다른 요일에 잡는 기수가
나올 수 있어서 막지는 않는다.
"""
import argparse
import re
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "timeline_startup.html"
RENDER = Path.home() / ".claude/skills/detail-page/scripts/render_detail.py"

WEEK_KO = "월화수목금토일"


def md(d: date) -> str:
    """8월 9일"""
    return f"{d.month}월 {d.day}일"


def dow(d: date) -> str:
    return WEEK_KO[d.weekday()]


def build(gen, label, first, t1, t2, out, no_render):
    second = first + timedelta(days=7)

    if first.weekday() != 6:
        print(f"  ! 1회차 {first} 가 일요일이 아니다 ({dow(first)}요일). 의도한 게 맞는지 확인할 것")

    html = SRC.read_text(encoding="utf-8")

    # 각 치환은 정확히 1건이어야 한다. 0건이면 HTML 구조가 바뀐 것 → 조용히 넘어가면
    # 옛 날짜가 그대로 박힌 이미지가 나오므로 즉시 멈춘다.
    tail = f"{second.day}일" if first.month == second.month else f"{second.month}월 {second.day}일"
    dates = f"{first.month}월 {first.day}일 · {tail} ({dow(first)})"
    subs = [
        (r'(<div class="eyebrow">)[^<]*(</div>)',
         rf'\g<1>{gen}기 · {label} 커리큘럼\g<2>'),
        # 26-08-03: 회차 분리 폐기 → 두 날짜를 한 문자열로 박는다
        (r'(<div class="when">)[^<]*?(<em>매회 12시 ~ 17시)',
         rf'\g<1>{dates}\g<2>'),
    ]
    for pat, rep in subs:
        html, n = re.subn(pat, rep, html, count=1)
        if n != 1:
            sys.exit(f"치환 실패: {pat}\n  timeline_startup.html 구조가 바뀌었다. 스크립트를 맞춰 고칠 것")

    # 시간대가 기수마다 다르면 여기서 갈아끼운다
    if t1:
        html = html.replace("매회 12시 ~ 17시 · 5시간", t1)

    stem = out or f"timeline_{gen}gi"
    tmp = HERE / f"_{stem}.html"
    tmp.write_text(html, encoding="utf-8")

    print(f"  {gen}기 · {label}")
    print(f"    오프라인  {dates}  ·  매회 5시간 (2주 10시간)")
    print(f"    라이브 · 1:1 은 날짜를 박지 않는다 (순서만 표시)")

    if no_render:
        print(f"  HTML만 생성: {tmp.name}")
        return

    png = HERE / f"{stem}.png"
    r = subprocess.run([sys.executable, str(RENDER), str(tmp), str(png)],
                       cwd=str(HERE), capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip())
    if r.returncode == 0:
        # 렌더가 끝나면 중간 HTML은 남길 이유가 없다. 남겨두면 다음 기수에서
        # 어느 게 마스터인지 헷갈린다 (마스터는 항상 timeline_startup.html)
        tmp.unlink()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--gen", required=True, help="기수 번호 (예: 5)")
    p.add_argument("--label", required=True, help="기수 라벨 (예: 9월반)")
    p.add_argument("--first", required=True, help="1회차 오프라인 날짜 YYYY-MM-DD")
    p.add_argument("--t1", help="시간대 문구 (기본 '매회 12시 ~ 17시 · 5시간')")
    p.add_argument("--t2", help=argparse.SUPPRESS)   # 회차 분리 폐기로 미사용
    p.add_argument("--out", help="출력 파일 stem (기본 timeline_<gen>gi)")
    p.add_argument("--no-render", action="store_true", help="HTML만 만들고 렌더는 건너뜀")
    a = p.parse_args()

    build(a.gen, a.label, date.fromisoformat(a.first),
          a.t1, a.t2, a.out, a.no_render)


if __name__ == "__main__":
    main()
