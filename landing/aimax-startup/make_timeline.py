# -*- coding: utf-8 -*-
"""
AIMAX 창업 프로그램 — 기수별 커리큘럼 타임라인 이미지 생성기 (카페 모집글용)

기수가 바뀌면 첫 오프라인 날짜 하나만 주면 2회차까지 계산해
timeline_startup.html 을 복제·치환하고 렌더까지 한다.

    python make_timeline.py --gen 5 --label 9월반 --first 2026-09-06

    1회차 = first        (일요일 · 6시간)
    2회차 = first + 7일   (일요일 · 4시간)

**날짜가 박히는 건 오프라인 2회뿐이다.** 온라인 라이브 요일·시간과 1:1 컨설팅 시점은
기수마다 정해지므로 이미지에 안 넣는다 — 타임라인은 "2회차 다음 주부터 주 1회",
"보통 5주차 전후" 라는 순서만 보여준다. 이 부분을 날짜로 바꾸지 말 것.

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
    subs = [
        (r'(<div class="eyebrow">)[^<]*(</div>)',
         rf'\g<1>{gen}기 · {label} 커리큘럼\g<2>'),
        (r'(<div class="when">)[^<]*?(<em>12시 ~ 18시)',
         rf'\g<1>{md(first)} ({dow(first)})\g<2>'),
        (r'(<div class="when">)[^<]*?(<em>12시 ~ 16시)',
         rf'\g<1>{md(second)} ({dow(second)})\g<2>'),
    ]
    for pat, rep in subs:
        html, n = re.subn(pat, rep, html, count=1)
        if n != 1:
            sys.exit(f"치환 실패: {pat}\n  timeline_startup.html 구조가 바뀌었다. 스크립트를 맞춰 고칠 것")

    # 시간대가 기수마다 다르면 여기서 갈아끼운다
    if t1:
        html = html.replace("12시 ~ 18시 · 6시간", t1)
    if t2:
        html = html.replace("12시 ~ 16시 · 4시간", t2)

    stem = out or f"timeline_{gen}gi"
    tmp = HERE / f"_{stem}.html"
    tmp.write_text(html, encoding="utf-8")

    print(f"  {gen}기 · {label}")
    print(f"    1회차  {first}  ({dow(first)})  6시간")
    print(f"    2회차  {second}  ({dow(second)})  4시간")
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
    p.add_argument("--t1", help="1회차 시간 문구 (기본 '12시 ~ 18시 · 6시간')")
    p.add_argument("--t2", help="2회차 시간 문구 (기본 '12시 ~ 16시 · 4시간')")
    p.add_argument("--out", help="출력 파일 stem (기본 timeline_<gen>gi)")
    p.add_argument("--no-render", action="store_true", help="HTML만 만들고 렌더는 건너뜀")
    a = p.parse_args()

    build(a.gen, a.label, date.fromisoformat(a.first),
          a.t1, a.t2, a.out, a.no_render)


if __name__ == "__main__":
    main()
