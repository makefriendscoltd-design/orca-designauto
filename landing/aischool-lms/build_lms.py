"""AIxSCHOOL 입학 상세 — 이상한마케팅 LMS 구조 + 확정 포스터 타입 스케일.

데이터는 운영 중인 공개 사이트 정본을 빌드마다 직접 읽는다.
  curriculum.json  M0~M12
  staff.json       6팀 24직군

표기 규칙(확정 · family-ai-school/CLAUDE.md)
  · 브랜드는 AIxSCHOOL 하나. "메이크패밀리"·"AIMAX" 쓰지 않는다
  · 가격은 월 275,000원만, 페이지에 한 번. 총액 3,300,000 은 쓰지 않는다
  · 성과 캡션에 기간·일수·날짜 범위를 적지 않는다 (개인정보)
  · 나민수 외 식별 가능한 인물 사진을 넣지 않는다 (현장은 청중·실습 테이블만)

  python build_lms.py  ->  detail_lms.html
"""
import json
import os
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parent
SRC = pathlib.Path.home() / "orca/projects/oracle-sangcheol/aixschool/public"
# 3개월 개편안이 폴더에 있으면 그걸 쓴다. 없으면 공개 사이트 정본(12개월).
_LOCAL = ROOT / "curriculum_3m.json"
CUR = json.loads((_LOCAL if _LOCAL.exists() else SRC / "curriculum.json").read_text(encoding="utf-8"))
STAFF = json.loads((SRC / "staff.json").read_text(encoding="utf-8"))

# ── 숏폼 직원 1명 환산 (2026-10-07 사용자 제공 운영 수치 + 크몽 공개 단가)
SHORT_DAY   = 20            # 하루 제작 편수 (운영 기록)
SHORT_MONTH = SHORT_DAY*30  # 월 600편
RATE_LOW    = 10000         # 크몽 숏폼 편집 STANDARD 1만원 (가장 보수적)
RATE_MID    = 50000         # DELUXE 5만원
SHORT_LOW   = SHORT_MONTH*RATE_LOW//10000     # 만원 단위
SHORT_MID   = SHORT_MONTH*RATE_MID//10000

# ── CS 직원 1명 환산 (운영 기록 + CS 아웃소싱 공개 단가)
CS_MONTH = 2300             # 월 처리 건수 (48일 3,694건 → 월 환산)
CS_DAY   = CS_MONTH // 30   # 일평균 약 77건
CS_LOW, CS_HIGH = 150, 250  # 멀티채널 풀타임 대행 월 150~250만원

# ── 밸류 스택 (2026-10-07 사용자 제공 단가) ────────────────
MONTHS_TOTAL = 12   # 전체 과정 1년
MONTHS_CORE = 3     # 집중 교육 구간
STAFF_MADE = 10      # 과정 중 직접 만드는 AI 직원 수
VALUE = [
    ("직접 만드는 AI 직원", "10명", 100, "직원 1명이 대신하는 일을 사람에게 맡겼을 때 기준", 10),
    ("주간 피드백 · 1년", "48회", 50, "1:1 컨설팅 회당 50만원 기준", 48),
    ("AI 빌드데이 오프라인", "2회", 190, "1차 졸업·최종 졸업 · 단독 판매가 190만원", 2),
    ("커뮤니티 · 월례 오프라인 강연", "12회", 10, "회당 10만원 기준", 12),
]
VALUE_SUM = sum(unit*cnt for _, _, unit, _, cnt in VALUE)
PRICE_MAN = 300     # 수강료 300만원
# 사람을 뽑았을 때 — 2026 최저임금 시급 10,320원 · 월 209시간 = 2,156,880원
HIRE_MONTH = 2156880
HIRE_TOTAL = HIRE_MONTH * MONTHS_TOTAL

# 사람으로 채우면 — 채용 공고 기준 월급 (학교 자체 조사)
WAGE = [
    ("shop-cs",                 "쇼핑몰 CS 담당자",   "월 240만 원부터",  "주문 안내 문자·메일을 하루 종일 내보내는 일"),
    ("shop-ops-manager",        "매출 기록 담당자",   "월 210만 원부터",  "주문과 매출을 모아 매일 정리해 보고하는 일"),
    ("naver-cafe-manager",      "네이버 카페 관리자", "월 240~280만 원",  "새 회원을 맞고 댓글을 관리하는 일"),
    ("youtube-channel-manager", "유튜브 채널 관리자", "월 250만 원",      "영상을 올리고 달린 댓글에 답하는 일"),
    ("content-editor",          "글감 수집 담당자",   "월 260~300만 원",  "오늘 쓸 만한 소식을 모아 글감으로 정리하는 일"),
    ("system-monitor",          "시스템 모니터링 요원", "월 230~300만 원", "멈춘 게 없는지 계속 지켜보는 일"),
]

