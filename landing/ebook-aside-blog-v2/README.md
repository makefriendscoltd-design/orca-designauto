# ASIDE 블로그 전자책 상세페이지 v2

2026-09-30 제작 완료. 이전 운영본은 `../lounge-rebuild-20260930/aside-blog/`에 보존했다. 이 폴더는 새 제작·검수 산출물이며 운영 페이지 교체는 하지 않았다.

## 정본과 출처

- 운영값: `../lounge-rebuild-20260930/catalog-audit.json`의 presentationId `aside-blog`. 상품399, 30,000원. 주문 이메일 PDF 수령 및 동일 이메일 라운지 재열람 유지.
- 원문: `../../incoming/lounge-ebooks-20260929/pdf-books/ebook-aside-blog/제작브리프.md`, `asset-35.pdf`. 원문4개 챕터의 준비·지시·검수·재작업으로 구성.
- 편집 정본: `detail.html`, `design.css`. 출력폭740px, 로컬 Pretendard5종.
- 이미지 출처: 이전 운영본 `qa/asset-provenance.json`, `qa/evidence-restored.json`. 기존8개 이미지 전부 해시 유지. 추가로 책 속 에디터 화면 `p15_img0.png` 사용.
- 실제 책의 실습과 설명용 예시를 구분. 저자·회사·커뮤니티 실적의 주체와 시점을 명시. 새로운 외부 사실 주장은 추가하지 않음.

## 구성과 산출물

복붙 문제 → 지시 범위 비교 → 실제 작업 화면 → 저자 실적 → 준비/지시/검수 → 4개 챕터 → 운영사 연간 매출·커뮤니티 증빙 → FAQ → 구매 안내.

밝은 그라데이션과 네이비, 블루와 표지의 노랑을 사용. 비교25px/43px, 본문28px, 제목49–65px로 역할 구분. 최신3D 표지와 저자 사진, 실습 캡처, 의미에 맞는 이모지를 배치.

- `detail_full.png`: 740×14672. 이전19318px 대비 약24% 축소.
- `hero.png`: 첫 화면. 별도 상품 썸네일 제작은 이번 범위에 없음.
- `preview.html`: 모바일 대응 조각 이미지 미리보기. 구매 버튼은 이미지 표현이며 결제 기능 없음.
- `slices/`: 10장. 보호영역 밖 배경행 절단, 높이 합과 전체 픽셀 재조립 일치.
- `qa/region-1.png`~`region-6.png`: 전체6구간 직접 확인. 표지 아래 제목과 구분선 간격 수정 후 재검수.
- `qa/runtime.json`: 실제 headless Chrome, 폰트5종·이미지10회 로딩, 가로 넘침0.
- `qa/evidence-coverage.json`: 기존 자료 누락0. 저자600시간+/1,500명+, 연매출40.5/41.3/27.6억, 카페12,127명·라운지2,885명 유지.
- `qa/humanize/`: 최신 설치본 quick-rules 직접 점검 및 의미 보존 게이트 통과. 초안 후 추가 윤문0%, 수치·인용·말투 PASS.
- `qa/launch-expected.json`: 기존 카탈로그를 변환한 검사용 허용값이며 운영 정본 아님. 운영값 검사 불일치0.
- `qa/preview-verification.json`: 390/740px 실제 브라우저, 각10장 로딩, 가로 넘침·이미지 사이 틈0.
- 미검증: 운영몰 교체, 실제 결제·PDF 수령. 이번 제작에서 실행하지 않음.

## 재렌더

이 폴더에서 `node qa/render.mjs "$PWD"`. Chrome headless로 폰트·이미지 decode 후 캡처한다. 슬라이스는 기존 `../lounge-rebuild-20260930/scripts/slice-master.py`의 보호영역 검사 방식을 사용한다.
