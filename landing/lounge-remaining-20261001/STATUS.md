# 미개편 전자책 교체 — 2026-10-01

사용자 승인: 기존 개별교체 건 제외, 최근 등록분 포함 전자책 상세페이지를 제작·교체·등록. 고객 메시지 발송/가격/판매상태/배송 설정 변경은 범위 밖.

- 전체16권 중 기존개별교체5권(컨셉,Threads PREMIUM,ASIDE,YouTube,자동퍼널) 제외.
- 대상11권: threads-basic,vault-start,smartstore-part1,zerobaek,ai-delegation,live-400,landing-page,smartstore-part2,smartstore-part3,hwaleo,naver-search.
- 디자인: 기존 구성 발전. v6전면교체 방식 미사용. 기존 실제증빙·본문캡처 보존, 최신3D표지 재확인. 랜딩은 승인v7그대로.
- 기존6권 강한헤드/타이포/간격/누적매출카드로 갱신. 신규4권 기존확정카피·자료 유지하며 책자/실제본문이미지/타이포비율 개선.
- 운영정본: /Users/apple/orca/projects/cafe24/launches/ebooks-remaining-20261001/inventory.json, backup/.
- 제로백 shop1=무료/shop4=30000,AI비서shop1=20000/shop4=99000 별도 렌더. 비진열shop4상태보존.
- Cafe24 완료:10상품×2몰=20건 PC/mobile설명변경,독립API재조회·가격/판매/진열등보존. 공개PC/mobile20뷰 실제이미지decode·가격·틈0·가로넘침0. CDN SHA256 전수일치.
- 무료라운지2소개:격리worktree의 lib/ebook-introductions.json만수정,12테스트PASS/Next webpack프로덕션빌드PASS,master e4b7ab6 push. 실제배포일치/게스트4뷰전이미지·접힘·읽기버튼검증완료.
- 최초Turbopack빌드는외부node_modules심볼릭링크제한으로실패,문서지원webpack빌드성공. 고객메시지/가격/자동배송변경없음.

- 2026-10-01 등록실행확인:20건전부provider readback성공/website성공메타데이터기록. 제외상품집합과업데이트집합교집합0. 공개20뷰PASS. 라운지e4b7ab6배포/필수라우트PASS,게스트4뷰검증완료.

## 완료
- 사용자요청11권상세개편·등록완료. 최근4권포함/기존개별5권제외. 전체보기index.html. publication-verification.json이최종검증요약.
- 실제구매·고객메일수신은이번작업에서재실행하지않음. 비공개shop4공개렌더는미검증,API20건으로구분.
