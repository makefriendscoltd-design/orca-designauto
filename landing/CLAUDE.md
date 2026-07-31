# landing — 상세페이지 · 랜딩페이지 레인

**여기서는 상세페이지와 썸네일만 만든다.** PPT 요청이 오면 `designauto/deck/` 대화창으로 보낸다.

공통 렌더·검수·브랜드 규칙은 상위 `../CLAUDE.md`. 여기엔 랜딩 전용 규칙만 적는다.

## 시작할 때 — `detail-launch` 스킬을 먼저 연다

```
Skill: detail-launch
```

원고 붙여넣기 → 상세페이지·썸네일 → 카페24 등록까지 한 스킬로 커버한다.
제작만 필요하면 `detail-page`, 커리큘럼 브리프에서 시작하면 `class-launch`.

### 0단계는 "같은 유형을 먼저 연다"

**이걸 건너뛰면 품질이 매번 리셋된다.** 실제로 26-07-29 실크로드 웨비나를 만들 때
아래 표의 웨비나 사례를 안 보고 범용 템플릿에서 새로 지었다가,
신청자 혜택 섹션 누락 · tutor 컴포넌트 미사용 · 길이 2.4배가 나왔다.

| 만들 것 | 먼저 열 것 |
|---|---|
| **무료 웨비나·특강 모집** | **`design/makefamily-webinar/detail_webinar.html`** |
| 무료 전자책 | `design/aimax-ebook/detail_v2.html` |
| 유료 전자책·디지털 | `design/aimax-ebook/detail_premium.html` |
| 유료 강의·클래스 | `design/bloomingbon-class/detail_class_v2.html` |

## 산출물 이름 규칙

```
detail_<상품>.html          편집 마스터 (1080px 고정폭)
detail_<상품>_full.png      렌더된 롱이미지 → 상세설명에 업로드
slices_<상품>/*.jpg         조각 (에디터 업로드용)
thumbnail_<상품>.html/.png  1000×1000 대표이미지
```

상품이 여러 개면 `landing/<상품>/` 하위 폴더로 나누고 `assets/` 를 그 안에 복사한다.

## 명령

```bash
S=~/.claude/skills
python $S/detail-page/scripts/render_detail.py detail_x.html detail_x_full.png
python $S/detail-page/scripts/render_detail.py thumbnail_x.html thumbnail_x.png --width 1000
python $S/detail-page/scripts/slice_detail.py detail_x_full.png ./slices_x --width 1080 --chunk 1500
```

## 0단계 — 정보 먼저 받는다 (없으면 물어본다)

수치가 없으면 페이지가 텅 빈다. **"신뢰도" 섹션에 넣을 숫자 3개는 반드시 확보.**

상품명 / 분량·형태 / **정가와 판매가** / 타깃 / 자랑할 실측 수치 / 보너스 /
수령 방식(이메일·링크) / 무료본 존재 여부 / 희소성 장치(한정가·인상 예고).

## 뼈대 — 랜딩 7단계

상세페이지는 이미지 모음이 아니라 **순서가 있는 설득**이다.

| 랜딩 7단계 | 섹션 | 역할 |
|---|---|---|
| ① 도입부 | HERO | 3초 안에 "이게 뭐고 얼마인가" |
| ② 공감대 | 문제 제기 `.pains` | 고객 말투로 증상 3개 |
| ③ 신뢰도 | 데이터/실적 `.grid3` `.metabar` | 숫자로 자격 증명 |
| ④ 문제 제기 | 다크 선언 `.state` | "다른 자료로는 왜 안 됐나" |
| ⑤ 해결방안 | 커리큘럼 `.parts` · 전용 무기 `.vault` · 비교표 `.cmp` | 내용물 전개 |
| ⑥ 반박 제거 | 적합/부적합 `.fitgrid` · 보증 `.guar` · FAQ | 구매 저항 해체 |
| ⑦ CTA | 최종 CTA `.cta` | 가격 재확인 + 행동 |

보너스 `.bonus` · 희소성 `.rise` 는 ⑤와 ⑦ 사이에 끼워 밀도를 올린다.

**무료 리드마그넷 7섹션 / 유료 상품 13섹션.** 무료본이 이미 있으면 유료 상세엔
**비교표 `.cmp` 가 사실상 필수** — "무료 봤는데 왜 또 사?"가 최대 반박이고 표 하나가 그걸 해결한다.

## 시각 리듬

```
HERO(다크) → rise(연블루) → pain(흰) → data(흰) → state(다크) →
cmp(흰) → parts(흰) → vault(딥네이비) → fit(흰) → bonus(연블루) →
guar(다크) → faq(흰) → CTA(액센트 풀블리드)
```

- 1080px 기준 스케일: h1 104 / h2 66 / 리드 30 / 본문 25~27 / 캡션 22.
  **모바일에서 축소돼 보이므로 웹 감각보다 1.5~2배 크게.**
- 섹션 패딩 110/90 고정. 흔들면 리듬이 깨진다
- h1/h2는 2줄, 뒷줄에 `.hl` 하이라이트. 한 줄짜리 긴 제목은 임팩트가 죽는다

## 검수

렌더 후 **반드시 4등분해서 눈으로 본다.** 긴 이미지는 Read로 한 번에 안 보인다.

```python
from PIL import Image
im = Image.open("detail_x_full.png"); W,H = im.size; N = 4
for i in range(N):
    p = im.crop((0, i*H//N, W, H if i==N-1 else (i+1)*H//N))
    p.resize((760, round(p.height*760/W))).save(f"chk_{i}.png")
```

폰트가 Pretendard인가(맑은고딕이면 로딩 실패) · 글자 넘침 · **가격 숫자 일치** ·
섹션 여백 리듬 · 다크/라이트 교차.

## 이 레인의 함정

- **가격은 상세이미지 · 썸네일 · 판매채널 3곳에 박힌다.** 세트로 안 바꾸면 클레임
- "판매량 늘수록 인상"이라 썼으면 **실제로 그렇게 운영해야 한다** (표시광고)
- 부적합 목록에 **진짜 비추천**을 적는다. 형식적으로 쓰면 역효과, 진짜로 쓰면 환불·클레임이 준다
- 4,000px 넘는 이미지를 에디터에 넣으면 브라우저가 얼어붙는다 → 반드시 슬라이스
- 반응형 HTML 직접 붙여넣기는 **탈락한 방식**이다(에디터가 CSS를 먹는다).
  1080 롱이미지가 표준. 고객이 텍스트를 복사·검색해야 할 때만 반응형을 고려

## 참고 사례

- **`design/makefamily-webinar/detail_webinar.html` — 무료 웨비나 모집 9섹션 7,530px.
  모집 페이지의 기준점.** whenbar · machine · topics · bonus · tutor
- `design/aimax-ebook/detail_v2.html` — 무료 7섹션
- `design/aimax-ebook/detail_premium.html` — 유료 13섹션 (유료 표준)
- `design/aimax-ebook/thumbnail_premium.html` — 1000×1000 썸네일 패턴
- `design/aimax-ebook/cafe24_order_result_delivery.html` — 주문완료 자동수령 박스
- `design/bloomingbon-class/detail_class_v2.html` — 유료 강의 상세 (컴포넌트 36개, 가장 발달)

컴포넌트 카탈로그와 유형별 표준 구조는 `~/.claude/skills/detail-launch/references/design-system.md`.
