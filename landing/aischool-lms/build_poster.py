"""AIxSCHOOL 입학 상세 — 다크 포스터 연작.

데이터는 **운영 중인 공개 사이트 정본을 직접 읽는다**(2026-10-07 기준).
  curriculum.json : M0~M12 13개월 과정
  staff.json      : 6팀 24직군
  index.html      : 운영 실적·수강생 사례 수치

  python build_poster.py  ->  detail_aischool_poster.html
"""
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parent
SRC = pathlib.Path.home() / "orca/projects/oracle-sangcheol/aixschool/public"

CUR = json.loads((SRC / "curriculum.json").read_text(encoding="utf-8"))
STAFF = json.loads((SRC / "staff.json").read_text(encoding="utf-8"))

# ── 공개 사이트에서 확인한 수치 (index.html) ───────────────────
OPS = [  # 운영진 성과 — 메이크패밀리 내부 운영 기록
    ("쇼핑몰 CS 담당자", "주문 안내 메일·문자 발송", "3,694", "건", "2026.07.31~09.17"),
    ("운영 매니저·비서", "업무 카드 배정 · 298건 완료", "441", "건", "담당자 5명에게 배정"),
    ("스레드 운영", "유입에서 발생한 결제", "1,681", "건", "방문 34,671 · 31,688,900원"),
]
CASES = [  # 수강생 사례 — 학교 개설 전 기존 교육 참여자
    ("화장품 브랜드", "Threads 프로필 조회 931,840", "3.89천만원", "실제 결제금액"),
    ("건강용품 브랜드", "조회 1,116,985", "116건", "최근 1주일 배송준비"),
    ("건강식품 브랜드", "조회 736,878", "첫 매출", "발생 확인"),
]


def copy_staff():
    """정본 staff 이미지를 작업 폴더로 동기화한다."""
    out = ROOT / "assets/staff"
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for t in STAFF["teams"]:
        for s in t["staff"]:
            for cand in (SRC / "staff" / f"{s['file']}.jpg",
                         SRC / "staff" / f"{s['file']}.png"):
                if cand.exists():
                    shutil.copy(cand, out / cand.name)
                    rows.append({"team": t["name"], "file": cand.name,
                                 "title": s["title"], "does": s["does"]})
                    break
    return rows


ROWS = copy_staff()
TEAMS = [t["name"] for t in STAFF["teams"]]


def faces(team):
    rs = [r for r in ROWS if r["team"] == team]
    cards = "".join(
        f'<div class="fc"><img src="assets/staff/{r["file"]}" alt="{r["title"]}">'
        f'<div class="ov"><b>{r["title"]}</b><span>{r["does"]}</span></div></div>'
        for r in rs)
    return f'<div class="team"><div class="tn">{team}</div><div class="faces4">{cards}</div></div>'


def opscards():
    return "".join(
        f'<div class="oc"><div class="who">{who}</div>'
        f'<div class="v">{v}<small>{u}</small></div>'
        f'<div class="what">{what}</div><div class="when">{when}</div></div>'
        for who, what, v, u, when in OPS)


def casecards():
    return "".join(
        f'<div class="cc"><div class="br">{br}</div>'
        f'<div class="v">{v}</div><div class="u">{u}</div>'
        f'<div class="sub">{sub}</div></div>'
        for br, sub, v, u in CASES)


def curriculum():
    out = []
    for m in CUR["months"]:
        les = m.get("lessons") or []
        rows = "".join(
            f'<div class="rw"><div class="l"><span class="ix">{i:02d}</span>'
            f'<span class="nm">{x["title"]}</span></div>'
            f'<span class="k">{"빌드데이" if "빌드데이" in x["title"] else "강의"}</span></div>'
            for i, x in enumerate(les, 1))
        out.append(
            f'<div class="acc"><div class="hd"><div class="t">{m["label"]} · {m["title"]}'
            f'<small>{m["goal"]}</small></div><div class="n">{len(les)}강</div></div>{rows}</div>')
    return "".join(out)


cover_faces = "".join(f'<img src="assets/staff/{r["file"]}" alt="">' for r in ROWS[:3])
TOTAL = sum(len(m.get("lessons") or []) for m in CUR["months"])

HTML = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=740">
<title>AIxSCHOOL 입학 신청 — AI 직원 양성 12개월 과정</title>
<link rel="stylesheet" href="poster.css">
</head>
<body>

<div class="topbar">
  <div class="lg"><i></i>AIxSCHOOL</div>
  <div class="ic"><s></s><div><u></u></div></div>
</div>
<div class="back">← 학교 소개로 돌아가기</div>

<div class="cover">
  <div class="faces">{cover_faces}</div>
  <div class="play"></div>
  <div class="in">
    <span class="yr">2027</span>
    <h2>직원 뽑기 전에,<br>AI 직원부터.</h2>
  </div>
