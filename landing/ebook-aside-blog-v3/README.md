# ASIDE 블로그 전자책 v3

2026-09-30. v2를 사용자가 디자인 퇴화로 반려. 직전 승인 Threads PREMIUM/컨셉 v10의 실제 렌더와 치수를 기준으로 다시 제작했다. v2는 보존한다.

후속 수정: 세로 매출 막대를 삭제하고 컨셉v10의 가로 막대 매출카드 HTML/CSS를 그대로 이식했다. 같은398→740배율로 렌더했으며8개 셀렉터의 글자크기·굵기·행간·자간·패딩·폭을 실제 브라우저에서 비교해 차이0개를 확인했다(`qa/approved-chart-comparison.json`). 본문은 승인 Threads의19px×배율/행간1.48/자간-0.018em, 히어로 리드는26px×배율/행간1.4/자간-0.025em으로 맞췄다. 블로그 캡처는 원본 y560부터270px만 CSS로 표시해 방문수 영역을 완전히 제외했다.

## 변경

책 내용·PC·동영상 보강: 원본 28쪽 PDF와 대조해 맥/윈도우 설치 준비, 실제 작성 프롬프트, 꾸미기 조건, 8개 검수 항목, 중단된 작업 이어가기와 CLI 안내를 구체화했다. 본문 15쪽 실제 지시문 캡처와 화면별 설명을 추가했다. `qa/book-content-verification.json`에 원문 대조를 기록했다.

연속 구성 후속 수정: `flow.css`와4개 구간 래퍼가 여러 섹션의 배경·광원을 공유한다. 준비/지시/검수 배경을 이어 깔고, 밝은 구간으로 전환하는 부분은 점진적으로 연결했다. 비교·추천대상·FAQ·커뮤니티의 반복 카드 박스를 줄였다. 이 배경 수정 단계에서는 문구가 동일했으며, 아래의 책 내용 보강 단계에서 카피를 추가했다. `qa/flow-before-after.jpg`는 왼쪽수정전/오른쪽수정후 주요경계 비교다. 경계행 RGB변화 최대216.33→0.88(`qa/flow-verification.json`), 전체6구간 직접검수,390/740px GIF변화·이미지틈0 확인. 최종PNG14장+GIF1개이며 안전절단은 가로균일색뿐 아니라 세로변화가 매끄러운 그라데이션도 보호영역 밖에서 허용한다.

- 짙은 배경, 금색 그라데이션 제목, 대형3D 표지, 광원·스포트라이트 전환. 제목79px/리드48.34px, 비교33px/65px, 본문35.33px를 기준으로 역할을 구분했다.
- 순서: 히어로 → 메이크패밀리 블로그 이웃 증거 → 실제 작성GIF → 반복 수작업 문제 → 저자 → 준비/지시/검수 → 목차 → 기존 회사·커뮤니티 증빙 → FAQ/구매.
- 네이버 블로그 @makefamily_ 공개 프로필에 표시된 이웃10,700명을 강조. 조회일2026.09.30. 실제 페이지 캡처와 HTML subscriberCount 대조. ASIDE로 늘어난 수치라고 주장하지 않는다.
- 09.22 실제 라이브 원본의00:34:46.5–00:35:00.5를 추출. 빈 에디터→제목·본문 입력→이미지 삽입. 재연·생성 화면 없이7초 반복(원본14초를2배속).
- 기존8개 증빙·표지 이미지 해시와 기존 연간/교육/회원 수치를 유지했다.

## 정본·출처

- 운영값 정본: `../lounge-rebuild-20260930/catalog-audit.json`, presentationId `aside-blog`. 상품399,30,000원, 주문 이메일PDF 수령/동일이메일 라운지 재열람 유지.
- 내용: `../../incoming/lounge-ebooks-20260929/pdf-books/ebook-aside-blog/제작브리프.md`, `asset-35.pdf`.
- 이미지 계보: `../lounge-rebuild-20260930/aside-blog/qa/asset-provenance.json`, `qa/evidence-restored.json`.
- 블로그 원문: https://m.blog.naver.com/makefamily_ . `qa/blog-evidence.json`, `assets/evidence/blog-neighbors.png`.
- 이웃수는 원문 화면의 충실한 인용이다. 공개프로필이 유일한 원출처이며 외부기관 독립확인은 없음. 연구게이트의 숫자주장2기관 조건을 충족했다고 보고하지 않는다. 강한 인과·효과 주장으로 확대하지 않는다.
- 영상 원본 및 크롭: `qa/live-provenance.json`. 원본 동영상은 저장소에 복사하지 않았다.

## 출력과 검수

- 편집 정본: `detail.html`, `design.css`, `flow.css`.
- **GIF 포함 미리보기: `preview.html`**. PNG14장과 실제 GIF1개를 조합한다. GIF 영역은 정적 슬라이스로 대체하지 않는다.
- `detail_full.png`: 740×23146, GIF는 대표 프레임으로 보여주는 정적 전체 보기.
- `demo.html`: 재생 버튼이 있는 실제 라이브 MP4 확인 페이지. 390px 실제 브라우저에서 재생 시간 증가, 반복·음소거·컨트롤 확인(`qa/video-verification.json`).
- `hero.png`: 첫 화면. 별도 상품 썸네일은 요청 범위에 없음.
- GIF: `assets/live/aside-live-writing.gif`,740×600,105프레임,7초,약1.28MB. 에디터 영역만 원본에서 크롭했다.
- `qa/package.py`: 정적 영역 안전절단, GIF 행 별도 유지, 대표 프레임 재조립 전체픽셀 일치 검사.
- `qa/runtime.json`: 폰트5종·모든 이미지 로딩, 가로 텍스트 넘침0.
- `qa/region-1.png`~`region-6.png`: 전체6구간 직접 검수. 신규 블로그 캡처/라이브 포스터/원본 연속프레임도 확인.
- `qa/evidence-coverage.json`: 기존8개 이미지 누락0, 원본해시 일치.
- `qa/humanize/gates.txt`: 최신 설치본 quick-rules 직접 점검, 의미보존·수치·인용·말투 게이트PASS. 초안후 추가윤문0%.
- `qa/launch-consistency.json`: 불일치0. 시간검출은 영상오프셋·촬영기록·코드 포맷이며 행사 일정이 아니다.
- `qa/gif-verification.json`:105프레임/7000ms/105개 서로 다른 프레임 검증.
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
