# 랜딩페이지의 정석 v6

실제 강의 상세페이지 3곳의 HTML/CSS를 조사하고 자체 코드로 재구성. 조사·적용 근거는 REFERENCES.md.

정본: detail.html + design.css. 학습 예제 정본: example-page.html. 최신3D표지 유지. 생성 화장품 사진 삭제. 결과물3종 → 사례3단계 → 운영사 누적 매출 → 목차·수령·FAQ 순서.

상품297·판매가30,000원. 740×11064px, PNG8개. preview.html·detail_full.png·slices/ 제공.

검증: 전체6구간 직접 확인, 390/740px 이미지로드·가로넘침·틈0, 슬라이스 재조립 원본일치. 운영 등록 미실행.

재생성:
```sh
node landing/ebook-landing-page-v6/qa/render-example.mjs landing/ebook-landing-page-v6
node landing/ebook-landing-page-v6/qa/render.mjs landing/ebook-landing-page-v6
python3 landing/ebook-landing-page-v6/qa/package.py
node landing/ebook-landing-page-v6/qa/check-preview.mjs landing/ebook-landing-page-v6
```