# 증명 화면 — 공개 사이트가 쓰는 실제 캡처
PROOF = [
    ("l15-order-intake",   "01 주문 접수",   "주문이 들어오면 바로 목록에 잡힙니다"),
    ("l15-run-result",     "02 안내문 생성", "상품에 맞는 안내문이 만들어집니다"),
    ("l15-send-log",       "03 발송 기록",   "누구에게 언제 나갔는지 기록이 남습니다"),
]
PROOF2 = [
    ("perf2025-threads-revenue-01", "스레드 유입 결제", "방문 34,671 · 결제 1,681건 · 결제금액 31,688,900원"),
    ("perf2025-threads-to-blog",    "스레드 → 블로그", "글 조회 1.2만 · 댓글 431건. 댓글에서 블로그로 넘기는 화면"),
    ("perf2025-blog-published",     "자동 발행",       "AI 직원이 직접 써서 올린 네이버 블로그 글"),
    ("perf2025-insta-comments",     "자동 답글",       "인스타그램 댓글마다 답글이 하나씩 달린 화면"),
    ("revenue-dashboard-card-masked","매일 아침 리포트","자동으로 만들어지는 세일즈 리포트 카드"),
]

ROW_NOTE = {'유튜브 채널 관리자': '구독자 수·영상 수·기간은 내부 집계 그대로입니다. 영상 제목과 썸네일만 가렸습니다.', '쇼핑몰 CS 담당자': '건수·기간·채널은 내부 집계 그대로입니다. 수신자와 주문 내용만 가렸습니다.', '운영 매니저 · 비서': '건수·완료 수·담당자 수는 내부 집계 그대로입니다. 카드 제목과 이름만 가렸습니다.', '시스템 모니터링 요원': '점검 주기와 감시 대상 24개 직군은 내부 운영 설정 그대로입니다.'}

OPS = [  # (직군, 수치, 단위, 설명, 기간, [(파일, 캡션, 실제여부)])
    ("스레드 운영", "1,681", "건", "스레드에서 들어온 방문이 결제로 이어진 건수", "2025년 집계 · 결제금액 31,688,900원", [
        ("perf2025-threads-revenue-01", "방문 34,671 · 결제 1,681건 · 결제금액 31,688,900원", 1),
        ("perf2025-threads-to-blog",    "글 조회 1.2만 · 댓글 431건. 댓글에서 블로그로 넘어가는 화면", 1),
    ]),
    ("릴스 PD", "0 → 2만", "명", "인스타그램 팔로워", "2개월 · 릴스 39개", [
        ("perf2025-insta-comments", "달린 댓글마다 답글이 하나씩 달려 있는 화면", 1),
    ]),
    ("유튜브 채널 관리자", "0 → 1만", "명", "나민수 AI 채널 구독자", "3개월 · 영상 177개", [
        ("ops-yt-channel", "영상 177개를 올렸고 댓글은 5분마다 확인해 답글을 답니다", 2),
    ]),
    ("글감 수집 · 블로그 담당자", "매일", "", "사람이 쓰지 않은 네이버 블로그 글", "현재도 운영 중", [
        ("perf2025-blog-published", "AI 직원이 직접 써서 올린 글. 발행 시각이 찍혀 있습니다", 1),
    ]),
    ("매출 기록 담당자", "매일 아침", "", "전날 매출을 정리한 리포트 카드", "현재도 운영 중", [
        ("revenue-dashboard-card-masked", "자동으로 만들어지는 세일즈 리포트. 금액은 가렸습니다", 1),
    ]),
    ("쇼핑몰 CS 담당자", "3,694", "건", "주문 안내 메일·문자 발송", "2026.07.31 ~ 09.17", [
        ("ops-cs-summary", "하루 평균 75.4건. 사람이 보낸 건 0건", 2),
    ]),
    ("운영 매니저 · 비서", "441", "건", "카톡·회의에서 뽑아낸 할 일 · 298건 완료", "2026.09.06 ~ 09.17", [
        ("ops-task-board", "담당자 5명에게 배정. 그중 298건이 완료로 넘어갔습니다", 2),
    ]),
    ("시스템 모니터링 요원", "5분", "마다", "다른 AI 직원이 멈췄는지 확인하고 다시 돌립니다", "매일 운영 중", [
        ("ops-sys-monitor", "24개 직군을 한 번에 점검한 화면. 멈추면 알리고 재시작합니다", 2),
    ]),
]
CASES = [  # 수강생 사례 — 학교 개설 전 기존 교육 참여자
    ("화장품 브랜드", "3.89천만원", "실제 결제금액"),
    ("건강용품 브랜드", "116건", "배송 준비"),
    ("건강식품 브랜드", "첫 매출", "발생 확인"),
]