</div>

<div class="head">
  <h1>[AIxSCHOOL] AI 학교 입학 신청하기</h1>
  <div class="rate"><b>12개월</b> 정규과정 <em>|</em> 6팀 24직군 <em>|</em> 나민수 대표 직강</div>
</div>
<div class="tagrow"><span class="n">1기</span><span class="h">모집중</span><span class="b">정원 30명</span></div>

<div class="topproof">
  <div class="ttl">가르치기 전에, 우리 회사가 먼저 씁니다</div>
  <div class="pf"><div class="n">주문 안내 3,694건<em>쇼핑몰 CS 담당 · 2026.07.31~09.17</em></div>
    <p>주문이 들어오면 안내 문자와 메일을 내보내는 일을 AI 직원이 처리한 건수입니다.</p></div>
  <div class="pf"><div class="n">업무 카드 441건<em>운영 매니저·비서 · 298건 완료</em></div>
    <p>카톡·텔레그램·회의에서 할 일을 뽑아 담당자 5명에게 배정한 건수입니다.</p></div>
  <div class="pf"><div class="n">AI 직원 24직군<em>6개 자동화팀</em></div>
    <p>영상·글쓰기·SNS·디자인·고객주문·업무관리 여섯 팀을 실제 운영에 붙여 쓰고 있습니다.</p></div>
</div>

<div class="tabs">
  <a href="#intro" class="on">소개</a>
  <a href="#staff">AI 직원</a>
  <a href="#curriculum">전체목차</a>
  <a href="#master">교장소개</a>
  <a href="#apply">신청</a>
</div>

<section class="p" id="intro">
  <div class="sm">사람을 더 뽑아서 해결하려 했습니다.</div>
  <div class="dec">그런데 매달 나가는 건<br><span class="bl">사람값이 아니라 시간이었습니다.</span></div>
  <div class="note">할 일은 늘고, 뽑자니 고정비가 무섭고,<br>혼자 하자니 밤이 사라집니다.</div>
</section>

<section class="p pb0" id="staff">
  <div class="dec s">여섯 개의 자동화팀.<br><span class="bl">맡길 일을 고르세요.</span></div>
  <div class="note">1학기에는 직원 한 명씩. 2학기에는 하나의 팀으로.</div>
  {''.join(faces(t) for t in TEAMS)}
  <div class="note" style="padding-bottom:64px">직원 사진은 AI로 만든 이미지입니다.</div>
</section>

<section class="p navy tight">
  <div class="dec s">설명 대신,<br><span class="bl">일하는 화면을 보여드립니다.</span></div>
  <div class="note">아래는 메이크패밀리가 사내에서 돌린 실제 운영 기록입니다.</div>
</section>

<section class="p">
  <div class="ghost">24</div>
  <div class="z">
    <div class="opsgrid">{opscards()}</div>
    <div class="note">메이크패밀리 내부 운영 기록입니다. 수강생의 동일한 결과를 보장하지 않습니다.</div>
  </div>
</section>

<div class="ev">
  <div class="lbl"><b>말보다 먼저,<br><em>일한 화면입니다.</em></b>
    <span>AI 직원이 돌아간 뒤 남은 운영 대시보드 기록입니다.</span></div>
  <div class="shot"><img src="assets/proof/dash_18d4.jpg" alt="운영 대시보드"></div>
  <div class="shot"><img src="assets/proof/dash_7c06.jpg" alt="운영 대시보드"></div>
  <div class="shot"><img src="assets/proof/dash_19ba.jpg" alt="운영 대시보드"></div>
  <div class="cp">메이크패밀리 내부 운영 화면입니다. 수강생의 동일한 결과를 보장하지 않습니다.</div>
</div>

<div class="bleed">
  <img src="assets/presentation_01.jpg" alt="메이크패밀리 현장">
  <div class="cap">AI 빌드데이 — 6개월·12개월 차에 직접 만든 직원을 발표합니다.</div>
</div>

<section class="p tight">
  <div class="dec s">교육받은 분들은<br><span class="bl">자기 사업에서 이런 결과를 냈습니다.</span></div>
  <div class="casegrid">{casecards()}</div>
  <div class="note">학교 개설 전 기존 교육 프로그램 참여자 사례이며 운영진 성과와는 별개입니다.
    수강 전·후 비교 자료가 없어 확인된 결과만 표시합니다. 같은 결과를 보장하지 않습니다.</div>
</section>

