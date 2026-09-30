# 스레드 PREMIUM 상세 리빌드 — 2026-09-30

승인된 컨셉 v10의 다크·라이트 전환, 큰 타이포 대비, 그라데이션 스포트라이트, 이모지, 광원 CTA를 스레드 내용에 맞춰 재구성했습니다. 최신 공유 3D표지를 상단·구성·마지막 모두 같은 파일로 사용합니다. 본책 실제 내지 4종, 별책·워크북 표지로 텍스트 연속 구간을 나눴습니다. AI 채팅 카드는 사용 예시로 표시했습니다.

- 정본: detail.html / design.css / brief.json. 운영값 근거는 brief.json의 기존 상품·원문 경로.
- 전체: detail_full.png 740×32623. hero.png / copy.md.
- 안전 슬라이스: slices/*.png. qa/validation.json에서 개수·좌표·높이합·픽셀일치 확인.
- QA: 실제 Chrome headless, 폰트5굵기/이미지10개 로드, 가로 넘침0. 전체6구간을 직접 검수했습니다. qa/overview.jpg는 한눈에 보는 판이며 원본은 전체PNG.
- 본책61p/별책11p/워크북10p는 배송원본PDF를 PyMuPDF로 검증했습니다.
- 330,000원 두 슬롯 일치. 상품277과별칭6개는 같은페이지 대상. 기존30부/30일실행후피드백/평생업데이트/발송후환불불가 정책 보존. 성과보장 추가없음.
- humanize: 최신 quick-rules 직접검수, verify_gates.py gate OK, 0% 불필요윤문없음. 원고작성과최종윤문단계를분리. qa/consistency.json 가격1종 issues0.
- 전자책원문이나 구매자상담캡처를 새로배포하지 않습니다. 판매노출허용 기존내지예시만사용.
- 외부발행·Git·상품가격·대표이미지 변경 없음. root가 등록전실제상품상태/정책을최종대조해야 합니다.

재렌더: `python3 /Users/apple/.agents/skills/detail-page/scripts/render_detail.py detail.html detail_full.png --width 740 --maxh 50000` (현재폴더에서실행).