def sync_staff():
    out = ROOT / "assets/staff"
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for t in STAFF["teams"]:
        for s in t["staff"]:
            for ext in (".jpg", ".png"):
                c = SRC / "staff" / f"{s['file']}{ext}"
                if c.exists():
                    shutil.copy(c, out / c.name)
                    rows.append({"team": t["name"], "file": c.name,
                                 "title": s["title"], "does": s["does"]})
                    break
    return rows


SHOTS = {x["id"]: x for x in json.loads((ROOT / "shots.json").read_text(encoding="utf-8"))["slots"]}


def slot(sid, kicker="", title=""):
    """연출컷 슬롯. shots/<id>.(jpg|png|gif) 가 있으면 소재, 없으면 촬영 지시판."""
    sp = SHOTS[sid]
    for ext in (".jpg", ".png", ".gif", ".jpeg", ".webp"):
        f = ROOT / "shots" / f"{sid}{ext}"
        if f.exists():
            on = (f'<div class="on"><div class="k">{kicker}</div>'
                  f'<div class="t">{title}</div></div>') if title else ""
            return f'<div class="slot has"><img src="shots/{f.name}" alt="">{on}</div>'
    if os.environ.get("SHOW_SLOTS") == "1":   # 제작용 미리보기에서만 지시판을 띄운다
        return (f'<div class="slot empty" style="min-height:{sp["h"]}px">'
                f'<div class="tag">촬영 예정 · {sid}</div>'
                f'<div class="ttl">{sp["자리"]}</div>'
                f'<div class="dir">{sp["촬영"]}</div>'
                f'<div class="meta">{sp["type"]} · 740 × {sp["h"]}px</div></div>')
    return ""


ROWS = sync_staff()

# 팀 구성은 정본 그대로. 설명·꼬리표만 teams.json 으로 덮어쓴다(초보 혼동 방지)
_RJ = json.loads((ROOT / "teams.json").read_text(encoding="utf-8"))["roles"]
for r in ROWS:
    o = _RJ.get(r["file"].rsplit(".", 1)[0])
    if o:
        r["does"] = o["does"]
        r["tag"] = o["tag"]
TEAMS = [t["name"] for t in STAFF["teams"]]
GIFSEQ = []
# 주차별 상세 — 공개 정본엔 제목만 있어 여기서 덧댄다
_LD = json.loads((ROOT / "lesson_detail.json").read_text(encoding="utf-8"))["detail"]
for _m in CUR["months"]:
    _d = _LD.get(str(_m["month"]), [])
    for _i, _l in enumerate(_m.get("lessons") or []):
        if _i < len(_d):
            _l.setdefault("do", _d[_i].get("do", ""))
            _l.setdefault("out", _d[_i].get("out", ""))

MONTH_GIF = {1: "g_task", 3: "g_keep", 5: "g_morning", 7: "g_writing",
             10: "g_ship", 12: "g_grad"}
TOTAL = sum(len(m.get("lessons") or []) for m in CUR["months"])


def faces(team, idx=0):
    """팀 소개 영상 + 직군 4명 타일. 영상은 마커로만 굽는다(실제 GIF 는 업로더가 끼운다)."""
    rs = [r for r in ROWS if r["team"] == team]
    cards = "".join(
        f'<div class="tile2"><img src="assets/staff/{r["file"]}" alt="{r["title"]}">'
        f'<div class="ov"><b>{r["title"]}</b><span>{r["does"]}</span></div>'
        f'<div class="rtag">{r.get("tag","")}</div></div>' for r in rs)
    vid = gifband(f"g_t{idx + 1}")
    return (f'<div class="tmlb"><em>//</em>{team}</div>{vid}'
            f'<div class="tiles">{cards}</div>')


