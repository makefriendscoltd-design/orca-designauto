"""Regenerate gap-safe slices from the rendered master. Requires Pillow."""
from pathlib import Path
from PIL import Image, ImageChops
import json
root=Path(__file__).resolve().parents[1]
im=Image.open(root/'detail_full.png').convert('RGB');width,height=im.size
uniform=[all(hi-lo<=3 for lo,hi in im.crop((0,y,width,y+1)).getextrema()) for y in range(height)]
safe=[False]*height
for y in range(3,height-3):safe[y]=all(uniform[y-3:y+4])
cuts=[0]
while height-cuts[-1]>2100:
 start=cuts[-1];candidates=[]
 for span in (2400,5000):
  candidates=[y for y in range(start+900,min(start+span,height-550)) if safe[y]]
  if candidates:break
 if not candidates:raise RuntimeError(f'No safe cut after {start}; inspect the layout')
 cuts.append(min(candidates,key=lambda y:abs(y-start-1500)))
cuts.append(height);dest=root/'slices';dest.mkdir(exist_ok=True)
expected={f'{i:02}.png' for i in range(1,len(cuts))}
extra={p.name for p in dest.glob('*.png')}-expected
if extra:raise RuntimeError(f'Stale slices: {sorted(extra)}. Archive them before rebuilding.')
for i,(a,b) in enumerate(zip(cuts,cuts[1:]),1):
 out=dest/f'{i:02}.png';im.crop((0,a,width,b)).save(out)
 assert ImageChops.difference(Image.open(out).convert('RGB'),im.crop((0,a,width,b))).getbbox() is None
report={'width':width,'height':height,'slice_count':len(cuts)-1,'cuts':cuts,'slice_height_sum':sum(b-a for a,b in zip(cuts,cuts[1:])),'slice_pixels_match_full':True}
(root/'qa/slices-rebuild.json').write_text(json.dumps(report,indent=2));print(f'PASS {len(cuts)-1} slices / {width}x{height}')
