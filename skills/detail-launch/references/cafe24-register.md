# 카페24 상품 등록 — 관리자 화면 자동화

몰: `makehobby0707` (메이크패밀리 / makefamily.kr). 26-07-29 실측으로 전 과정 성공.

## API 가 풀렸다 (26-07-31 확인) — 기존 상품 수정은 API 로 한다

토큰 스코프에 **`mall.read_product` · `mall.write_product` 가 들어와 있다.**
(예전엔 403 이었다. 이 문서의 옛 서술을 믿고 화면부터 열지 말 것.)

```python
json.load(open(os.path.expanduser('~/coding/cafe24bot/token.json')))['scopes']
# ['mall.read_order','mall.write_order','mall.read_shipping','mall.write_shipping',
#  'mall.read_product','mall.write_product','mall.read_category']
```

### 되는 것 / 안 되는 것

| 작업 | 방법 |
|---|---|
| 상세설명 주입 (PC·모바일) | **`PUT /api/v2/admin/products/{no}`** — Froala 3중 세팅 함정이 통째로 사라진다 |
| 대표이미지 교체 | **`POST /api/v2/admin/products/{no}/images`** — base64 를 `detail_image` 로 주면 **4종(big/medium/tiny/small) 자동 생성** |
| 상품 조회·백업 | `GET /api/v2/admin/products/{no}` |
| **상세설명용 이미지 업로드** | **API 로 안 된다.** 관리자 세션이 필요해 Chrome 으로 해야 한다 (아래 3절) |

### ⚠️ 최상위 `shop_no` 가 없으면 쓰기가 조용히 무시된다 (26-08-04 실측)

`{'request':{...}}` 만 보내면 **HTTP 200 에 정상 응답까지 오는데 값이 안 바뀐다.**
`{'shop_no':1,'request':{...}}` 로 보내면 1회에 들어간다.
이 문서와 메모리에 적혀 있던 *"PUT 200 인데 반영 안 됨 → 3회 재시도"* 증상은
사실상 전부 이것이었다. **재시도 루프를 짜기 전에 `shop_no` 부터 확인할 것.**

**`GET` 도 마찬가지다.** `shop_no` 없이 조회하면 몰이 여러 개인 상품은
**shop 1 과 shop 4 값이 호출마다 번갈아 나온다.** display 가 T→F→T 로 요동쳐서
"저장이 되돌아갔다"고 오진하게 된다. 검증 GET 에도 항상 `shop_no` 를 명시한다.

```python
cl.get(f'/api/v2/admin/products/278', shop_no=1)   # 이렇게
```

몰별 가격은 별개 필드다. 26-08-04 에 278 의 shop 4 판매가는 PUT 3회가 다 안 먹어
890,000 이 그대로 남았다(진열 F 라 노출은 안 됨). **기본몰만 고치고 끝내지 말 것.**

```python
# 상세설명 — 이미지 URL 은 상대경로로. 멀티도메인(makefamily.kr / makehobby0707)에서 둘 다 뜬다
cl.put('/api/v2/admin/products/277',
       {'shop_no':1,'request':{'description':html,'mobile_description':html}})

# 대표이미지 — request 는 단수, images 업로드용 엔드포인트는 requests 복수라 헷갈린다
cl.post('/api/v2/admin/products/277/images',
        {'shop_no':1,'request':{'image_upload_type':'A','detail_image':b64}})
```

함정: `POST /api/v2/admin/products/images`(상품번호 없는 쪽)는 `{'requests':[{'image':b64}]}`
형식이고 `/web/upload/NNEditor/...` 경로를 준다. **그 경로는 대표이미지로 못 쓴다**
(`422 [Product image] Wrong image path`). 반드시 상품번호가 붙은 엔드포인트를 쓸 것.

함정 2: 상품번호 붙은 쪽의 키는 **`detail_image`** 다. `image` 로 보내면
**에러 없이 현재 이미지 URL 만 되돌려준다** — 성공으로 오진하기 딱 좋다.
반영 판정은 응답 URL 의 날짜 폴더가 바뀌었는지(`/202607/` → `/202608/`)로 한다.
같은 URL 이 돌아오면 안 올라간 것이다.

**그래도 이미지 업로드는 화면이 필요하므로 아래 절차가 여전히 유효하다.**

## 등록 절차 (Claude-in-Chrome)

`https://makehobby0707.cafe24.com/disp/admin/product/productregister`

### 1. 표시 설정

