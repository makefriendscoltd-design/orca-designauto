# 실제 페이지 코드 조사와 적용

2026-10-01, Chrome headless에서 공개 HTML/CSS와 계산된 스타일을 확인했다. 제3자 이미지·강사 사진·성과·강의 혜택은 가져오지 않았다.

| 확인한 페이지 | 코드·화면 관찰 | 이번 적용 |
|---|---|---|
| [콜로소 상세페이지 디자인](https://coloso.co.kr/products/graphicdesign-jeonghaneul) | 본문980px, 2열480px+20px+480px. `.fc-layout-206 .container__body` flex row-reverse, `.catalog-curriculum__list` 이미지480×270 | 사례 이미지와 설명을 분리한 2열, 결과물 3열, 단계별 이미지 |
| [패스트캠퍼스 상세페이지 절대공식](https://fastcampus.co.kr/mktg_online_pages) | 실습 결과물 중심, 본문980px. 주요 헤드라인은 이미지여서 글꼴 수치를 DOM에서 얻을 수 없음 | 먼저 완성 예제를 보여주고 구성 방법을 설명하는 순서 |
| [Flux Framer Masterclass](https://www.flux-academy.com/courses/the-framer-masterclass) | 실제 제작 화면 중심 히어로. DOM h1 72/76.8px, h2 56/67.2px | 자체 HTML을 렌더한 작업 화면 히어로, 큰 헤드라인과 얇은 보조 설명 |

740px 상세 이미지 규격으로 다시 설계했다. `design.css`에서 본문 안쪽652px, 제목77px/1.12, 섹션 제목55–59px/1.2, 본문29px을 사용한다. 레퍼런스 코드를 그대로 복제한 것이 아니라 실제 구조와 비율을 확인해 적용했다.

## 자체 이미지 정본
- `example-page.html`: 책30장의 남성 올인원 시나리오를 발췌·요약해 작성한 학습용 화면. 실제 판매제품이나 효과 인증 이미지가 아니다.
- `qa/render-example.mjs`: 위 HTML을 렌더해 assets/example-full.png, example-hero.png 생성.
- assets/current-cover.png: 기존 승인 최신 3D 표지.
- 이전 v5 생성 화장품 사진 제외. 커뮤니티 회원수 제외.
- 원문: incoming/lounge-ebooks-20260929/lounge-books/landing-page/원문.md, 9·16·19·21·25·30장.
- 매출은 운영사 전체 누적 매출이며 이 책 또는 랜딩페이지 한 개의 성과로 표현하지 않음.

조사 원본 HTML/CSS·캡처는 /tmp/landing-course-refs, /tmp/landing-ref-coloso에 있다. 비교사이트 자산은 배포물에 포함하지 않는다. 별도 조사한 fastcampus.co.kr/dgn_online_figma는 실제 접속404로 근거에서 제외했다.
