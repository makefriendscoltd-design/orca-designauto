# designauto — 랜딩/덱 제작 작업실

상세페이지 · 썸네일 · 슬라이드덱을 **HTML/CSS로 만들고 headless로 렌더해
이미지·PPTX로 뽑는** 작업 폴더. 포토샵을 쓰지 않는다.

## 두 레인 — 대화창을 나눠서 쓴다

랜딩페이지와 PPT는 쓰는 자리도, 설득 방식도 다르다. 섞으면 서로의 톤이 오염된다.
**각 레인에서 별도 대화창을 연다.**

| 레인 | 폴더 | 무엇을 | 어디서 열까 |
|---|---|---|---|
| **랜딩** | `designauto/landing/` | 상세페이지 1080px 롱이미지 · 썸네일 1000×1000 | 이 레인 대화창 |
| **덱** | `designauto/deck/` | 1920×1080 슬라이드 → `.pptx` | 별도 대화창 |

각 폴더에 자체 `CLAUDE.md` 와 `assets/pretendard/` 가 들어 있다. 그 폴더에서 세션을 열면
이 파일(공통 규칙) + 레인 CLAUDE.md 가 함께 읽힌다.

**assets 는 레인마다 복사본을 둔다.** HTML이 `assets/...` 상대경로를 쓰기 때문에
공용 폴더로 빼면 렌더가 깨진다.

## 이웃 폴더

| 폴더 | 무엇이 있나 |
|---|---|
| `orca/projects/design/` | 이전 브랜드별 산출물 (aimax-ebook · bloomingbon-class · makefamily-webinar) — 참고 사례 |
| `orca/projects/threads guide/` | 전자책 원고 HTML/PDF |
| `~/.claude/skills/` | 현재 돌아가는 스킬 3종 (아래) |
| `D:\coding\*`, `orca/projects/cafe24` | 발행·문자 자동화 (토큰이 절대경로라 이동 금지) |

## 현재 자동화 자산 (2026-07 기준)

이미 유저 레벨 스킬로 굳어 있다. **새로 만들기 전에 이걸 먼저 본다.**

| 스킬 | 입력 → 출력 | 스크립트 |
|---|---|---|
| `class-launch` | `brief.json` → 상세페이지 / 세일즈덱 | `scripts/build_class.py` |
| `detail-page` | 1080px HTML → 롱이미지 → 슬라이스 | `scripts/render_detail.py`, `slice_detail.py` |
| `poster-detail` | 레퍼런스 실측 → 860px 포스터판 상세 → 슬라이스 | `scripts/measure_type.py`, `compare_scale.py`, `slice_poster.py` |
| `slide-deck` | 1920×1080 HTML → `.pptx` + 낱장 PNG | `scripts/build_deck.py` |

```bash
python3 ~/.claude/skills/class-launch/scripts/build_class.py brief.json --detail --render
python3 ~/.claude/skills/class-launch/scripts/build_class.py brief.json --deck   --render
python3 ~/.claude/skills/detail-page/scripts/render_detail.py detail_x.html detail_x_full.png
python3 ~/.claude/skills/detail-page/scripts/slice_detail.py detail_x_full.png ./slices --width 1080 --chunk 1500
python3 ~/.claude/skills/slide-deck/scripts/build_deck.py deck.html "출력.pptx"
python3 ~/.claude/skills/poster-detail/scripts/measure_type.py ref.png --width 860   # 레퍼런스 실측 먼저
```

**맥에는 `python` 이 없다. `python3` 로 쓴다.** 스크립트가 Pillow 없는 인터프리터로 실행되면
`~/.claude/skills/.venv` 로 알아서 재실행하므로 어떤 python3 를 써도 된다.

브리프 스키마는 `~/.claude/skills/class-launch/references/brief.schema.md`,
검증된 실제 브리프는 `references/brief.example.json`(블루밍본 4주) 또는
`design/bloomingbon-class/brief.json`.

### 아직 스크립트가 없는 구간 (자동화 후보)