def wagepanels():
    out = []
    for f, title, pay, what in WAGE:
        img = next((r["file"] for r in ROWS if r["file"].startswith(f + ".")), None)
        if not img:
            continue
        out.append(
            f'<section class="wg"><div class="wgin">'
            f'<img src="assets/staff/{img}" alt="">'
            f'<div class="wgt">{title}</div>'
            f'<div class="wgw">{what}</div>'
            f'<div class="wgp"><span>사람으로 채우면</span><b>{pay}</b></div>'
            f'<div class="wga">지금 이 자리는 AI 직원이 일합니다</div>'
            f'</div></section>')
    return "".join(out)


def proofshots(rows, lead=""):
    cards = "".join(
        f'<figure class="ps"><img src="assets/shots/{f}.webp" alt="">'
        f'<figcaption><b>{t}</b><span>{c}</span></figcaption></figure>'
        for f, t, c in rows if (ROOT / "assets/shots" / f"{f}.webp").exists())
    return f'<div class="psw">{lead}{cards}</div>' if cards else ""


def opsblocks():
    out = []
    for who, v, u, what, when, shots in OPS:
        imgs = ""
        for f, c, real in shots:
            if not (ROOT / "assets/shots" / f"{f}.webp").exists():
                continue
            bg = {1: '<span class="bg ok">실제 화면</span>',
                  2: '<span class="bg sum">집계 화면</span>',
                  }.get(real, '<span class="bg re">재현 화면</span>')
            imgs += (f'<figure class="ev2"><img src="assets/shots/{f}.webp" alt="">'
                     f'<figcaption>{bg}{c}</figcaption></figure>')
        note = ROW_NOTE.get(who, "")
        if not shots:
            note = ("업무 카드에는 직원 이름과 거래처가 그대로 들어 있어 "
                    "화면을 공개하지 않습니다. 건수와 집계 기간만 밝힙니다.")
        note = f'<div class="noev">{note}</div>' if note else ""
        body = (f'<div class="evs">{imgs}</div>' if imgs else "")
        out.append(
            f'<div class="rec2"><div class="rh"><div><div class="who">{who}</div>'
            f'<div class="what">{what}</div><div class="when">{when}</div></div>'
            f'<div class="v">{v}<small>{u}</small></div></div>{note}{body}</div>')
    return "".join(out)


def cases():
    return "".join(
        f'<div class="case"><div class="b">{b}</div><div class="v">{v}</div><div class="u">{u}</div></div>'
        for b, v, u in CASES)


def gifband(name, kicker="", title=""):
    """연출영상 GIF 띠. 파일이 없으면 아무것도 내보내지 않는다."""
    f = ROOT / "gifs" / f"{name}.gif"
    if not f.exists():
        return ""
    GIFSEQ.append(name)
    lead = ""
    if title:
        lead = (f'<section class="p t"><div class="numlb">{kicker}</div>'
                f'<div class="gap1"></div><div class="md">{title}</div></section>')
    return lead + '<div class="gifmark"></div>'


def orgchart():
    cols = "".join(
        f'<div class="col"><div class="drop"></div>'
        f'<div class="cap4">{t.replace(" 자동화팀","").replace("자동화팀","")}</div>'
        f'<div class="mem">' + "".join(
            f'<figure><img src="assets/staff/{r["file"]}" alt="">'
            f'<figcaption>{r["title"]}</figcaption></figure>'
            for r in ROWS if r["team"] == t) + '</div></div>'
        for t in TEAMS)
    return f"""<section class="org">
  <div class="lb">졸업할 때 손에 남는 것</div>
  <h3>사장 한 명 밑에<br><em>스물네 명이</em> 붙습니다.</h3>
  <div class="boss"><div class="ph"><img src="assets/char/namin_profile.jpg" alt=""></div>
    <b>나</b><span>사장</span></div>
  <div class="trunk"></div><div class="rail"></div>
  <div class="cols">{cols}</div>
  <div class="foot">사람은 그대로 한 명입니다.<br><b>늘어난 건 일하는 손이고, 줄어든 건 내 시간입니다.</b></div>
</section>"""


