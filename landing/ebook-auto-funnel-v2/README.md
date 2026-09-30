# 자동 퍼널 상세페이지 v2

사용자 요청: 다음 상품 자동 퍼널 전자책 제작. 헤드카피 공식(원하는 결과→수단→상품 형태)을 적용해 “매번 직접 팔지 않아도 / 구매로 이어지는 / 자동 퍼널 설계서”로 구성.

- 정본: detail.html / design.css / youtube.css / funnel.css. 승인 ASIDE·YouTube 타이포/공유배경/그라데이션/누적매출카드 재사용.
- 제품 정본: 기존 catalog-audit.json과 기존 auto-funnel brief. 현재 API 상품 282 · 판매가 50,000원 확인: qa/current-product.json. 공개라운지제공문구 재확인: qa/current-delivery.json.
- 기본몰 판매·진열중,별도몰중지; 시안은50000원. 외부운영/가격/발송변경없음.
- 원문: incoming/lounge-ebooks-20260929/lounge-books/auto-funnel/원문.md. 7장, 실제프롬프트, 7단계, 즉시+4일 후속순서 반영. 실제업무화면을 새로 지어내지 않음.
- 550개·200만원: 책1장 저자사례, AIMAX스레드가이드북 무료배포2026.07, 원문상 카페24실측. 원주문 DB독립검증을 주장하지 않음.
- 누적114.9억원: 회사전체2021.01~2024.04. 현재승인 ASIDE정본 검증기록참조; 이책단독매출로표현하지않음.
- 원래이미지3종 전부해시보존(최신표지/카카오3방/카페),기존라이선스3D아이콘3개활용. 카페화면CSS로핵심프로필/12127영역만크게표시. qa/content-evidence.json.
- 카카오2977+2710+2589=8276은방별참여합계(중복포함),카페12127은2026.09.10캡처. 독자/구매자로바꿔부르지않음.
- 헤드공식적용비교: qa/head-copy-review.json. 한글quick-rules로점검,추가윤문없이수치/주장보존게이트PASS.
- 렌더740×20277,13PNG,전체6구간직접검수. 이미지/폰트로드·넘침0,390/740실브라우저틈0,재조립픽셀일치. qa/validation.json,preview-verification.json.
- 편집HTML에서파생전체PNG/슬라이스/preview.html재생성. 썸네일은요청범위아님; hero.png는첫구간미리보기.
- 이번제작에서운영상세교체안함. 실제구매·이메일수령·회원권한동선미검증.

재현: node qa/render.mjs <상품폴더> → python3 qa/package.py → node qa/check-preview.mjs <상품폴더>.
