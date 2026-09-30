# ASIDE 블로그 전자책 v3

2026-09-30. v2를 사용자가 디자인 퇴화로 반려. 직전 승인 Threads PREMIUM/컨셉 v10의 실제 렌더와 치수를 기준으로 다시 제작했다. v2는 보존한다.

## 변경

- 짙은 배경, 금색 그라데이션 제목, 대형3D 표지, 광원·스포트라이트 전환. 제목79px/리드44px, 비교33px/65px, 본문34–37px로 역할을 구분했다.
- 순서: 히어로 → 메이크패밀리 블로그 이웃 증거 → 실제 작성GIF → 반복 수작업 문제 → 저자 → 준비/지시/검수 → 목차 → 기존 회사·커뮤니티 증빙 → FAQ/구매.
- 네이버 블로그 @makefamily_ 공개 프로필에 표시된 이웃10,700명을 강조. 조회일2026.09.30. 실제 페이지 캡처와 HTML subscriberCount 대조. ASIDE로 늘어난 수치라고 주장하지 않는다.
- 09.22 실제 라이브 원본의00:34:45–00:35:02를 추출. 빈 에디터→제목·본문 입력→이미지 삽입. 재연·생성 화면 없이17초 원속도 반복.
- 기존8개 증빙·표지 이미지 해시와 기존 연간/교육/회원 수치를 유지했다.

## 정본·출처

- 운영값 정본: `../lounge-rebuild-20260930/catalog-audit.json`, presentationId `aside-blog`. 상품399,30,000원, 주문 이메일PDF 수령/동일이메일 라운지 재열람 유지.
- 내용: `../../incoming/lounge-ebooks-20260929/pdf-books/ebook-aside-blog/제작브리프.md`, `asset-35.pdf`.
- 이미지 계보: `../lounge-rebuild-20260930/aside-blog/qa/asset-provenance.json`, `qa/evidence-restored.json`.
- 블로그 원문: https://m.blog.naver.com/makefamily_ . `qa/blog-evidence.json`, `assets/evidence/blog-neighbors.png`.
- 이웃수는 원문 화면의 충실한 인용이다. 공개프로필이 유일한 원출처이며 외부기관 독립확인은 없음. 연구게이트의 숫자주장2기관 조건을 충족했다고 보고하지 않는다. 강한 인과·효과 주장으로 확대하지 않는다.
- 영상 원본 및 크롭: `qa/live-provenance.json`. 원본 동영상은 저장소에 복사하지 않았다.

## 출력과 검수

- 편집 정본: `detail.html`, `design.css`.
- **GIF 포함 미리보기: `preview.html`**. PNG12장과 실제 GIF1개를 조합한다. GIF 영역은 정적 슬라이스로 대체하지 않는다.
- `detail_full.png`: 740×20562, GIF는 대표 프레임으로 보여주는 정적 전체 보기.
- `hero.png`: 첫 화면. 별도 상품 썸네일은 요청 범위에 없음.
- GIF: `assets/live/aside-live-writing.gif`,740×600,170프레임,17초,약558KB. 에디터 영역만 원본에서 크롭했다.
- `qa/package.py`: 정적 영역 안전절단, GIF 행 별도 유지, 대표 프레임 재조립 전체픽셀 일치 검사.
- `qa/runtime.json`: 폰트5종·모든 이미지 로딩, 가로 텍스트 넘침0.
- `qa/region-1.png`~`region-6.png`: 전체6구간 직접 검수. 신규 블로그 캡처/라이브 포스터/원본 연속프레임도 확인.
- `qa/evidence-coverage.json`: 기존8개 이미지 누락0, 원본해시 일치.
- `qa/humanize/gates.txt`: 최신 설치본 quick-rules 직접 점검, 의미보존·수치·인용·말투 게이트PASS. 초안후 추가윤문0%.
- `qa/launch-consistency.json`: 불일치0. 시간검출은 영상오프셋·촬영기록·코드 포맷이며 행사 일정이 아니다.
- `qa/gif-verification.json`:170프레임/17000ms/111개 서로 다른 프레임 검증.
- `qa/preview-verification.json`: 실제390/740px 브라우저에서 로딩/틈/가로넘침 검사 및12초간격GIF 픽셀변화 검사.
- 미검증: 운영몰 교체·실제 결제/수령. 이번 수정에서는 실행하지 않았다.

## 재현

프로젝트 루트에서:

```sh
node landing/ebook-aside-blog-v3/qa/render.mjs landing/ebook-aside-blog-v3
python3 landing/ebook-aside-blog-v3/qa/package.py
node landing/ebook-aside-blog-v3/qa/check-preview.mjs landing/ebook-aside-blog-v3
```

렌더러는 전체이미지에만 data-poster를 사용한다. 편집HTML과 미리보기의GIF 참조는 유지한다. 모든 브라우저 작업은 headless.
