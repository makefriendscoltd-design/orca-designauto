# -*- coding: utf-8 -*-
"""
AIMAX 창업 프로그램 — 카페 모집글 첨부용 카드 4장 생성기 (1080×1350 · 4:5)

    python make_cards.py --gen 5 --label 9월반 --first 2026-09-06
    → cards_5gi_1.png  전체 흐름
      cards_5gi_2.png  오프라인 2주 (바이브코딩 · 수익화 세팅)
      cards_5gi_3.png  온라인 5개월 운영 (매일 · 매주 · 매달)
      cards_5gi_4.png  매월 복습 라이브 커리큘럼 (다크)

롱이미지(timeline_startup.html)는 상세페이지 포맷이라 카페 본문에서 모바일 스크롤이
길다. 카페에는 이 카드 4장을 글 흐름 중간에 나눠 넣는다.

**날짜가 박히는 건 오프라인 2주뿐이다.** 온라인 운영 주기·복습 라이브 시점은
"이후 5개월" · "매월 1회" 라는 주기만 쓴다 — 날짜로 바꾸지 말 것.

마스터(cards_startup.html)는 5기(9월반) 기준이고, 아래 BASE_* 문자열을 그대로
찾아 바꾼다. 마스터의 날짜 표기를 고치면 BASE_* 도 같이 고쳐야 한다.
"""
import argparse
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

# --- venv 고정: 스킬 전용 venv 가 아니면 그쪽으로 재실행한다 ---
# (시스템 python3 에도 PIL 이 깔려 있어 "PIL 있나"로 판정하면 numpy/fitz 에서 뒤늦게 터진다)
import os as _os, sys as _sys
_vdir = _os.path.join(_os.path.expanduser("~"), ".claude", "skills", ".venv")
_vpy = _os.path.join(_vdir, "Scripts" if _os.name == "nt" else "bin",
                     "python.exe" if _os.name == "nt" else "python")
if _os.path.exists(_vpy) and _os.path.realpath(_sys.prefix) != _os.path.realpath(_vdir):
    _os.execv(_vpy, [_vpy, _os.path.abspath(__file__)] + _sys.argv[1:])
# --- shim 끝 ---

from PIL import Image

HERE = Path(__file__).resolve().parent
SRC = HERE / "cards_startup.html"
RENDER = Path.home() / ".claude/skills/detail-page/scripts/render_detail.py"

CARD_W, CARD_H, N_CARDS = 1080, 1350, 4
WEEK_KO = "월화수목금토일"

# 마스터에 박혀 있는 4기 값. 몇 건 나와야 하는지까지 못박아 둔다 —
# 건수가 다르면 마스터 구조가 바뀐 것이고, 조용히 넘어가면 옛 날짜가 섞인 카드가 나간다
BASE_LABEL = ("5기 · 9월반", 1)
# 26-08-03 구조 변경: 회차별 분리를 폐기하고 두 날짜를 한 문자열로 묶었다.
# 카드1 flow 와 카드2 dayhd 두 곳에 같은 문자열이 들어간다.
BASE_DATES = ("9월 6일 · 13일 (일)", 2)

SUBTITLES = ["전체 흐름", "오프라인 2주", "온라인 5개월 운영", "복습 라이브 커리큘럼"]


def two_dates(a: date, b: date) -> str:
    """9월 6일 · 13일 (일)  — 달이 넘어가면 9월 27일 · 10월 4일 (일)"""
    tail = f"{b.day}일" if a.month == b.month else f"{b.month}월 {b.day}일"
    return f"{a.month}월 {a.day}일 · {tail} ({WEEK_KO[a.weekday()]})"


def swap(html: str, base, new: str) -> str:
    old, want = base
    got = html.count(old)
    if got != want:
        sys.exit(f"치환 실패: '{old}' 가 {want}건이어야 하는데 {got}건이다.\n"
                 f"  cards_startup.html 이 바뀌었다. make_cards.py 의 BASE_* 를 맞춰 고칠 것")
    return html.replace(old, new)


def build(gen, label, first, out, keep_raw):
    second = first + timedelta(days=7)
    if first.weekday() != 6:
        print(f"  ! 1회차 {first} 가 일요일이 아니다 ({WEEK_KO[first.weekday()]}요일). 맞는지 확인할 것")

    html = SRC.read_text(encoding="utf-8")
    html = swap(html, BASE_LABEL, f"{gen}기 · {label}")
    html = swap(html, BASE_DATES, two_dates(first, second))

    stem = out or f"cards_{gen}gi"
    tmp_html = HERE / f"_{stem}.html"
    raw = HERE / f"_{stem}_raw.png"
    tmp_html.write_text(html, encoding="utf-8")

    r = subprocess.run([sys.executable, str(RENDER), str(tmp_html), str(raw)],
                       cwd=str(HERE), capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(r.stderr.strip() or r.stdout.strip())

    im = Image.open(raw)
    if im.size != (CARD_W, CARD_H * N_CARDS):
        # 높이가 다르면 카드 하나가 넘쳤거나 줄어든 것. 그대로 자르면 경계가 어긋난다
        sys.exit(f"높이가 {im.size[1]} 이다 (기대 {CARD_H * N_CARDS}).\n"
                 f"  카드 내용이 1350px 를 넘쳤다. cards_startup.html 여백을 조일 것")

    print(f"  {gen}기 · {label}   오프라인 {two_dates(first, second)} · 매회 5시간")
    for i in range(N_CARDS):
        png = HERE / f"{stem}_{i + 1}.png"
        im.crop((0, i * CARD_H, CARD_W, (i + 1) * CARD_H)).save(png)
        print(f"    {png.name}  {CARD_W}×{CARD_H}  {SUBTITLES[i]}")

    im.close()
    if not keep_raw:
        tmp_html.unlink()
        raw.unlink()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--gen", required=True, help="기수 번호 (예: 5)")
    p.add_argument("--label", required=True, help="기수 라벨 (예: 9월반)")
    p.add_argument("--first", required=True, help="1회차 오프라인 날짜 YYYY-MM-DD")
    p.add_argument("--out", help="출력 파일 stem (기본 cards_<gen>gi)")
    p.add_argument("--keep-raw", action="store_true", help="중간 HTML·이어붙인 원본 PNG 를 남김")
    a = p.parse_args()
    build(a.gen, a.label, date.fromisoformat(a.first), a.out, a.keep_raw)


if __name__ == "__main__":
    main()
