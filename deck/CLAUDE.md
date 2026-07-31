# deck — 슬라이드 덱 · PPT 레인

**여기서는 PPT만 만든다.** 상세페이지 요청이 오면 `designauto/landing/` 대화창으로 보낸다.

공통 렌더·검수·브랜드 규칙은 상위 `../CLAUDE.md`. 여기엔 덱 전용 규칙만 적는다.

## 시작할 때 — `slide-deck` 스킬을 먼저 연다

```
Skill: slide-deck
```

레이아웃 8종 템플릿과 빌드 스크립트를 들고 있다. 강의 상품이면 `class-launch` 스킬
(브리프 JSON → 덱)이 더 빠르다. 랜딩과 브리프를 공유하면 가격·일정이 어긋날 수 없다.

## 방식

파워포인트를 직접 다루지 않는다. **1920×1080 HTML 슬라이드를 세로로 쌓아 한 번에 렌더**하고,
1080px 단위로 잘라 16:9 PPTX에 이미지로 얹는다.

```
<덱>.html                 편집 마스터 (슬라이드가 세로로 쌓인 한 파일)
<덱>.pptx                 발표용 (16:9, 슬라이드당 이미지 1장)
deck_slides/slide_NN.png  낱장 (카톡·노션 배포용)
```

```bash
python ~/.claude/skills/slide-deck/scripts/build_deck.py deck.html "출력.pptx"
# 옵션: --w 1920  --h 1080  --keep-png
```

렌더 → 하단 트림 → 1080 배수 복원 → 분할 → PPTX 조립까지 한 번에 한다.

## 랜딩과 무엇이 다른가

| | 상세페이지 | 세일즈 덱 |
|---|---|---|
| 어디에 | 카페24·클래스101 등 판매 채널 | 웨비나·설명회 마지막 |
| 누가 볼 때 | 혼자, 스크롤하며 | 발표자가 말하면서 함께 |
| 역할 | 혼자 읽고 결제까지 가야 함 → **설득이 전부 들어감** | 말이 설득을 하고 화면은 근거만 → **커리큘럼·오퍼 중심** |
| 분량 | 세로 1만~2만px | 8~10장 |

**요청 범위를 좁게 읽어라.** "커리큘럼 PPT"는 문제제기·후킹까지 만들라는 뜻이 아니다.
앞단(문제 인식·공감)은 발표자가 말로 하는 경우가 많다.

## 절대 규칙

- 슬라이드 목록을 **텍스트로 먼저 확정하고** HTML을 쓴다. 몇 장, 무슨 순서인지
- `body{ width:1920px }`, 각 `.slide{ width:1920px; height:1080px; overflow:hidden }`
- **한 장이라도 1080px을 넘치면 이후 전부 밀린다.** 내용이 많으면 슬라이드를 쪼갠다
- 프레젠테이션은 멀리서 본다 → h1 104 / h2 76 / 본문 30~36px. **상세페이지보다 더 크게**
- 페이지 번호는 `.pnum` 으로 우하단 고정

## 검수

빌드 출력의 **슬라이드 장수가 예상과 다르면 넘친 슬라이드가 있다.** 낱장 PNG로 잡는다.

```python
from PIL import Image; import glob
fs = sorted(glob.glob('deck_slides/slide_*.png')); w, h = 560, 315
sheet = Image.new('RGB', (2*w, ((len(fs)+1)//2)*h), '#dfe3ea')
for i, f in enumerate(fs):
    sheet.paste(Image.open(f).resize((w-8, h-8)), ((i%2)*w+4, (i//2)*h+4))
sheet.save('grid.png')
```

넘침·잘림 · 폰트가 Pretendard인지 · 밝은/어두운 슬라이드 리듬 · 숫자 일관성.

## 이 레인의 함정

- **텍스트 편집 불가.** 슬라이드가 이미지라 파워포인트에서 문구를 못 고친다.
  → 수정은 HTML을 고쳐 재빌드(30초). **사용자에게 이 점을 먼저 알린다**
- **마지막 슬라이드가 흰 배경이면 하단이 잘린다.** 스크립트가 배경색으로 되메우지만 장수를 꼭 확인
- 4,000px 넘는 이미지를 슬라이드에 넣지 말 것 (렌더러가 얼어붙음)
- `class-launch` 로 뽑을 때 `[warn] 모집정보 N행` 이 뜨면 표가 잘린 것
  → 브리프에 `info_rows_deck` 로 덱 전용 행을 따로 준다
- 표지용 강사 사진은 **누끼**(`instructor.photo_cut`)를 쓴다. 원본 사각형은 티가 난다

## 참고 사례

- `design/bloomingbon-class/sales_deck.html` + `블루밍본 4주 커리큘럼.pptx` — 9장 세일즈 덱
  (표지·개요·주차4·제공물·진행안내·가격)
- `design/bloomingbon-class/brief.json` — 검증된 브리프
- 레이아웃 8종: `~/.claude/skills/slide-deck/references/template.html`