def valuestack():
    rows = "".join(
        f'<div class="vs"><div class="l"><b>{name}</b><span>{why}</span></div>'
        f'<div class="r"><em>{qty}</em>{unit*cnt:,}만원</div></div>'
        for name, qty, unit, why, cnt in VALUE)
    return rows


def curriculum():
    out = []
    for m in CUR["months"]:
        les = m.get("lessons") or []
        tagmap = {"gate": "수료 확인", "feedback": "주간 피드백", "builday": "오프라인"}
        rows = "".join(
            f'<div class="wk"><div class="wt">{x["title"]}'
            + (f'<span class="kk">{tagmap[x["kind"]]}</span>' if x.get("kind") in tagmap else "")
            + f'</div><div class="wd">{x.get("do","")}</div>'
            + (f'<div class="wo">제출 · {x["out"]}</div>' if x.get("out") and x["out"] != "—" else "")
            + '</div>' for x in les)
        g = ""
        gid = m.get("gif") or MONTH_GIF.get(m["month"])
        if gid and (ROOT / "gifs" / f"{gid}.gif").exists():
            GIFSEQ.append(gid)
            g = '<div class="gifmark"></div>'
        out.append(f'<div class="mon"><div class="mh"><span class="no">{m["month"]:02d}</span>'
                   f'<span class="ti">{m["title"]}</span></div>'
                   f'<div class="go">{m["goal"]}</div>{g}<div class="ls">{rows}</div></div>')
    return "".join(out)


cover = "".join(f'<img src="assets/staff/{r["file"]}" alt="">' for r in ROWS[:3])

HTML = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=740">
<title>AIxSCHOOL 입학 신청</title>
<link rel="stylesheet" href="lmsposter.css">
</head>
<body>

{slot("s01_hook","AIxSCHOOL","직원 뽑기 전에,<br>AI 직원부터.")}

<section class="stack" id="intro">
  <div class="big">0</div>
  <div class="fore">
    <div class="lb">먼저 말씀드립니다</div>
    <div class="hd">저희도 사람을<br>더 뽑아봤습니다.</div>
    <div class="bd">그런데 매달 빠져나간 건 월급이 아니라 제 시간이었습니다.
      가르칠 시간, 고칠 시간, 그만두면 다시 뽑을 시간.</div>
  </div>
</section>

{slot("s02_hire")}

{gifband("g_wage","사람 vs AI 직원","같은 일을<br>누가 더 싸게 하나.")}

<section class="p t">
  <div class="cap2">이 자리를 사람으로 채우면</div>
  <div class="gap1"></div>
  <div class="md">한 명씩<br><span class="bl">얼마인지 보겠습니다.</span></div>
</section>
{wagepanels()}
<section class="p t">
  <div class="cap">월급은 채용 공고에 적힌 금액 기준입니다.<br>
    여섯 자리를 사람으로 채우면 월 1,430만원부터 시작합니다.</div>
</section>

<section class="p navy t">
  <div class="md">그래서 사람 대신<br><span class="bl">직원을 만들었습니다.</span></div>
  <div class="gap2"></div>
  <div class="cap">여섯 개 팀에 스물네 명.<br>인건비는 0원입니다. (네, 전부 AI입니다)</div>
</section>

{slot("s03_staff","AI STAFF","이 직원들이<br>실제로 일하는 화면.")}

<section class="p pb0" id="staff">
  <div class="numlb">AI STAFF</div>
  <div class="gap1"></div>
  <div class="md">이 중에 누구부터<br><span class="bl">뽑으시겠습니까.</span></div>
  <div class="gap1"></div>
  <div class="cap">첫 달은 기초를 같이 밟고,<br>그다음부터 필요한 직원을 골라서 만듭니다.</div>
  {''.join(faces(t, i) for i, t in enumerate(TEAMS))}
  <div class="gap2"></div>
  <div class="cap" style="padding-bottom:110px">직원 사진은 AI로 만든 이미지입니다.</div>
</section>

{gifband("g_band","AI 직원 양성학교","지금 저희 회사에서<br>매일 출근합니다.")}

{gifband("g_grid")}

{orgchart()}

<section class="p navy t">
  <div class="md">가르치기 전에,<br><span class="bl">저희가 먼저 썼습니다.</span></div>
  <div class="gap2"></div>
  <div class="cap">파는 사람이 안 쓰는 걸 가르치지는 않겠습니다.</div>