- **진열상태·판매상태 둘 다 `전체`** 체크 (몰 4개: 한국어2 · 영어 · 일본어)
- 상품분류: 목록에서 고르고 **`적용` 버튼을 눌러야** 반영된다. 안 누르면 저장 시 빠진다
  - 이 몰의 분류: `멤버십` `전문대행` `AI 직원 인력사무소` `-`
  - **`-` 는 실제로 존재하는 분류다.** "분류 없음"이 아니다
- 메인 진열: 상품 성격에 맞는 영역 체크 (`무료 웨비나 리스트` 등)

### 2. 기본 정보

**섹션 헤더 클릭이 토글이라 접혔다 펴졌다 한다.** 접힌 상태에서 좌표를 찍으면
엉뚱한 곳에 입력되고 조용히 실패한다. **입력 전 스크린샷으로 펼침을 확인**하고,
좌표 대신 `find` 로 얻은 ref 로 클릭한다.

- 상품명 → 4개 몰에 자동 복사된다
- 상품명(관리용) 50자 제한
- 상품 요약설명 — 일시·가격·핵심 조건을 한 줄로

### 3. 상세설명 이미지 — **에디터 UI를 쓰지 않는다** (26-07-30 갱신)

에디터는 **Froala** 다. 업로드 엔드포인트를 인스턴스에서 직접 읽어 `fetch` 로 쏘면
**왕복 19번이 3번으로 줄고 토글·드롭존 함정이 전부 사라진다.** 이게 현재 표준 방법이다.

```js
// 1) 엔드포인트 확보 — FroalaEditor.INSTANCES 는 7개(상세·모바일·사이즈·결제·배송·교환·CS) 순서 고정
const inst = FroalaEditor.INSTANCES[0];          // product_description
inst.opts.imageUploadURL    // /ind-script/nnEditor/filemanager2/upload.php?uploadPath=/home/ec_users/<몰ID>/public_html/web/upload/NNEditor/
inst.opts.imageUploadParam  // "photoupload"
inst.opts.imageMaxSize      // 5,242,880 (장당 5MB)
```

```js
// 2) 핸들러 없는 전용 input 을 새로 만들어 file_upload 로 전량 주입 (한 번에 다 됨, 합계 10MB 미만)
//    #iconFiles 는 multiple 이지만 onchange 로 아이콘이 등록돼 버리니 쓰지 말 것
const f=document.createElement('input');
f.type='file'; f.multiple=true; f.id='CLAUDE_BULK';
f.setAttribute('aria-label','CLAUDE_BULK_TARGET');   // find 로 잡을 손잡이
f.style.cssText='position:fixed;left:20px;top:120px;width:460px;height:40px;opacity:1;z-index:2147483647;';
document.body.appendChild(f);
```

```js
// 3) 한 번의 JS 호출 안에서 순차 POST — 여기서 왕복이 0 이 된다
for(const file of [...document.getElementById('CLAUDE_BULK').files]){
  const fd=new FormData(); fd.append(inst.opts.imageUploadParam, file, file.name);
  const j=JSON.parse(await (await fetch(inst.opts.imageUploadURL,
      {method:'POST',body:fd,credentials:'same-origin'})).text());
  // {"result":"success","name":"s0.jpg","size":"1080px/1508px","link":"/web/upload/NNEditor/20260730/s0.jpg"}
}
```

끝나면 만든 input 을 `remove()` 한다.

함정:
1. **같은 파일명이 이미 있으면 `copy-<epoch>-원본명.jpg` 로 사본이 생긴다.**
   테스트로 1장 올려봤으면 그 이름은 이미 점유됐다. 최종 HTML엔 원본 경로를 쓴다.
   상품마다 접두사를 갈라둘 것 (`s*` `v5_*` `tp_*` …)
2. **업로드 성공을 응답만으로 믿지 말 것.** 경로가 예측 가능하니 HEAD 로 전수 검증하고
   `content-length` 를 로컬 파일 크기와 대조한다
3. **순서는 응답 순서가 아니라 내가 만든 배열로 정한다.** 정렬된 HTML을 통째로 덮어쓴다

### ⚠️ 연속 업로드는 캡차에 걸린다 (26-07-31 실측) — 가장 크게 막힌 지점

20장을 쉬지 않고 POST 했더니 **15장째부터 차단**됐다. 응답이 JSON 이 아니라
`쇼핑몰 접속 인증 안내` HTML 로 바뀐다 — *"고객님 PC의 네트워크 IP에서 과다접속이 유입되어"*.

```js
// 판정 : JSON 이면 통과, HTML 이면 캡차
try{ const j=JSON.parse(t); ok=(j.result==='success'); }
catch(e){ /* DOMParser 로 title 확인 → '접속 인증' 이면 CAPTCHA */ }
```

