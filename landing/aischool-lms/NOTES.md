# AIxSCHOOL 입학 상세 — 카페24 상품 395

`[AIxSCHOOL] AI 학교 입학 신청하기` · 3,300,000원 · 1년 과정 · 진열 중
라이브: https://makefamily.kr/product/detail.html?product_no=395

## 빌드 → 렌더 → 업로드

```bash
python3 build_lms.py                                  # 데이터 읽어 detail_lms.html 생성
python3 ~/.claude/skills/detail-page/scripts/render_detail.py \
        detail_lms.html out/lms_poster.png --width 740 --maxh 60000
rm -f _up_lms.json                                    # 이미지 바뀌었으면 캐시 삭제 필수
~/orca/projects/cafe24/.venv/bin/python update_lms.py # shop1·4 동시 주입
```

렌더에 **Chromium 계열 + Pretendard 로컬 폰트**가 필요하다. `assets/pretendard/*.woff2` 가 HTML 옆에
있어야 하며 CDN `<link>` 로 바꾸면 headless 에서 폰트가 안 붙는다.

## 구조

벤치마크는 이상한마케팅 LMS 강의상세. 가져온 것은 **레이어 순서·강조 위계·컴포넌트 문법**이고
문구·사진·커리큘럼은 전부 AIxSCHOOL 자체 자산이다.

```
상단바 → 상품명·메타·배지 → 운영 기록 3줄 → 스티키 탭
→ 후킹 → 사람 vs AI → AI 직원 24명(팀별 영상+타일) → 100명 양성 → 조직도
→ 운영 수치 → 카운트업 → 12개월 선언
→ 커리큘럼 13블록 40강 → 교장 → 입학 절차
→ 숏폼 계산면 → 주문 스크롤 → CS 계산면 → 밸류스택 → 사람 뽑으면
→ 빌드데이 → FAQ → 가격·CTA → 푸터
```

**FAQ·주의사항은 반드시 맨 뒤, 최종 CTA 직전이다.** 레퍼런스가 그 순서다.

## 타입 스케일 — 줄이지 말 것

`xl 108 / lg 80 / md 60 / sm2 44 / cap2 28 / cap 24`, 면 패딩 150px.
**이보다 줄이면 다시 웹페이지처럼 보인다.** 실측으로 확정된 값이다.

## GIF 는 마커로 들어간다

롱이미지로 구우면 GIF 가 정지하므로, HTML 에는 `<div class="gifmark">`(마젠타 60px)만 굽고
`update_lms.py` 가 그 띠를 찾아 **`_gifseq.json` 순서대로** 실제 GIF 파일을 끼운다.

- 마커가 연달아 붙으면 한 덩어리로 잡히므로 높이(60px)로 나눠 개수를 복원한다
- GIF 를 추가·삭제하면 `_gifseq.json` 이 자동 갱신된다. 손으로 고치지 않는다

## ⚠️ 영상 고를 때 — 브랜드 함정

이 페이지의 브랜드는 **AIxSCHOOL 하나**다. 화면에 `AIMAX`·`메이크패밀리` 가 보이면 안 된다.

소재 원본: `~/orca/workspaces/family_pm/ai학교/landing-video-broll/out/mp4` (55개, 전부 AIxSCHOOL 판)
**`demo-*` 계열(aixschool/source/home-static/media/video)은 대부분 AIMAX 화면 녹화다.**
쓰기 전에 상단 14% 를 잘라 로고를 확인할 것:

```bash
ffmpeg -ss 2 -i <영상>.mp4 -frames:v 1 -vf "crop=iw:ih*0.14:0:0" /tmp/chk.jpg
```

격리 이력은 `gifs/_banned/README.md`.

## 표기 규칙 (확정)

- 브랜드는 **AIxSCHOOL** 하나. `AIMAX`·`메이크패밀리` 금지
- 가격은 **월 275,000원만**, 페이지에 한 번. 총액 3,300,000 은 쓰지 않는다
  (카페24 스킨의 총액 표시는 `update_lms.py` 의 `<style>` 로 덮는다)
- **성과 캡션에 기간·날짜 범위를 적지 않는다** (개인정보로 반려된 이력)
- **나민수 외 식별 가능한 인물 사진 금지.** 현장은 청중·실습 테이블만
- 내부 용어 금지 — `업무 카드` → `할 일`, 제작 메모(`SHOT`·`후킹`)가 노출되면 안 된다

빌드 후 점검:
```bash
grep -c "메이크패밀리\|AIMAX\|3,300,000\|SHOT\|후킹\|업무 카드" detail_lms.html   # 0 이어야 한다
```