- **전자책 PDF 렌더·검수** — `render_pdf.py` / `montage.py` / `half.py` 를 매번 스크래치패드에
  다시 썼다. 꼬리 페이지 판정(`body_bottom/H < 0.5`)까지 포함해 고정 툴로 만들 값어치가 있다
- **누끼 따기** — 단색 배경 인물 사진(중성 회색 키잉 + 플러드필). 절차는 문서에만 있고 코드가 없다
- **검수 몽타주** — 상세 4등분 / 덱 격자 / PDF 8×N 그리드가 세 스킬에 각각 인라인 코드로 흩어져 있다.
  하나의 `contact_sheet.py` 로 합칠 수 있다
- **가격 일괄 반영** — 가격은 상세이미지·썸네일·판매채널 3곳에 박힌다. 지금은 수동

## 맥 작업 환경 (26-08-04 이관 완료)

원래 윈도우에서 돌리던 파이프라인을 이 맥으로 옮겼다. **아래는 실제로 렌더까지 돌려 확인한 상태다.**

| | 값 |
|---|---|
| 렌더 브라우저 | **Google Chrome 151** (`/Applications/Google Chrome.app`) — 스크립트가 자동 탐색 |
| 파이썬 | `~/.claude/skills/.venv` (3.14) — Pillow · python-pptx · PyMuPDF · requests · numpy |
| 실행 | `python3 <스크립트>`. Pillow 없는 python3 로 실행돼도 위 venv 로 자동 재실행된다 |
| 카페24 토큰 | `~/coding/cafe24bot/token.json` — `_c24.py` 가 자동으로 찾는다 |
| 발송 코드 | `~/orca/projects/cafe24/`(문자·메일) · `~/orca/projects/familypartners/`(뿌리오 자격증명) |

- 브라우저 탐색 순서는 `render_detail.py` / `build_deck.py` 의 `BROWSER_CANDIDATES` 에 있다.
  Chrome → Edge → Chromium → Brave → playwright 번들 순. **윈도우 경로도 그대로 남겨뒀으니
  같은 스크립트가 양쪽에서 돈다.**
- **`D:\coding\...` · `C:\Users\hey_m\...` 로 적힌 경로를 보면 옛 문서다.** 위 표의 맥 경로로 읽는다.
- 아직 못 옮긴 것: `brain-council` 스킬이 가리키는 볼트가 이 맥에 없다
  (`~/brain-sangchul` 은 6축 구조라 다른 자료다). 디자인 파이프라인과는 무관.

## 렌더 규칙 (실측으로 굳힌 것, 어기면 깨진다)

- **Pretendard 로컬 `@font-face` 필수.** CDN `<link>` 는 headless에서 안 붙어 맑은고딕으로 렌더된다.
  HTML 옆에 `assets/pretendard/*.woff2` 5종을 둔다 — 공용 폴더로 빼면 상대경로가 깨진다.
  원본: `orca/projects/design/aimax-ebook/assets/pretendard/`
- **전역 브라우저 kill 절대 금지** (윈도우 `taskkill /IM msedge.exe` · 맥 `pkill Chrome`).
  유저가 열어둔 브라우저까지 죽는다.
  `--user-data-dir=<격리프로필>` 로 띄우고 그 PID만 종료 — 세 스킬 스크립트엔 이미 반영됨
- **맥은 폰트 폴백이 안 보인다.** 윈도우는 Pretendard 로딩 실패 시 맑은고딕이라 딱 티가 나는데,
  맥은 Apple SD Gothic Neo 로 떨어져 그럴싸하게 보인다. **높이가 기준선과 다르면 폰트 실패를 의심할 것**
  (같은 HTML이면 맥·윈도우 렌더 높이가 픽셀 단위로 같다 — 26-08-04 실측으로 확인)
- **Edge stale 렌더(윈도우 한정).** 이전 msedge 프로세스가 안 죽으면 재렌더가 무시되고 **이전 파일 바이트가 그대로 남는다.**
  페이지 수가 같으면 못 알아챈다 — 파일 크기가 그대로면 의심할 것.
  렌더 전 kill + 대기를 스크립트에 내장한다