<div class="ev">
  <div class="lbl"><b>결과 화면도<br><em>그대로 싣습니다.</em></b>
    <span>수강생이 제공한 실제 운영 결과 화면입니다.</span></div>
  <div class="shot"><img src="assets/proof/brand5_10m.jpg" alt="수강생 결제 화면"></div>
  <div class="shot"><img src="assets/proof/store_205d_crop.jpg" alt="스토어 기록"></div>
  <div class="shot"><img src="assets/proof/store_2410_crop.jpg" alt="스토어 기록"></div>
  <div class="cp">학교 개설 전 기존 교육 프로그램 참여자의 결과입니다.
    수강 전·후 비교 자료가 없어 확인된 결과만 표시했으며 같은 결과를 보장하지 않습니다.</div>
</div>

<div class="bleed">
  <img src="assets/speaker-live.jpg" alt="나민수 대표 강연">
  <div class="cap">나민수 대표가 직접 가르칩니다.</div>
</div>

<section class="p navy">
  <div class="dec s">졸업할 때 남는 것은<br><span class="bl">내 업무에서 돌아가는 AI 팀입니다.</span></div>
  <div class="rule"></div>
  <div class="bignum"><div class="lb">12개월 · 13개 과정</div><div class="v">{TOTAL}<small>강</small></div></div>
  <div class="note">매월 직원 1명씩 · 6개월 1차 졸업 · 12개월 최종 졸업</div>
</section>

<section class="w" id="curriculum">
  <div class="eb">CURRICULUM</div>
  <h2>12개월 동안<br><em>이렇게 갑니다.</em></h2>
  <div class="lead">매월 AI 직원을 한 명씩 만들어 실제 업무에 붙입니다.
    6개월 차에 1차 졸업, 12개월 차에 조직도를 발표하고 최종 졸업합니다.</div>
  {curriculum()}
</section>

<section class="w" style="background:#f9fafb" id="master">
  <div class="eb">INSTRUCTOR</div>
  <h2>AI 학교,<br><em>나민수 대표가 직접 가르칩니다.</em></h2>
  <div class="tutor">
    <img src="assets/char/namin_profile.jpg" alt="나민수 대표">
    <div>
      <div class="nm">나민수</div>
      <div class="ro">AIxSCHOOL 교장 · 메이크패밀리 대표</div>
      <ul>
        <li>사내 운영에 AI 직원을 직접 붙여 쇼핑몰 CS·업무 분배를 돌리고 있습니다</li>
        <li>우리 회사가 쓰는 AI 직원을 그대로 만드는 법을 가르칩니다</li>
        <li>매월 만든 직원을 과제로 제출하고 검토·수정·승인을 거칩니다</li>
        <li>졸업은 영상 시청이 아니라 실제로 일하는 화면으로 판정합니다</li>
      </ul>
    </div>
  </div>
</section>

<section class="price" id="apply">
  <div class="opt">
    <div class="top"><div class="nm">AI 학교 정규과정 · 12개월</div><div class="tag">정원 30명</div></div>
    <div class="row">
      <div class="mo">월 분할 시<b>275,000원</b></div>
      <div class="tot">일시납<b>3,300,000원</b></div>
    </div>
    <div class="nt">12개월 할부 기준 월 275,000원입니다. 할부 수수료와 조건은 결제 수단에 따라 다릅니다.</div>
  </div>
  <div class="cta">입학 신청하기 <i></i></div>
  <div class="fine">입학설명회에서 어떤 AI 직원이 필요한지 먼저 확인하실 수 있습니다.</div>

  <div class="notice">
    <b>신청 전에 확인해 주세요</b>
    <ul>
      <li>운영 수치는 메이크패밀리 내부 기록이며 수강생의 동일한 결과를 보장하지 않습니다.</li>
      <li>수강생 사례는 학교 개설 전 기존 교육 참여자의 결과이며 운영진 성과와 별개입니다.</li>
      <li>수강 전·후 비교 자료가 제공되지 않아 확인된 결과만 표시했습니다.</li>
      <li>졸업은 영상 시청만으로 인정되지 않습니다. 실제로 일하는 직원 화면 확인이 필요합니다.</li>
      <li>AI 직원 인물 이미지는 AI로 만든 것이며 실제 인물이 아닙니다.</li>
    </ul>
  </div>
</section>

<div class="bottombar">
  <div class="p2"><s>12개월 정규과정 · 정원 30명</s><b>3,300,000원</b></div>
  <div class="btn">입학 신청</div>
</div>

<div class="footer">
  <b>AIxSCHOOL · 메이크패밀리</b>
  AI 직원 양성 12개월 정규과정 · 6팀 24직군 · 기수 정원 30명<br>
  과목과 운영 기준은 학교 운영 정책에 따라 갱신됩니다.
</div>

</body>
</html>
"""

out = ROOT / "detail_aischool_poster.html"
out.write_text(HTML, encoding="utf-8")
print(f"{out.name} {len(HTML):,}자 · 직원 {len(ROWS)}명 · {len(CUR['months'])}개월 {TOTAL}강")
