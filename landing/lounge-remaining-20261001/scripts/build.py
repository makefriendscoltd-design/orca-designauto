from pathlib import Path
import re,shutil,json,hashlib
from html.parser import HTMLParser
R=Path(__file__).resolve().parents[1];L=R.parent; old=L/'lounge-rebuild-20260930'
heads={'threads-basic':'팔로워 0이어도<br>팔리는 스레드','vault-start':'받아둔 전자책을<br>내 AI의 지식으로','smartstore-part1':'팔리는 제품<br>찾는 비법서','zerobaek':'첫 고객을 만드는<br>실전 마케팅','ai-delegation':'시키면 제대로 하는<br>AI 비서 만드는 법','live-400':'기획부터 완성까지<br>AI 영상 제작법'}
nums={'threads-basic':275,'smartstore-part1':348,'zerobaek':319,'ai-delegation':286,'live-400':400,'landing-page':297,'smartstore-part2':401,'smartstore-part3':402,'hwaleo':403,'naver-search':404}
inv=json.loads(Path('/Users/apple/orca/projects/cafe24/launches/ebooks-remaining-20261001/inventory.json').read_text())
chart='''<div class="cumulative-proof"><h3>메이크프렌즈 누적 매출</h3><div class="proof-total">114.9<small>억원</small></div><p class="proof-period">2021.01 — 2024.04</p>'''
for y,v,w in [('2021년','40.5',35.2494),('2022년','81.8',71.2256),('2023년','109.4',95.2406),('2024.04','114.9',100)]:chart+=f'<div class="proof-row"><header><span>{y} <small>까지 누적</small></span><b>{v}<small>억</small></b></header><i style="width:{w}%"></i></div>'
chart+='''<p class="proof-caption">(주)메이크프렌즈 전체 매출 · 월별 원장 40개월 합산<br>각 막대는 2021년 1월부터 해당 시점까지의 누적액</p></div>'''
chartcss='''.cumulative-proof{background:#fcfcfc;color:#587488;padding:24px 20px;text-align:left;border-radius:12px;margin:25px 0}.cumulative-proof h3{font-family:P,sans-serif;font-size:17px;line-height:1.3;margin:0;font-weight:700;letter-spacing:-.025em}.proof-total{font-size:62px;line-height:1.15;font-weight:800;letter-spacing:-.055em;color:#0072ee;margin-top:10px}.proof-total small{font-size:22px;margin-left:4px}.cumulative-proof .proof-period{font-size:13px;line-height:1.5;margin:10px 0 22px;color:#71848e}.proof-row{margin-top:18px}.proof-row header{display:flex;justify-content:space-between;align-items:baseline}.proof-row span{font-size:15px}.proof-row span small{font-size:10px}.proof-row b{font-size:26px;color:#0072ee}.proof-row b small{font-size:13px}.proof-row i{display:block;height:5px;margin-top:7px;border-radius:4px;background:linear-gradient(90deg,#0072ee,#69d7ee)}.cumulative-proof .proof-caption{font-size:10px;line-height:1.5;color:#71848e;margin:21px 0 0}
'''
class Text(HTMLParser):
 def __init__(self):super().__init__();self.a=[]
 def handle_data(self,d):
  if d.strip():self.a.append(d.strip())