- Edge headless는 print-to-pdf 후 프로세스가 안 닫힌다(파일은 정상 기록) → size stable 폴링 후 격리 PID 종료
- `print-color-adjust:exact` — 없으면 배경색이 날아간다
- 폭: 상세 **1080px 고정**(반응형 아님, `word-break:keep-all`), 슬라이드 **1920×1080**
- 4,000px 넘는 이미지를 에디터·슬라이드에 넣으면 브라우저가 얼어붙는다
- 슬라이드는 한 장이라도 1080px을 넘치면 이후 전부 밀린다

## 검수 규칙

**생성물은 초안이다. 반드시 눈으로 본다.**

- 상세페이지: 4등분해서 Read (폰트가 Pretendard인가 · 넘침 · 가격 숫자 일치 · 다크/라이트 리듬)
- 덱: 낱장 PNG를 격자로 붙여 한 장으로 확인. 장수가 예상과 다르면 넘친 슬라이드가 있다
- PDF: PyMuPDF로 8×N 몽타주 렌더 후 Read. **잉크 %는 지표로 못 쓴다** —
  텍스트 페이지는 줄간 여백 때문에 7~10%가 정상
- 꼬리(반쯤 빈) 페이지 판정: 페이지별 `body_bottom/H` (runfoot 제외, y>0.9 필터) < 0.5

### 페이지브레이크 교훈

`page-break-inside:avoid` 박스는 통째로 다음 장으로 튀기 때문에 **여백만 조여선 임계를 못 넘는다.**
1. 문서 전용 밀도 CSS로 먼저 조인다 (font-size · line-height · padding · 콜아웃 패딩)
2. 그래도 남는 트레일링 박스는 **앞 페이지에서 박스 높이(~18mm)만큼 실제 내용을 걷어낸다.** 찔끔은 소용없음
3. 트레일링 블록(take/규칙)은 앞 요소의 why/카드에 접어넣어 orphan 자체를 막는다
4. 고치면 재렌더 + 몽타주로 재확인 — 두더지잡기가 된다

## 디자인 규칙

- **본문 카피에 이모지 금지.** 구어체로. 매끄러운 마케팅 카피는 AI 티가 난다.
  (26-08-09 완화 — 와디즈/타이탄 문법의 **포스터형 장식 요소**로 쓰는 건 예외.
  문장 사이에 뿌리는 게 AI 티지, 그래픽으로 쓰는 건 아니다. 컬러 이모지는 렌더된다)
- 방어 가능한 수치만. 과장 금지
- 밝은 섹션만 이어붙이지 말고 다크 섹션을 3~4개 간격으로
- 폰트는 웹 감각보다 크게 — 상세 h1 104 / h2 66 / 본문 25~27px, 덱 h1 104 / h2 76 / 본문 30~36px
- 전자책 본문 `line-height: 1.95` (스레드 가이드북 계열), 밀도가 필요한 책만 1.74로 조인다

### 브랜드 컬러

| 프로젝트 | 액센트 | 베이스 |
|---|---|---|
| AIMAX | `#1B3C9C` (로고 실측) / 상세는 `#2b52ff` | 네이비 |
| 블루밍본 | `#2b52ff` | 네이비 |
| 메이크패밀리 웨비나 | `#0aa2c0` / 밝은 `#5ee0f5` | 블랙+시안 |

## 운영 주의

- **가격은 상세이미지 · 썸네일 · 판매채널 3곳 세트로 바꾼다.** 하나만 바꾸면 클레임
- "판매량 늘수록 인상"이라 썼으면 실제로 그렇게 운영해야 한다 (표시광고법)
- 이미지 교체 시 파일명을 바꾼다. 같은 이름이면 캐시 때문에 확인이 안 된다

## 알려진 문서 오류

스킬 문서의 "실제 사례" 경로가 폴더 분리(26-07-28) 전 기준으로 남아 있다. 실제 위치:

| 문서가 가리키는 곳 | 실제 위치 |
|---|---|
| `threads guide/detail_v2.html`, `detail_premium.html`, `thumbnail_premium.html`, `cafe24_order_result_delivery.html` | `design/aimax-ebook/` |
| `threads guide/sales_deck.html` | `design/bloomingbon-class/` |
