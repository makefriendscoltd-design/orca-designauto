# 컨셉의 정석 상세페이지 — 승인 제작 방식 v10

정본은 `detail.html`, `design.css`, `assets/`. 출력은 `detail_full.png`(740×50441)와 `slices/`34개다. 현재 상품284의 이미지 교체용 결과물이다.

제작 기준: [레퍼런스 재구현 방식](../../.agents/skills/ebook-detail-page/references/reference-rebuild.md).

## 재현

1. HTML/CSS/원본애셋을 수정한다. PNG나 슬라이스를 직접 수정하지 않는다.
2. `detail-page` 스킬의 render_detail.py로 출력한다:
   `python3 <skill-root>/detail-page/scripts/render_detail.py detail.html detail_full.png --width 740 --maxh 80000`
3. 저장소 루트에서 `node landing/ebook-concept-ecommerce-v10/qa/check-runtime.mjs landing/ebook-concept-ecommerce-v10`으로 검수한다. Node의 WebSocket 지원 및 로컬 Chrome 필요. macOS 기본경로 외 환경은 `CHROME_BIN`을 지정한다.
4. 전체4~6구간과 수정한 애셋을 직접 확인한다.
5. `python3 landing/ebook-concept-ecommerce-v10/scripts/build_slices.py`로 재분할한다(Pillow 필요).
6. 운영값 검사를 통과한 뒤 별도 Cafe24 운영작업공간에서 백업·업로드·교체·공개페이지검증한다. 이 저장소에는 토큰이나 운영 API 백업을 넣지 않는다.

표지 출처와 예시이미지 경로는 `qa/asset-provenance.json`. 현재 표지는 실제 패밀리라운지 BookCover 3D 컴포넌트에서 렌더한 정본이다. 과거 `cover_cut.png`를 다시 사용하지 않는다. 본문사진은 원문 설명용 예시이며 성과증거가 아니다.

렌더·폰트·이미지 로드·텍스트넘침·슬라이스 픽셀 검증 결과는 `qa/runtime.json`, `qa/validation.json`. 저자·상품·가격 내용은 자동으로 새 버전에 따라가지 않으므로 다음 출시에서는 운영 정본을 다시 대조한다.

## 등록 완료 — 2026-09-30

상품284, shop1/shop4의 PC·모바일 상세이미지를 v10 34장으로 교체했다. 독립 API 읽기 및 공개 PC·모바일4경로에서 새 이미지34장과 기존 가격을 확인했다. 상품명·가격·판매/진열·대표이미지 보존. 검증요약은 `qa/published.json`. 외부등록 백업과 실행기록은 Cafe24 운영작업공간에 보관한다.
