# 랜딩페이지의 정석 개편

- 출력 폭740px, 논리폭398px. 사용자 승인 컨셉 v10의 그라데이션·타이포 대비·애셋 비율을 계승.
- 원문: incoming/lounge-ebooks-20260929/lounge-books/landing-page/원문.md
- 기존 운영값 근거: landing/ebook-landing-page/brief.md, 현재값 root 독립 API 교차확인 완료.
- 가격: 30,000원; 상품번호: 297
- 새 수치·후기·성과 주장 없음. UI 시각예시는 실제 제품 화면으로 주장하지 않음.
- vault-start는 기존 usage-kit의 최신 책전체 TXT 첨부 방식 적용.
- 최신 표지: root 제공 /tmp/lounge-current-covers/landing-page.png (최종 QA에서 해시 기록)
- 외부 등록 없음.

## 검증
- 실제 Chrome 렌더740×15926,6구간 직접검수. 폰트5종 및 모든이미지 로드, 가로넘침0.
- 슬라이스11장, 높이합·원본픽셀일치 확인.
- 현재가 root 독립API교차확인 완료: 297=30000원,282=50000원;vault무료로그인.
- humanize latest quick-rules 직접점검 및 verify_gates 결과 qa/humanize/gates.txt.
- 표지해시 qa/validation.json. 실제등록 및 유료구매자 권한동선은 미검증.