- **장당 4~6초 간격**을 넣는다. 간격 없이 20장은 확실히 걸린다.
  실측(26-08-03): **6초 간격이면 23장도 안 걸린다** (10 + 7 + 6 으로 나눠 올림)
- **한 번의 javascript_tool 호출은 45초에서 타임아웃된다.** 12장×6초=72초로 짜면
  중간에 끊긴다(끊겨도 업로드는 진행 중일 수 있으니 **HEAD 로 어디까지 갔는지 먼저 확인**).
  한 배치는 **6~7장**으로 끊는 게 안전하다
- 한 번 걸리면 **시간이 지나도 자동으로 안 풀린다.** 4초 간격 재시도도 계속 막혔다
- **캡차는 Claude 가 풀지 않는다.** 사용자가 직접 입력해야 한다.
  `/captcha/form` 을 GET 으로 열면 쇼핑몰 메인으로 리다이렉트돼 화면이 안 나온다 →
  업로드 POST 응답 HTML 을 그대로 탭에 그려주면 사용자가 풀 수 있다:

```js
let html = await (await fetch(URL_UP,{method:'POST',body:fd,credentials:'same-origin'})).text();
html = html.replace(/<head([^>]*)>/i, '<head$1><base href="https://makehobby0707.cafe24.com/">');
document.open(); document.write(html); document.close();   // 사용자가 입력 → 인증 확인
```

`<base>` 를 안 넣으면 캡차 이미지가 상대경로라 깨진다. 인증 뒤엔 바로 JSON 이 돌아온다.

### 응답 본문이 `[BLOCKED: Cookie/query string data]` 로 나올 때

javascript_tool 이 쿠키성 문자열을 마스킹한 것이다. **본문을 통째로 반환하지 말고**
`t.length` · `/success/.test(t)` · `DOMParser` 로 뽑은 `title` 처럼 **가공한 값만** 돌려받으면 읽힌다.

### 3-B. 상세설명 주입 — PC·모바일 3중 세팅

Froala 라서 `html.set` 만으로는 저장 시 덮이는 경우가 있다. **셋 다** 한다.

```js
function setEditor(name, html){                    // 'product_description' / '_mobile'
  const inst=FroalaEditor.INSTANCES.find(e=>e.$oel[0].name===name||e.$oel[0].id===name);
  if(inst){ inst.html.set(html); inst.undo.saveStep(); }
  const ifr=document.getElementById(name+'_IFRAME');
  if(ifr?.contentDocument?.body) ifr.contentDocument.body.innerHTML=html;
  const ta=document.querySelector(`textarea[name="${name}"]`);
  ta.value=html; ta.dispatchEvent(new Event('change',{bubbles:true}));
}
```

이미지 나열 HTML은 `font-size:0;line-height:0` 래퍼로 감싼다. 안 하면 조각 사이에 틈이 생긴다.

```html
<div style="max-width:1080px;margin:0 auto;font-size:0;line-height:0;">
<img src="/web/upload/NNEditor/…/s0.jpg" alt="" style="display:block;width:100%;max-width:1080px;height:auto;border:0;margin:0;padding:0;">
…
</div>
```

```js
// iframe 과 textarea 둘 다 세팅해야 한다. iframe 만 바꾸면 저장 시 덮인다
document.getElementById('product_description_IFRAME').contentDocument.body.innerHTML = html;
[...document.querySelectorAll('textarea')]
  .filter(t=>/product_description/i.test(t.name))
  .forEach(t=>{ t.value=html; t.dispatchEvent(new Event('change',{bubbles:true})); });
```

### 4. 대표이미지 — 자동화 된다 (26-07-29 갱신)

예전 문서엔 "사람이 드래그해야 함"으로 적혀 있었으나 **뚫렸다.**

```js
// 1) hidden input 을 잠깐 드러낸다 (다른 file input 과 헷갈리지 않게 라벨을 붙인다)
const f=document.getElementById('imageFiles');
f.setAttribute('aria-label','THUMB_TARGET');
f.style.cssText='position:fixed;left:20px;top:200px;width:420px;height:40px;opacity:1;z-index:2147483647;';
```
→ `find` 로 `THUMB_TARGET` ref 획득 → `file_upload` → `change` 이벤트 디스패치
→ **상세·목록·작은목록·축소 4종이 한 번에 채워진다.**

**"+ 등록" 버튼은 절대 클릭하지 말 것.** OS 파일 다이얼로그가 열려 세션이 막힌다.

### 5. 판매 정보