</section>

<section class="p t">
  <div class="numlb">우리 회사가 돌린 기록</div>
  <div class="gap1"></div>
  <div class="md">숫자 옆에<br><span class="bl">그 화면을 같이 둡니다.</span></div>
  <div class="gap1"></div>
  <div class="bd">숫자만 적으면 못 믿으실 겁니다. 건수마다 실제로 돌아간 화면을 붙였습니다.</div>
  <div class="recs">{opsblocks()}</div>
  <div class="gap2"></div>
  <div class="cap">전부 저희 회사 내부 운영 화면입니다.<br>수강생의 동일한 결과를 보장하지 않습니다.</div>
</section>

<section class="p t">
  <div class="numlb">도입처 기록 · 우리 회사 밖</div>
  <div class="gap1"></div>
  <div class="md">같은 일을<br><span class="bl">15시간에서 5분으로.</span></div>
  <div class="gap1"></div>
  <div class="bd">병의원에 같은 방식을 적용한 곳이 측정한 기록입니다. 예약 안내·차트 정리·매출 관리를 묶어서 쟀습니다.</div>
  <div class="recs"><div class="rec2"><div class="evs">
    <figure class="ev2"><img src="assets/shots/case-clinic-time.webp" alt="">
    <figcaption><span class="bg sum">집계 화면 · 도입처 측정</span>도입 전 15시간 → 도입 후 5분. 측정 기간 1개월</figcaption></figure>
  </div></div></div>
  <div class="gap2"></div>
  <div class="cap">도입처가 직접 측정한 수치입니다.<br>저희 내부 기록이 아니며 동일한 결과를 보장하지 않습니다.</div>
</section>

{slot("s04_cs")}
{slot("s05_card")}

{gifband("g_countup")}

{slot("s06_buildday","AI 빌드데이","만든 직원을<br>직접 보여줍니다.")}

<section class="p t">
  <div class="md">배운 분들은<br><span class="bl">자기 사업에서<br>이렇게 썼습니다.</span></div>
  <div class="cases">{cases()}</div>
  <div class="gap2"></div>
  <div class="cap">학교 개설 전 기존 교육 참여자 사례이며 운영진 성과와 별개입니다.<br>
    수강 전·후 비교 자료가 없어 확인된 결과만 표시했고, 같은 결과를 보장하지 않습니다.</div>
</section>

{slot("s07_before")}

<section class="p navy">
  <div class="numlb">12개월 · 13개 과정</div>
  <div class="gap1"></div>
  <div class="num">{TOTAL}<small>강</small></div>
  <div class="rule"></div>
  <div class="md">1년 뒤 남는 건 수료증이 아니라<br><span class="bl">내 사무실에서 일하는 팀입니다.</span></div>
</section>

{slot("s09_month","CURRICULUM","매달 직원이<br>한 명씩 늘어납니다.")}

<section class="w" id="curriculum">
  <div class="eb">CURRICULUM</div>
  <h2>1년 동안<br><em>이렇게 갑니다.</em></h2>
  <div class="lead">매달 직원을 한 명씩 만들어 그달 안에 업무에 붙입니다.<br>
    6개월 차에 1차 졸업, 12개월 차에 조직도를 발표하고 최종 졸업합니다.</div>
  {curriculum()}
</section>

{slot("s08_master","INSTRUCTOR","가르치는 사람이<br>먼저 쓰고 있습니다.")}

<section class="w" style="background:#f9fafb" id="master">
  <div class="eb">INSTRUCTOR</div>
  <h2>가르치는 사람이<br><em>먼저 쓰고 있습니다.</em></h2>
  <div class="tutor">
    <img src="assets/char/namin_profile.jpg" alt="나민수 대표">
    <div>
      <div class="nm">나민수</div>
      <div class="ro">AIxSCHOOL 교장</div>
      <ul>
        <li>사내 운영에 AI 직원을 직접 붙여 쇼핑몰 CS·업무 분배를 돌리고 있습니다</li>
        <li>우리가 쓰는 AI 직원을 그대로 만드는 법을 가르칩니다</li>
        <li>매월 만든 직원을 과제로 제출하고 검토·수정·승인을 거칩니다</li>
        <li>졸업은 영상 시청이 아니라 실제로 일하는 화면으로 판정합니다</li>
      </ul>
    </div>
  </div>
