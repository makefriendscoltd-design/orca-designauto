# AI로 유튜브 정복하기 v2

사용자 승인 ASIDE v3를 기준으로 재제작. 기존 운영본은 보존하고 새 정본으로 검수한다.

- 정본: detail.html / design.css / youtube.css. 기본몰 상품 321 · 판매가 110,000원. 현행값은 qa/current-product.json의 실제 API조회.
- 별도몰 shop4는99,000원·판매/진열중지. 이110,000원 시안을 shop4에 그대로 등록하지 않는다.
- 최신3D표지, 기존6개이미지 전부해시보존. 원문 검색/영상사례2개 추가.
- 937명·13만회는 원문에 실린 타채널 참고영상 사례. 회사·저자·구매자 성과로 표현하지 않는다. 채널명 루담하우스_일상 꽃의 시작.
- 누적매출카드는 최신 사용자 승인 ASIDE 정본을 재사용. 2021.01~2024.04 회사전체114.9억원. 과거 annual-only 메모보다 현재 승인누적형식을 우선한다.
- 라운지 가이드와 영상 제작 본책69쪽/별책43쪽을 구분. PDF페이지수 실제재확인; qa/content-evidence.json.
- 원문: incoming/lounge-ebooks-20260929/lounge-books/youtube-bisu/원문.md 및 pdf-books/ebook-ai-video-staff/asset-28.pdf,asset-29.pdf.
- 결과: detail_full.png 740×20237, 안전슬라이스13장, preview.html 390/740실브라우저 로드·틈0·넘침0, 재조립픽셀일치. 6구간 직접검수.
- 한글 quick-rules 검토와 의미·수치보존 게이트PASS. qa/humanize/.
- 가격/날짜/상품번호 품질게이트: qa/launch-consistency.json.
- 사용자 승인 운영교체 완료: 기본몰 상품321 PC/mobile설명·공개13이미지·가격110000원·390/1280실브라우저로드/틈0 확인. 기존판매·진열·가격보존. qa/publication-verification.json. 실제결제·권한부여·수령은 미검증.

재현: node qa/render.mjs <상품폴더절대경로> → python3 qa/package.py → node qa/check-preview.mjs <상품폴더절대경로>.

후속 히어로: 사용자 지정 “유튜브 1만 / AI로 만드는 비법서”. 1만을116px로 강조. 나머지 본문HTML 동일 검증. qa/hero-copy-verification.json.

헤드카피 제작 기준은 `.agents/skills/ebook-detail-page/references/head-copy.md`로 공식화하고 SKILL.md 진입점에서 연결했다.