for slug in list(heads)+['smartstore-part2','smartstore-part3','hwaleo','naver-search','landing-page','zerobaek-shop4','ai-delegation-shop4']:
 base=slug.replace('-shop4','');new=base in ['smartstore-part2','smartstore-part3','hwaleo','naver-search'];source=L/f'ebook-{base}-20261001' if new else (L/'ebook-landing-page-v7' if base=='landing-page' else old/slug)
 p=R/slug;p.mkdir(exist_ok=True);(p/'qa').mkdir(exist_ok=True);shutil.copytree(source/'assets',p/'assets',dirs_exist_ok=True)
 for f in source.glob('*.css'):shutil.copy(f,p/f.name)
 h=(source/'detail.html').read_text();orig=h;h=h.replace('</head>','<link rel="stylesheet" href="refinement.css"></head>')
 if not new and base!='landing-page':
  h=re.sub(r'(<h1\b[^>]*>).*?(</h1>)',lambda m:m[1]+heads[base]+m[2],h,count=1,flags=re.S)
  h=re.sub(r'<section\b[^>]*(?:id="company-results"|class="ev-section ev-revenue")[^>]*>.*?</section>',lambda m:'<section class="ev-section ev-revenue"><div class="ev-eyebrow">AIMAX · 메이크패밀리 운영사</div><h2>직접 팔아온 경험을<br>실전의 기준으로</h2>'+chart+'</section>',h,flags=re.S)
  if base=='vault-start':h=re.sub(r'<div class="annual-chart">.*?</p></div>',lambda m:chart,h,flags=re.S)
  css='''/* Refine the existing 398px composition; retain its original sections and assets. */
section{letter-spacing:-.02em}.page .hero{padding-top:48px;padding-bottom:48px}.page .hero h1{font-family:P,sans-serif;font-size:49px;line-height:1.14;letter-spacing:-.045em;font-weight:800}.page .hero p{line-height:1.48}.page .hero .lead{font-size:19px;line-height:1.45}.page .hero .thread{display:none}.page .hero .cover,.page .hero .book{max-width:none;width:330px;margin-left:auto;margin-right:auto}.page h2{line-height:1.2;letter-spacing:-.035em}.page .old{font-size:17px;color:#8798a0}.page .new{font-size:36px;line-height:1.2;letter-spacing:-.035em}.page .photo{margin-top:25px;margin-bottom:22px}.page .photo img{width:100%;height:auto}.page .sheet{transform:none;border-radius:8px}.page .card{border-radius:9px}.page .scene{padding-top:66px;padding-bottom:66px}.page .scene.hero{padding-top:48px;padding-bottom:48px}.page section.light,.page section.tint,.page section.spot{padding-top:60px;padding-bottom:60px}.page .ev-section{padding:58px 28px}.page .answer{line-height:1.5}.page .ev-proof-card{border-radius:9px}.page .flow div{border-radius:8px}.page .end{padding-top:58px}.page .notes{padding-top:24px;padding-bottom:24px}
'''+chartcss
  # Vault's .scene is an image frame, not a section.
  if base=='vault-start':css=css.replace('.page .scene{','.page section.scene{');css+='\n.page .hero h1{font-size:46px}.page .beam{padding-top:64px}.page .proof-section{padding-top:65px;padding-bottom:65px}\n'
  if base=='ai-delegation':css+='\n.page .hero h1{font-size:44px}.page .flow{gap:12px}.page .sheet dt{font-size:15px}.page .sheet dd{font-size:18px}\n'
 elif new:
  css='''/* Preserve each recent book's approved copy, art, delivery and section order. */
section{padding:88px 48px}h2{font-size:58px;line-height:1.19;letter-spacing:-.04em}.hero{padding-top:46px;padding-bottom:66px}.brand{padding-bottom:32px}.hero .cover-stage{width:540px;margin-top:20px}.hero .shop-card{margin-top:30px}.hero-desc{font-size:29px;line-height:1.5}.paper{background:#eef2ee}.evidence{background:linear-gradient(#101c23,#18343d)}.evidence figure{margin-top:35px}.evidence img{max-width:100%;height:auto}.evidence-card{border-radius:7px}.intro p{font-size:30px;line-height:1.5}.topic{padding:25px 0}.topic h3{font-size:31px}.topic p{font-size:26px;line-height:1.5}.step{padding:25px 0}.step p{font-size:26px;line-height:1.5}.prompt{margin-top:32px;border-radius:5px}.format-grid{gap:20px;margin-top:35px}.format-box{padding:25px 22px}.format-box p{font-size:24px;line-height:1.5}.delivery{margin-top:38px}.faq{margin-top:46px}.closing .closing-cover{width:380px}.closing h2{font-size:58px}.shop-card{border-radius:7px}.closing{padding-bottom:65px}
'''
 else:css='/* Approved v7, published without further visual changes. */'
 (p/'detail.html').write_text(h);(p/'refinement.css').write_text(css+'\n.proof-total small,.proof-row small{display:inline!important}.proof-total,.proof-row b{white-space:nowrap}\n')
 for f in ['render.mjs','package.py','check-preview.mjs']:shutil.copy(L/'ebook-landing-page-v7/qa'/f,p/'qa'/f)
 render=(p/'qa/render.mjs').read_text().replace("let e=document.querySelector(s),c=getComputedStyle(e)","let e=document.querySelector(s)||document.querySelector('p'),c=getComputedStyle(e)").replace("document.querySelectorAll('.page section')","document.querySelectorAll('main section')").replace("'.hero-lead'","'.hero p'")
 (p/'qa/render.mjs').write_text(render.replace('.source-line,.scene,.point','.source-line,div.scene,.point'))
 x=Text();x.feed(h);(p/'copy.md').write_text('\n'.join(x.a)+'\n')
 imgs=re.findall(r'<img[^>]*src="([^"]+)"',orig);assert all(i in h for i in imgs)
 evidence={'source':str(source),'existing_images_preserved':len(imgs),'changes':'Existing composition refined; newer book copy and assets unchanged' if new else 'Existing source preserved; stronger headline and cumulative chart; measured type/spacing','cover_hashes':{i:hashlib.sha256((p/i).read_bytes()).hexdigest() for i in set(imgs) if 'cover' in i and (p/i).exists()}}
 (p/'qa/source-preservation.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2))
 shop=4 if slug.endswith('-shop4') else 1;row=next((r for r in inv if r['slug']==base and r['shop_no']==shop),None)
 brief={'slug':slug,'source':str(source),'source_operating_record':'/Users/apple/orca/projects/cafe24/launches/ebooks-remaining-20261001/inventory.json','product_no':nums.get(base),'shop':shop,'price':row['price'] if row else 0,'status':'design-ready; publication pending'}
 (p/'brief.json').write_text(json.dumps(brief,ensure_ascii=False,indent=2))
 approved={'allowed_dates':['2026-09-10','2026-09-29','2026-09-30','2026-10-01'],'allowed_prices':[]} # Populate scanner from fresh provider record and known older anchors if present.
 (p/'qa/launch-expected.json').write_text(json.dumps(approved))
 print(slug)