## ⚠️ 가짜 UI 를 그리지 않는다

카페24가 이미 헤더·상품명·탭·푸터를 그린다. 이미지 안에 또 그리면 중복이고 **눌리지도 않는다.**
상단바·뒤로가기·상품명·배지·스티키 탭·푸터를 넣었다가 전부 뺐다.
(`family-ai-school/CLAUDE.md` 에 이미 있던 규칙 — "이미지 안에서 눌리지 않는 UI 는 넣지 않는다")

## 유튜브 ID 와 대표이미지

- 영상 ID 정본은 `aixschool/public/admission/assets/video.generated.js` → **`e2Jp0D3jwOU`**
  옛 `Y1k44op1ZLk` 는 **비공개(403)** 라 상단에 접근 권한 오류가 떴다. 스크립트를 물려받을 때 확인할 것
- **대표이미지도 같이 갱신한다.** 상세만 바꾸면 스킨 상단에 옛 썸네일이 그대로 남는다.
  `thumb_lms.html` → `out/thumb_lms.png` → `update_lms.py` 가 자동 교체.
  나민수는 **누끼본**(`assets/char/namin_cut.png`)을 쓴다. 원본 jpg 는 흰 배경이 네모로 박힌다

## GIF 는 전체 길이 + 배속으로 뽑는다

앞부분만 잘라 쓰면 **애니메이션이 중간에 끊긴다.** 팀 영상은 13.3초짜리인데 3초만 써서
네 단계 중 둘까지만 보였다. 전체를 담고 `setpts=PTS/배속` 으로 5초 안에 한 바퀴가 끝나게 한다.

```bash
ffmpeg -y -nostdin -v error -i IN.mp4   -vf "setpts=PTS/2.66,fps=10,scale=700:-2:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=${cols}[p];[s1][p]paletteuse=dither=bayer:bayer_scale=5" OUT.gif
```

**두 번 조용히 실패했다. 둘 다 기억할 것:**
1. **`-nostdin` 없으면** ffmpeg 이 `while read` 루프의 stdin 을 먹어 루프가 깨진다
2. **zsh 는 `$cols[p]` 를 배열 첨자로 해석한다.** `${cols}` 로 감싸야 `max_colors` 가 빈 값이 안 된다
   (`2>/dev/null` 로 에러를 가리면 옛 파일이 그대로 남아 성공한 것처럼 보인다 — 용량·프레임수로 검증할 것)

## 증명자료 — 숫자만 적지 않는다

운영 수치 뒤에는 **실제 운영 화면**을 붙인다. 캡처 정본은 `aixschool/public/media/shots/*.webp`
(`l15-*` 주문 안내 3단계, `perf2025-*` 유입·결제, `revenue-dashboard-card-masked`).

**주석이 그려진 캡처는 쓰지 않는다.** 빨간 화살표·형광 박스가 구워진 내부 검토본이 섞여 있다
(`assets/_annotated/` 에 격리). 쓰기 전에 빨강·시안 픽셀 비율로 걸러낼 것.

## 고관여 페이지 — 크게, 하나씩

리뷰 피드백(2026-10-08): **작은 그리드로 여러 개 보여주지 말고 한 면에 하나씩 크게.**
임금 비교 6개를 6칸 그리드에서 6면으로 풀었다(`.wg`). 인물 190px · 직무 46px · 월급 58px 취소선.

## 데이터 출처 (빌드마다 직접 읽는다)

| 파일 | 경로 |
|---|---|
| 커리큘럼 13블록 40강 | `aixschool/public/curriculum.json` |
| 6팀 24직군 | `aixschool/public/staff.json` |
| 직군 설명·구분 꼬리표 | `teams.json` (이 폴더) |
| 3개월 개편안(보류) | `_curriculum_3m_proposal.json` |
| 연출컷 슬롯 정의 | `shots.json` |

`teams.json` 은 팀 구성을 바꾸지 않는다. 겹쳐 보이는 직군(숏폼↔릴스PD, 카페 글↔카페 응대)을
**설명과 꼬리표로만** 구분한다 — 초보 수강생 기준.

## 남은 일

- 연출컷 슬롯 13개(`shots.json`)는 아직 비어 있다. `shots/<id>.jpg` 로 넣으면 자동으로 박힌다
- 24직군 개별 영상(`08-staff-01~24`)은 팀별 6개만 썼다. 수강신청 섹션을 만들면 과목마다 붙일 수 있다
- 밸류 스택의 "직원 1명당 100만원"은 숏폼·CS 두 개만 계산식이 있다. 나머지는 근거 없음
