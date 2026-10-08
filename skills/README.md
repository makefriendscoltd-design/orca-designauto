# skills — 상세페이지를 만드는 쪽

저장소의 `landing/*` 가 결과물이라면, 여기는 그걸 **만드는 도구**다.

## 들어 있는 것

| 경로 | 뭐 하는 것 |
|---|---|
| `detail-page/scripts/render_detail.py` | HTML → 롱이미지 PNG 렌더러 (headless Edge) |
| `detail-launch/SKILL.md` | 원고 → 상세페이지 → 카페24 등록까지의 작업 절차 |
| `detail-launch/references/design-system.md` | 컴포넌트 카탈로그 · 유형별 표준 구조 |
| `detail-launch/references/cafe24-register.md` | 카페24 Admin API 로 상세·대표이미지 올리는 법 |

## 렌더러 쓰는 법

```bash
python3 skills/detail-page/scripts/render_detail.py <input.html> <out.png> [--width 740] [--maxh 80000]
```

- **`--maxh` 기본값이 40000px 이고 넘으면 조용히 잘린다.** 높이가 정확히 40000 으로
  찍히면 잘린 것이다. 긴 페이지는 `--maxh 80000` 을 준다.
- 폭: 상세 740 또는 1080 고정, 썸네일 1000, 슬라이드 1920.
- **Pretendard 를 HTML 옆 `assets/pretendard/*.woff2` 에 로컬로 둬야 한다.**
  CDN `<link>` 는 headless 에서 안 붙어 맑은고딕으로 렌더된다.
- 격리 프로필로 Edge 를 띄우고 그 PID 만 종료한다. `taskkill /IM msedge.exe` 금지 —
  열어둔 브라우저까지 죽는다.

실제 사용 예는 `landing/aischool-lms/` 를 보면 된다
(`build_lms.py` 로 HTML 생성 → 렌더 → `update_lms.py` 로 카페24 업로드).

## 안 들어 있는 것

`slice_detail.py`(롱이미지 조각내기)는 뺐다. `landing/aischool-lms/update_lms.py` 가
자체 슬라이싱 + GIF 마커 삽입을 하고 있어서 그쪽을 보는 게 빠르다. 따로 필요하면 말해라.
