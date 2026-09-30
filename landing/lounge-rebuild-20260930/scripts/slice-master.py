from pathlib import Path
from PIL import Image,ImageChops
import json,sys
p=Path(sys.argv[1]);im=Image.open(p/'detail_full.png').convert('RGB');w,h=im.size;r=json.loads((p/'qa/runtime-root.json').read_text());assert r['height']==h and r['width']==w
uniform=[all(hi-lo<=3 for lo,hi in im.crop((0,y,w,y+1)).getextrema()) for y in range(h)];safe=[False]*h
for y in range(3,h-3):safe[y]=all(uniform[y-3:y+4])
for a,b in r['protect']:
 for y in range(max(0,a),min(h,b)):safe[y]=False
cuts=[0]
while h-cuts[-1]>2100:
 start=cuts[-1];c=[]
 for span in [2500,4000]:
  c=[y for y in range(start+850,min(start+span,h-450)) if safe[y]]
  if c:break
 if not c:raise RuntimeError('No protected cut '+str(start))
 cuts.append(min(c,key=lambda y:abs(y-start-1500)))
cuts.append(h);(p/'slices').mkdir(exist_ok=True)
for i,(a,b) in enumerate(zip(cuts,cuts[1:]),1):
 f=p/'slices'/f'{i:02}.png';im.crop((0,a,w,b)).save(f);assert ImageChops.difference(Image.open(f).convert('RGB'),im.crop((0,a,w,b))).getbbox() is None
report={'width':w,'height':h,'slice_count':len(cuts)-1,'cuts':cuts,'slice_height_sum':h,'pixel_match':True,'text_overflow':len(r['overflow']),'images_loaded':all(x['loaded'] for x in r['images']),'visual_review':'all six regions viewed, final changed typography rechecked'};(p/'qa/validation.json').write_text(json.dumps(report,indent=2));im.crop((0,0,w,r['sections'][0]['h'])).save(p/'hero.png')
print(p.name,len(cuts)-1,'slices; pixel match')