</section>

<section class="w" style="background:#f9fafb">
  <div class="eb">PROCESS</div>
  <h2>입학은<br><em>세 단계입니다.</em></h2>
  <div class="steps3">
    <div class="st"><b>01</b><div><h3>무료 입학설명회</h3>
      <p>무엇을 만드는지 먼저 봅니다. 교육과정과 운영 방식, 수강료를 확인합니다.</p></div></div>
    <div class="st"><b>02</b><div><h3>입학 신청</h3>
      <p>신청 후 결제하면 확정됩니다.</p></div></div>
    <div class="st"><b>03</b><div><h3>학습 시작</h3>
      <p>입학 주간에 설치를 끝내고 첫 수업으로 들어갑니다.</p></div></div>
  </div>
</section>

{gifband("g_short","숏폼 편집 직원","하루 20편이<br>이렇게 나옵니다.")}

<section class="stack">
  <div class="big">600</div>
  <div class="fore">
    <div class="lb">직원 한 명 값, 계산해봤습니다</div>
    <div class="hd">숏폼 담당 한 명이<br>하루 {SHORT_DAY}편을 만듭니다.</div>
    <div class="calc">
      <div class="cl"><span>한 달 제작량</span><b>{SHORT_MONTH:,}편</b></div>
      <div class="cl"><span>외주 최저 단가 (1편)</span><b>{RATE_LOW:,}원</b></div>
      <div class="cl eq"><span>사람에게 맡기면</span><b>월 {SHORT_LOW:,}만원</b></div>
    </div>
    <div class="bd">가장 싼 단가로 계산한 금액입니다. 조금만 손이 더 가는 편집(5만원대)으로 잡으면
      월 {SHORT_MID:,}만원이 됩니다. 저희가 "직원 한 명당 100만원"이라고 적은 건
      그래서 보수적으로 잡은 숫자입니다.</div>
    <div class="src">단가 출처 — 크몽 숏폼 편집 공개 패키지(STANDARD 1만원 / DELUXE 5만원).
      제작량은 학교 운영사 내부 기록이며 수강생의 동일한 결과를 보장하지 않습니다.</div>
  </div>
</section>

{gifband("g_orders","주문이 들어오면","사람이 안 봐도<br>안내가 나갑니다.")}

<section class="stack">
  <div class="big">2,300</div>
  <div class="fore">
    <div class="lb">두 번째 계산</div>
    <div class="hd">CS 담당 한 명이<br>월 {CS_MONTH:,}건을 처리합니다.</div>
    <div class="calc">
      <div class="cl"><span>한 달 처리량</span><b>{CS_MONTH:,}건</b></div>
      <div class="cl"><span>일평균</span><b>약 {CS_DAY}건</b></div>
      <div class="cl eq"><span>사람에게 맡기면</span><b>월 {CS_LOW:,}~{CS_HIGH:,}만원</b></div>
    </div>
    <div class="bd">전화·채팅·메일을 평일과 주말까지 받는 대행 기준입니다.
      업계에서는 일평균 100건이 넘으면 2인 교대를 붙입니다. 저희는 그걸 한 명이 받습니다.
      사람이 아니라서 주말에도 쉬지 않습니다.</div>
    <div class="src">단가 출처 — CS 상담 아웃소싱 공개 견적(멀티채널 전문형 월 150만~250만원).
      처리량은 학교 운영사 내부 기록이며 수강생의 동일한 결과를 보장하지 않습니다.</div>
  </div>
</section>

<section class="stack">
  <div class="big">{VALUE_SUM:,}</div>
  <div class="fore">
    <div class="lb">받아가는 것</div>
    <div class="hd">따로 사면<br>{VALUE_SUM:,}만원입니다.</div>
    <div class="vstack">{valuestack()}
      <div class="vs total"><div class="l"><b>합계</b></div><div class="r">{VALUE_SUM:,}만원</div></div>
      <div class="vs now"><div class="l"><b>수강료</b></div><div class="r">{PRICE_MAN}만원</div></div>
    </div>
    <div class="bd" style="margin-top:30px">환산 단가는 각 항목을 따로 구매했을 때의 기준가입니다.</div>
  </div>
</section>

