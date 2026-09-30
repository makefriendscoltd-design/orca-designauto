# 라운지 전자책 상세페이지 전체 개편

`index.html`에서 현재 라운지 12종을 확인할 수 있습니다. 컨셉 책은 기존 승인본 `../ebook-concept-ecommerce-v10/`을 사용하고, 나머지 11종을 이 폴더에서 제작했습니다.

## 편집과 재생성

- 정본: 각 상품의 `detail.html`, `design.css`, `assets/`와 원문·가격 근거.
- 파생물: `detail_full.png`, `hero.png`, `slices/`. 직접 수정하지 않습니다.
- 상세페이지는 740px 폭으로 렌더합니다. 현재 표지를 상단·하단에 사용하며, 본문 예시와 실물 캡처의 출처를 각 상품 QA에 기록했습니다.
- QA는 전체 구간 시각 검수, 폰트·이미지 로딩, 텍스트 넘침, 슬라이스 재조립 픽셀 일치, 한국어 카피 검수를 포함합니다.
- 일반 런타임 검사는 `node scripts/check-detail.mjs <상품폴더>`로 실행합니다. Playwright 설치가 필요하며 다른 설치본은 `PLAYWRIGHT_MODULE`로 지정합니다.
- 검사 후 `python3 scripts/slice-master.py <상품폴더>`로 텍스트·카드 경계를 피하는 슬라이스를 생성합니다. Pillow가 필요합니다.

## 운영 변형

기본몰과 shop4의 기존 가격이 다른 상품은 별도로 렌더했습니다. 가격 자체를 변경한 작업이 아닙니다.

| 상품번호 | 기본몰 | shop4 | 변형 폴더 |
|---|---:|---:|---|
| 321 | 110,000원 | 99,000원 | youtube-bisu-shop4 |
| 286 | 20,000원 | 99,000원 | ai-delegation-shop4 |
| 319 | 0원 | 30,000원 | zerobaek-shop4 |

319는 주문 후 이메일 PDF를 받는 상품입니다. 로그인만으로 무료로 읽는 `threads-basic`, `vault-start`와 구분합니다. 275의 shop4 판매·진열 중지 상태도 유지합니다.

무료 두 권은 라운지 기존 읽기·목차 아래에 접히는 책 소개를 추가했습니다. 구매 권한이나 원래 읽기 동작은 변경하지 않습니다.

## 근거와 배포

- `catalog-audit.json`: 작업 시작 시점 라운지 카탈로그 12종과 원문 매핑.
- 각 `qa/`: 런타임·시각·카피 검증.
- `qa-independent-review.md`: 별도 검수 결과와 발견 사항. 제목 및 배송 안내 수정은 최종 산출물에 반영했습니다.
- `qa-app-production.json`: 무료 책 소개의 실제 라운지 배포 검증.
- `publication-verification.json`: Cafe24 API 및 공개 페이지 최종 대조.
- `PROGRESS.md`: 현재 완료 상태와 미검증 범위.

운영 백업과 실행 스크립트는 Cafe24 작업공간의 `launches/lounge-all-20260930/`에 보관합니다. 원본 PDF 전문이나 고객 정보는 이 폴더에 포함하지 않습니다.