- 소비자가 / 공급가 — 0원 상품이면 그대로 0
- **판매가**: 기본몰에 값을 넣고 **`환율 자동계산`** 클릭
  → 메이크패밀리 채널(KRW) · PRO 영어(USD) · PRO 일본어(JPY) 까지 자동으로 채워진다.
  안 누르면 다른 몰 가격이 비어 저장이 막힌다
- **배송방법 `자체배송`** → 배송비 무료. 0원 상품에 배송비가 붙으면 신청이 막힌다

### 6. 저장

`상품등록` 버튼 클릭. **탭이 5~15초 멈춘다** (이미지가 많을수록).
스크린샷이 타임아웃 나도 실패가 아니다.

성공 판정은 **URL 전이**로 한다:
```
/exec/admin/shop1/product/productregister   ← 처리 중
/disp/admin/shop1/product/productmanage     ← 완료 (상품목록으로 이동)
```

## 기존 상품 수정 (여러 상품에 같은 상세페이지 붙이기)

> **먼저 위 API 절을 볼 것.** 상세설명 주입·대표이미지 교체는 이제 API 로 되고,
> 그게 아래 화면 조작보다 훨씬 안전하다. 화면이 필요한 건 **상세설명용 이미지 업로드뿐**이다.

### ⚠️ 상세설명에 큰 이미지가 박힌 상품은 수정 화면을 열면 안 된다

`product_no=277` 은 상세설명이 **13,267px 롱이미지 한 장**이었는데, 수정 화면을 열자
에디터가 그걸 로드하다 **렌더러가 죽었다** (Runtime.evaluate 45초 타임아웃 ×2, 스크린샷도 실패).
CLAUDE.md 의 "4,000px 넘는 이미지를 에디터에 넣으면 브라우저가 얼어붙는다"가 이 현상이다.

→ 이미지 업로드는 **대시보드처럼 가벼운 관리자 페이지에서** 한다.
Froala 인스턴스가 없어도 엔드포인트는 고정이라 그대로 쓸 수 있다:

```
POST /ind-script/nnEditor/filemanager2/upload.php?uploadPath=/home/ec_users/<몰ID>/public_html/web/upload/NNEditor/
param: photoupload
```

주입은 API 로 하므로 수정 화면은 끝까지 안 열어도 된다.

```
https://makehobby0707.cafe24.com/disp/admin/product/productregister?product_no=107
```
→ **`상품 수정` 화면으로 열린다.** 신규 등록과 같은 URL 이다.
저장 버튼은 `상품등록` 이 아니라 **`상품수정`(a 태그)**, 전이 URL 은 `/exec/admin/shop1/product/ProductModify`.

**상세설명은 상품마다 별개 필드다. 공통 편집 기능은 없다.** 대신 이렇게 한다:

1. 이미지는 **한 번만** 업로드해 `/web/upload/NNEditor/YYYYMMDD/` URL 을 확보
2. 그 URL 로 만든 **똑같은 HTML 문자열**을 상품마다 주입 → 이미지 재업로드 없음
3. 상품 수가 늘어도 3-B 주입 + 저장만 반복하면 된다

**덮어쓰기 전에 기존 상세설명을 백업한다.** 카페24엔 상세설명 되돌리기가 없다.
관리자 textarea 값은 tool 로 못 읽어올 때가 있으니(쿠키성 문자열로 차단됨)
**외부 HTTP 로 스토어프런트를 받아 파일로 저장**하는 게 확실하다.
옛 이미지 파일 자체는 서버에 남으므로 URL만 알면 복구된다.

기수·일정처럼 **상품별로 다른 정보는 본 페이지에 넣지 말고 마지막 1장으로 분리**한다.
그래야 공통 조각을 그대로 재사용할 수 있다. (`detail_<상품>_schedule.html` → `s18_schedule.jpg`)

## 등록 후 검증

얼어붙은 탭 대신 **외부 HTTP 요청으로 실제 상품페이지**를 받아 문자열 검사한다.
`requests` 는 **UA 헤더가 없으면 403** 이다.

```python
h={'User-Agent':'Mozilla/5.0 … Chrome/126 Safari/537.36'}
r = requests.get('https://makefamily.kr/product/detail.html', params={'product_no':'107'}, headers=h)
len(set(re.findall(r'NNEditor/20260730/(s[\w]+\.jpg)', r.text)))   # 새 슬라이스 전수
re.findall(r'NNEditor/20260715/[\w.]+', r.text)                    # 옛 이미지 잔존 여부
re.findall(r'/web/product/(?:big|small)/\d+/\S+', r.text)          # 대표이미지
```