<section class="p t">
  <div class="cap2">사람을 한 명 뽑으면</div>
  <div class="gap1"></div>
  <div class="lg">1년에<br><span class="bl">{HIRE_TOTAL//10000:,}만원입니다.</span></div>
  <div class="gap2"></div>
  <div class="cap">2026년 최저임금 시급 10,320원 · 월 209시간 환산 {HIRE_MONTH:,}원 기준.<br>
    4대보험·퇴직금·교육 시간은 빼고 계산한 금액입니다.<br>
    그리고 그 사람은 1년 뒤 그만둘 수 있습니다.</div>
</section>

{slot("s10_value","VALUE","직원 10명을 만들고<br>1년 뒤에도<br>계속 일합니다.")}

{slot("s12_cta","AIxSCHOOL","1년 뒤,<br>내 사무실에서<br>일하는 팀.")}

{gifband("g_talking","AI 빌드데이","코드 대신 말로<br>가르쳐서 키웁니다.")}

<section class="w">
  <div class="eb">FAQ</div>
  <h2>입학 전,<br><em>궁금한 점.</em></h2>
  <div class="qa"><div class="q">코딩이나 AI를 몰라도 시작할 수 있나요?</div>
    <div class="a">네. 코드는 직접 쓰지 않습니다. 말로 설명해 만드는 바이브코딩부터 배웁니다.</div></div>
  <div class="qa"><div class="q">일주일에 어느 정도 공부해야 하나요?</div>
    <div class="a">강의 한 편이 15~20분입니다. 따라 한 뒤 결과를 제출합니다.</div></div>
  <div class="qa"><div class="q">어떤 준비물이 필요한가요?</div>
    <div class="a">맥이나 윈도우 컴퓨터 한 대면 됩니다. 입학 주간에 설치 강의가 있습니다.</div></div>
  <div class="qa"><div class="q">수강료 외에 도구 비용이 드나요?</div>
    <div class="a">AI 도구 구독료 외에 추가 비용은 없습니다.</div></div>
  <div class="qa"><div class="q">빌드데이는 어떻게 참여하나요?</div>
    <div class="a">빌드데이는 수강생이 모여 자기가 만든 AI 직원을 보여주는 오프라인 자리입니다. 월 1회 주말, 서울대입구에서 엽니다. 전원 참여할 수 있습니다.</div></div>
  <div class="qa"><div class="q">중간에 수강을 종료할 수 있나요?</div>
    <div class="a">월 결제라 원하는 달에 멈출 수 있습니다. 만든 AI 직원은 계속 내 것입니다.</div></div>
</section>

<section class="price" id="apply">
  <div class="reprise">[AIxSCHOOL] AI 학교 입학 신청하기</div>
  <div class="opt">
    <div class="nm">AI 학교 정규과정 · 1년</div>
    <div class="v">월 275,000<small>원</small></div>
    <div class="nt">1년 과정 · 12개월 할부 · 정원 30명<br>할부 수수료와 조건은 결제 수단에 따라 다릅니다.</div>
  </div>
  <div class="cta">입학 신청하기 <i></i></div>
  <div class="fine">입학설명회에서 어떤 AI 직원이 필요한지 먼저 확인하실 수 있습니다.</div>

  <div class="notice">
    <b>신청 전에 확인해 주세요</b>
    <ul>
      <li>운영 수치는 학교 운영사 내부 기록이며 수강생의 동일한 결과를 보장하지 않습니다.</li>
      <li>수강생 사례는 학교 개설 전 기존 교육 참여자의 결과이며 운영진 성과와 별개입니다.</li>
      <li>수강 전·후 비교 자료가 제공되지 않아 확인된 결과만 표시했습니다.</li>
      <li>졸업은 영상 시청만으로 인정되지 않습니다. 실제로 일하는 직원 화면 확인이 필요합니다.</li>
      <li>AI 직원 인물 이미지는 AI로 만든 것이며 실제 인물이 아닙니다.</li>
    </ul>
  </div>
</section>

</body>
</html>
"""

(ROOT / "_gifseq.json").write_text(json.dumps(GIFSEQ, ensure_ascii=False), encoding="utf-8")
out = ROOT / "detail_lms.html"
out.write_text(HTML, encoding="utf-8")
print(f"{out.name} {len(HTML):,}자 · 직원 {len(ROWS)} · {len(CUR['months'])}개월 {TOTAL}강")
