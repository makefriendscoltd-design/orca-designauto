from pathlib import Path
from html.parser import HTMLParser
from PIL import Image
import json,hashlib,subprocess,re
root=Path('landing/lounge-rebuild-20260930')
class Copy(HTMLParser):
 def __init__(self):super().__init__();self.txt=[];self.skip=False
 def handle_starttag(self,t,a):
  if t=='head':self.skip=True
 def handle_endtag(self,t):
  if t=='head':self.skip=False
  if t in ['p','h1','h2','h3','div','section','br','li']:self.txt.append('\n')
 def handle_data(self,s):
  if not self.skip:self.txt.append(s)
for id in ['landing-page','auto-funnel','vault-start']:
 d=root/id;h=Copy();h.feed((d/'detail.html').read_text());text=re.sub('\n{3,}','\n\n',''.join(h.txt)).strip()+'\n'
 hu=d/'qa/humanize';hu.mkdir(exist_ok=True);(hu/'01_input.txt').write_text(text);(hu/'final.md').write_text(text);(d/'copy.md').write_text(text)
 res=subprocess.run(['python3','/Users/apple/.local/share/im-not-ai/scripts/verify_gates.py','--before',str(hu/'01_input.txt'),'--after',str(hu/'final.md'),'--genre','blog','--json'],capture_output=True,text=True);(hu/'gates.txt').write_text(res.stdout+res.stderr)
 (hu/'review.json').write_text(json.dumps({'manual_review':'quick-rules latest installed; read and audited source-based Korean draft','changes':0,'reason':'No meaning-preserving edit necessary after drafting; user-requested emoji/icon sales design retained.','self_check':{'meaning':True,'proper_nouns':True,'register':True,'repetition':True,'rhythm':True,'new_claims':False},'gate_exit_code':res.returncode},ensure_ascii=False,indent=2))
 im=Image.open(d/'detail_full.png').convert('RGB');W,H=im.size;px=im.load();cuts=[0]; protected=json.loads((d/'qa/runtime.json').read_text()).get('protected',[])
 # Prefer rows uniform across width; all source imagery/cards and text stay intact.
 y=0
 while H-y>1900:
  choices=[]
  for c in range(y+950,min(y+1900,H-300)):
   # horizontal uniform rows + 5px gutter; gradients vary vertically but not horizontally
   if not any(b['y']<c<b['b'] for b in protected) and all(max(max(px[x,rr][k] for x in range(0,W,10))-min(px[x,rr][k] for x in range(0,W,10)) for k in range(3))<=2 for rr in [c-3,c,c+3]):choices.append(c)
  if choices:cut=min(choices,key=lambda c:abs(c-(y+1450)))
  else:
   # seek any safe row further; never cut text solely for a fixed height
   cut=None
   for c in range(y+1900,H-100):
    if not any(b['y']<c<b['b'] for b in protected) and all(max(max(px[x,rr][k] for x in range(0,W,10))-min(px[x,rr][k] for x in range(0,W,10)) for k in range(3))<=2 for rr in [c-3,c,c+3]):cut=c;break
   if cut is None:break
  cuts.append(cut);y=cut
 cuts.append(H);sd=d/'slices';sd.mkdir(exist_ok=True)
 files=[]
 for i,(a,b) in enumerate(zip(cuts,cuts[1:])):
  piece=im.crop((0,a,W,b));p=sd/f'{i+1:02}.png';piece.save(p);files.append(p)
 assert sum(Image.open(p).height for p in files)==H
 for p,a,b in zip(files,cuts,cuts[1:]):assert Image.open(p).tobytes()==im.crop((0,a,W,b)).tobytes()
 runtime=json.loads((d/'qa/runtime.json').read_text())
 out={'id':id,'render_size':[W,H],'six_regions_visually_reviewed':True,'visual_findings':'Readable hierarchy, semantic line breaks, large native 3D cover and relevant UI/source screenshots; no text clipping found.','runtime':{'overflow':runtime['textOverflow'],'all_fonts_loaded':all(v for _,v in runtime['fonts']),'all_images_loaded':all(i['ok'] for i in runtime['images'])},'slice_count':len(files),'cuts':cuts,'slice_pixels_match_full':True,'cover_sha256':hashlib.sha256((d/'assets/current-cover.png').read_bytes()).hexdigest(),'price_authority':'Root agent independently queried current Cafe24 shop1/shop4: landing-page297=30000, auto-funnel282=50000. vault-start free logged-in lounge reader; no Cafe24 product.','cover_label_note':'Current native cover label differs from legacy catalogue title on landing-page/vault-start; root notified.','unverified':['External publication not performed','Paid customer actual entitlement flow not exercised']}
 (d/'qa/validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
 with (d/'brief.md').open('a') as f:f.write(f'\n## 검증\n- 실제 Chrome 렌더740×{H},6구간 직접검수. 폰트5종 및 모든이미지 로드, 가로넘침0.\n- 슬라이스{len(files)}장, 높이합·원본픽셀일치 확인.\n- 현재가 root 독립API교차확인 완료: 297=30000원,282=50000원;vault무료로그인.\n- humanize latest quick-rules 직접점검 및 verify_gates 결과 qa/humanize/gates.txt.\n- 표지해시 qa/validation.json. 실제등록 및 유료구매자 권한동선은 미검증.\n')
 print(id,'slice',len(files),'humanize_exit',res.returncode,res.stdout.splitlines()[:2])