**브라우저로 확인할 땐 반드시 새 탭에서 연다.** 저장 직후 기존 탭은 옛 DOM 을 붙들고 있어
리로드·쿼리스트링 캐시버스터로도 안 바뀐다. 실제로 서버는 새 내용을 주는데
탭에서만 `#prdDetail` 이미지가 1장으로 보여 오진하기 쉽다.

### 스토어프런트에 엣지 캐시가 있다 — 저장 실패로 오진하지 말 것

`makefamily.kr` 은 `x-cache: HIT` 를 반환하는 캐시 뒤에 있고 **쿼리스트링 캐시버스터가 안 먹는다.**
어떤 상품은 10초 안에 반영되고 어떤 상품은 **몇 분 뒤에** 바뀐다. 26-07-30 에 125 를 저장한 뒤
"안 됐다"고 판단해 같은 작업을 두 번 했다. 아래 순서로 판정한다.

1. **관리자에 저장됐는지가 진짜 판정 기준이다.** 편집 페이지를 다시 열어 textarea 를 읽는다
   ```js
   const ta=document.querySelector('textarea[name="product_description"]');
   ({ new:(ta.value.match(/NNEditor\/20260730/g)||[]).length, old:(ta.value.match(/NNEditor\/20260429/g)||[]).length })
   ```
2. 화면 상단의 **`최종 상품수정일`** 이 오늘로 바뀌었으면 저장 자체는 성공한 것이다
3. 그 다음에 `makehobby0707.cafe24.com` (원본 호스트)로 확인 → 여기가 먼저 바뀐다
4. `makefamily.kr` 은 20초 간격으로 재시도하며 기다린다. 두 번째 시도쯤 바뀐다

### 저장 버튼 — 화면 밖이면 ref 클릭이 빗나간다

저장 버튼은 **`a#eProductModify`** (텍스트 `상품수정`). 하단 고정 바에 같은 라벨이 또 있어
`find` 가 화면 밖(예: y=847, 뷰포트 714)의 것을 잡아오면 클릭이 아무 일도 안 한다.

```js
document.getElementById('eProductModify').scrollIntoView({block:'center'});
document.getElementById('eProductModify').click();   // 좌표 클릭보다 확실하다
```

**`.click()` 을 쓰면 즉시 페이지가 전이하므로 같은 JS 호출 안에서 `await sleep` 을 걸지 말 것**
(`Inspected target navigated` 에러가 난다 — 실패가 아니다).
`/disp/admin/product/ProductBlank` 로 튀는 경우가 있는데 이때도 저장은 되어 있으니
반드시 1번 기준으로 확인하고, 성급히 재시도하지 않는다.

스토어프런트는 상세 이미지를 **lazy-load** 한다. 방금 로드한 직후엔 `naturalHeight === 1`
(1px 플레이스홀더)로 나오니 스크롤·대기 후 판정한다. 총 렌더 높이로 검산하면 편하다.

배송비는 상품페이지에 `배송방법 배송필요 없음 / 배송비 무료` 로 찍힌다.

## 등록 후 연결 작업

1. **`.env` 의 `CAFE24_PRODUCT_NO` 에 새 번호를 쉼표로 추가** (`275,279`)
   → 매시간 도는 `ship.py` 가 이 주문도 배송완료 처리한다. 안 하면 배송준비중으로 쌓인다
2. **`order-notify` 스킬**로 상품번호에 안내 문구를 건다.
   `notify.py` 는 스케줄러에 없다 — 사람이 `--execute` 를 붙여야만 나간다.
   **실제 발송은 사용자 승인을 받고 실행한다**

## 실측 기록

| 항목 | 값 |
|---|---|
| product_no 279 | `[무료웨비나] 직장인을 위한 수출 매칭 수익화 클래스` |
| 상품코드 | `P0000OKT` |
| 상세 이미지 | 12장 (1080×~1500, 각 200~300KB) |
| 소요 | 이미지 업로드가 대부분. 12장에 약 12회 왕복 (구 방식) |

| 항목 | 값 (26-07-30 · 기존 상품 수정) |
|---|---|
| product_no 107 | `(8월/9월) AIMAX 창업 프로그램 4기` · 상품코드 `P00000ED` · 판매 18건 |
| 옵션 | `4기 (8월반)` / `5기 (9월반) (+200,000)` — 기수는 옵션으로 처리돼 있다 |
| 상세 이미지 | 19장 (슬라이스 18 + 일정 1), 합계 2,981KB |
| 소요 | **왕복 3회** — file_upload 1 + POST 루프 1 + 주입 1 |
