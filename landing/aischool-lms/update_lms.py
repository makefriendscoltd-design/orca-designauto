"""상품 395 갱신 — 롱이미지 조각 사이에 연출영상 GIF 를 순서대로 끼운다.

HTML 에는 GIF 자리에 마젠타 마커(.gifmark)만 굽는다. 여기서 마커 띠를 찾아
그 자리에서 이미지를 끊고 _gifseq.json 순서대로 GIF 를 넣는다.
description = [가격덮개 style] + [유튜브 iframe] + [조각·GIF] + [월결제 배너]
"""
import base64, json, os, re, sys, time
from pathlib import Path
sys.path.insert(0, str(Path.home() / "orca/projects/cafe24"))
os.chdir(Path.home() / "orca/projects/cafe24")
from dotenv import load_dotenv; load_dotenv()
from cafe24_client import Cafe24Client
from PIL import Image

HERE = Path("/Users/apple/orca/workspaces/designauto/강의-상세페이지/landing/aischool-lms")
FULL = HERE / "out/lms_poster.png"
SEQ  = json.loads((HERE / "_gifseq.json").read_text())
OUT  = HERE / "out/sl"
CACHE = HERE / "_up_lms.json"
NO, YT = 395, "e2Jp0D3jwOU"   # 「제가 교장입니다」. 옛 Y1k44op1ZLk 는 비공개(403)라 접근 오류가 났다
BAND = "/web/upload/NNEditor/20261008/1bae15c45a66c2bf6393d76f22970bed.png"
SUMMARY = "1년 정규과정 · 6팀 24직군 · AI 빌드데이 · 정원 30명 · 수강료 300만원 (12개월 할부)"

im = Image.open(FULL).convert("RGB"); W, H = im.size
px = im.load()
def mag(y):
    hit = sum(1 for x in range(0, W, 20)
              if px[x, y][0] > 230 and px[x, y][1] < 40 and px[x, y][2] > 230)
    return hit > (W // 20) * 0.8
bands, cur = [], None
for y in range(H):
    if mag(y) and cur is None: cur = y
    elif not mag(y) and cur is not None:
        bands.append((cur, y)); cur = None
if cur is not None: bands.append((cur, H))
# 마커가 연달아 붙으면 하나로 합쳐 잡힌다 → 높이(60px)로 나눠 개수를 복원한다
MARK = 60
split = []
for b0, b1 in bands:
    n = max(1, round((b1 - b0) / MARK))
    step = (b1 - b0) / n
    for k in range(n):
        split.append((int(b0 + step * k), int(b0 + step * (k + 1))))
bands = split
print(f"full {W}x{H} · 마커 {len(bands)}개 / GIF {len(SEQ)}개")
assert len(bands) == len(SEQ), f"마커와 GIF 수가 안 맞음 {len(bands)} vs {len(SEQ)}"

# 마커 사이 구간을 1400px 로 조각내고, 마커 자리에 GIF 를 끼운 순서 리스트를 만든다
OUT.mkdir(parents=True, exist_ok=True)
for f in OUT.glob("*.jpg"): f.unlink()
seg, n, prev = [], 0, 0
for i, (b0, b1) in enumerate(bands + [(H, H)]):
    y = prev
    while y < b0:
        h = min(1400, b0 - y)
        p = OUT / f"s{n:02d}.jpg"
        im.crop((0, y, W, y + h)).save(p, quality=88, subsampling=0)
        seg.append(("img", p)); n += 1; y += h
    if i < len(bands):
        seg.append(("gif", HERE / "gifs" / f"{SEQ[i]}.gif"))
    prev = b1
print(f"조각 {sum(1 for t,_ in seg if t=='img')} + GIF {sum(1 for t,_ in seg if t=='gif')}")

c = Cafe24Client()
b64 = lambda p: base64.b64encode(p.read_bytes()).decode()
rel = lambda u: re.sub(r"^https?://[^/]+", "", u)
def up(paths):
    out = []
    for i in range(0, len(paths), 10):
        ch = paths[i:i+10]
        r = c.post("/api/v2/admin/products/images", {"requests": [{"image": b64(x)} for x in ch]})
        ims = r.get("images") or []
        assert len(ims) == len(ch), r
        out += [rel(x.get("path") or x.get("image_path")) for x in ims]
    return out

if CACHE.exists():
    urls = json.loads(CACHE.read_text())
else:
    urls = up([p for _, p in seg])
    CACHE.write_text(json.dumps(urls, ensure_ascii=False, indent=1))
print("업로드", len(urls))

img = lambda u: f'<img src="{u}" style="display:block;width:100%;max-width:740px;" alt="">'
video = (f'<div style="position:relative;width:100%;max-width:740px;margin:0 auto;padding-top:56.25%;background:#000;">'
         f'<iframe src="https://www.youtube.com/embed/{YT}?rel=0" title="AI 학교" '
         f'style="position:absolute;left:0;top:0;width:100%;height:100%;border:0;" '
         f'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>')
ONCLICK = "product_submit(1,'/exec/front/order/basket/',document.querySelector('a.btnSubmit.gFull'));return false;"
band = (f'<a href="#none" onclick="{ONCLICK}" style="display:block;cursor:pointer;">'
        f'<img src="{BAND}" style="display:block;width:100%;max-width:740px;" alt="300만원 12개월 할부 · 월 250,000원으로 시작하기"></a>')
style = ('<style>'
 '#span_product_price_text,span.quantity_price,#mf-sum dl dd,#mf-sum dl.mf-total dd,.xans-product-detail .total{font-size:0!important;color:transparent!important;letter-spacing:0!important}'
 '#span_product_price_text::after,span.quantity_price::after,#mf-sum dl dd::after{content:"300만원 · 12개월 할부";font-size:16px;color:#111;font-weight:800}'
 '.xans-product-detail .total::after{content:"300만원 · 12개월 할부 (월 250,000원)";font-size:22px;color:#111;font-weight:900}'
 '.xans-product-detail .total *{font-size:0!important;color:transparent!important}'
 '#mf-sum,tr.productPrice,#totalProducts{display:none!important}'
 '</style>')
html = (f'{style}<div style="max-width:740px;margin:0 auto;font-size:0;line-height:0;">\n'
        f'{video}\n' + "\n".join(img(u) for u in urls) + f'\n{band}\n</div>')
for shop in (1, 4):
    c.put(f"/api/v2/admin/products/{NO}", {"shop_no": shop, "request":
          {"description": html, "mobile_description": html, "summary_description": SUMMARY}})
time.sleep(3)
# 대표이미지 교체 — 스킨 상단에 뜨는 썸네일. 상세만 바꾸면 옛 디자인이 그대로 남는다
THUMB = HERE / "out/thumb_lms.png"
if THUMB.exists():
    r = c.post(f"/api/v2/admin/products/{NO}/images",
               {"shop_no": 1, "request": {"image_upload_type": "A", "detail_image": b64(THUMB)}})
    print("대표이미지 교체:", (r.get("image") or {}).get("detail_image", r))
    time.sleep(2)

for shop in (1, 4):
    p = c.get(f"/api/v2/admin/products/{NO}", shop_no=shop)["product"]
    d = p.get("description") or ""
    print(f"shop{shop} img={d.count(chr(60)+chr(105)+chr(109)+chr(103))} gif={d.count('.gif')} yt={YT in d} thumb={(p.get('detail_image') or '')[-12:]}")
